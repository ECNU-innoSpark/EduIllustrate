#!/usr/bin/env python3
"""
MCP Server for Explanation Generation (HTTP Mode)
This server exposes the explanation generation functionality through MCP protocol over HTTP.
"""

import os
import sys
import json
import asyncio
import re
import time
from typing import Optional, Dict, Any, List
from pathlib import Path
from PIL import Image
import base64
from io import BytesIO

try:
    from fastmcp import FastMCP
except ImportError:
    print("Error: fastmcp package not found. Install it with: pip install fastmcp", file=sys.stderr)
    sys.exit(1)

# Add current directory to path to import local modules
sys.path.insert(0, str(Path(__file__).parent))

from mllm_tools.litellm import LiteLLMWrapper

# Initialize FastMCP server
mcp = FastMCP("Explanation Generation Server")


@mcp.tool()
async def generate_diagram_and_text(
    problem: str,
    output_dir: str,
    image_path: Optional[str] = None,
    model: str = "gemini-3-pro-preview",
    max_retries: int = 3,
    max_scene_concurrency: int = 5,
    translate_to_chinese: bool = True,
) -> str:
    """
    Generate educational diagram and text explanation from a problem.

    This tool generates Manim-based educational diagrams and step-by-step text explanations
    for mathematical/scientific problems.

    Args:
        problem: The problem text to generate explanation for
        output_dir: Absolute path to directory where outputs will be saved
        image_path: Optional absolute path to an image file associated with the problem
        model: AI model to use (e.g., gemini-3-pro-preview, Kimi-K25)
        max_retries: Maximum number of retry attempts on failure
        max_scene_concurrency: Maximum concurrent scene processing
        translate_to_chinese: Whether to translate content to Chinese

    Returns:
        JSON string with generation results including paths to generated files
    """
    try:
        # Import here to avoid circular dependencies
        from generate_explanation import ExplanationGenerator

        # Initialize models
        planner_model = LiteLLMWrapper(
            model_name=model,
            temperature=0.7,
            print_cost=True,
            verbose=False,
            use_langfuse=False
        )

        scene_model = LiteLLMWrapper(
            model_name=model,
            temperature=0.7,
            print_cost=True,
            verbose=False,
            use_langfuse=False
        )

        helper_model = LiteLLMWrapper(
            model_name=model,
            temperature=0.7,
            print_cost=True,
            verbose=False,
            use_langfuse=False
        )

        # Load image if path provided
        problem_image = None
        if image_path:
            if not os.path.exists(image_path):
                return json.dumps({
                    "error": f"Image file not found: {image_path}",
                    "success": False
                })
            try:
                problem_image = Image.open(image_path)
            except Exception as e:
                return json.dumps({
                    "error": f"Failed to open image: {e}",
                    "success": False
                })

        # Create explanation generator
        explanation_generator = ExplanationGenerator(
            planner_model=planner_model,
            scene_model=scene_model,
            helper_model=helper_model,
            output_dir=output_dir,
            verbose=False,
            use_rag=False,
            use_context_learning=False,
            use_visual_fix_code=False,
            use_langfuse=False,
            max_scene_concurrency=max_scene_concurrency,
            translate_to_chinese=translate_to_chinese
        )

        topic = "problem_0_math"

        description = problem
        if problem_image:
            description += "\n(Note: The attached image is the original diagram.)"

        # Save problem image if provided
        if problem_image:
            file_prefix = re.sub(r'[^a-z0-9_]+', '_', topic.lower())
            output_topic_dir = os.path.join(explanation_generator.output_dir, file_prefix)
            os.makedirs(output_topic_dir, exist_ok=True)
            problem_image_save_path = os.path.join(output_topic_dir, "problem_diagram.png")
            problem_image.save(problem_image_save_path)

        start_time = time.perf_counter()

        await explanation_generator.generate_markdown_diagrams(
            topic,
            description,
            max_retries=max_retries,
            only_plan=False,
            problem_image=problem_image,
        )

        elapsed = time.perf_counter() - start_time

        # Find generated output files
        file_prefix = re.sub(r'[^a-z0-9_]+', '_', topic.lower())
        output_topic_dir = os.path.join(explanation_generator.output_dir, file_prefix)
        video_path = None
        doc_path = None

        if os.path.exists(output_topic_dir):
            for f in os.listdir(output_topic_dir):
                if f.endswith('.mp4'):
                    video_path = os.path.join(output_topic_dir, f)
                    break
            doc_dir = os.path.join(output_topic_dir, "doc")
            solution_path = os.path.join(doc_dir, "solution.md")
            if os.path.exists(solution_path):
                doc_path = solution_path

        return json.dumps({
            "success": True,
            "output_dir": output_topic_dir,
            "video_path": video_path or "Not found",
            "doc_path": doc_path or "Not found",
            "time_seconds": elapsed
        }, indent=2, ensure_ascii=False)

    except Exception as e:
        import traceback
        return json.dumps({
            "error": f"Error during generation: {str(e)}",
            "traceback": traceback.format_exc(),
            "success": False
        })


@mcp.tool()
async def list_available_models() -> str:
    """
    List all available AI models that can be used for explanation generation.

    Returns:
        JSON string containing list of available models
    """
    # Load allowed models
    allowed_models_path = Path(__file__).parent / 'src' / 'utils' / 'allowed_models.json'
    try:
        with open(allowed_models_path, 'r') as f:
            models_data = json.load(f)
            models = models_data.get("allowed_models", [])

        return json.dumps({
            "success": True,
            "models": models,
            "count": len(models)
        }, indent=2)
    except Exception as e:
        return json.dumps({
            "error": f"Error loading models list: {str(e)}",
            "success": False
        })


@mcp.tool()
async def png_to_base64(
    image_path: str,
    resize_width: Optional[int] = None,
    resize_height: Optional[int] = None
) -> str:
    """
    Convert a PNG image to base64 encoded string.

    This tool reads a PNG image file and converts it to a base64 encoded string.
    Optionally, you can resize the image before encoding.

    Args:
        image_path: Path to the PNG image file
        resize_width: Optional width to resize the image (maintains aspect ratio if height not specified)
        resize_height: Optional height to resize the image (maintains aspect ratio if width not specified)

    Returns:
        JSON string containing the base64 encoded image

    Example:
        Input: "path/to/image.png"
        Output: {
            "success": true,
            "base64": "/9j/4AAQSkZJRg...",
            "format": "PNG",
            "original_size": [800, 600],
            "encoded_size": [800, 600]
        }
    """
    try:
        # Check if file exists
        if not os.path.exists(image_path):
            return json.dumps({
                "error": f"Image file not found: {image_path}",
                "success": False
            })

        # Check if file is a valid image
        try:
            img = Image.open(image_path)
            original_size = img.size
            img_format = img.format

            # Convert to RGB if necessary (for RGBA or other modes)
            if img.mode in ('RGBA', 'LA', 'P'):
                # Create a white background
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                img = background

            # Resize if requested
            if resize_width or resize_height:
                if resize_width and resize_height:
                    # Both dimensions specified
                    new_size = (resize_width, resize_height)
                elif resize_width:
                    # Only width specified, maintain aspect ratio
                    aspect_ratio = img.size[1] / img.size[0]
                    new_size = (resize_width, int(resize_width * aspect_ratio))
                else:
                    # Only height specified, maintain aspect ratio
                    aspect_ratio = img.size[0] / img.size[1]
                    new_size = (int(resize_height * aspect_ratio), resize_height)

                img = img.resize(new_size, Image.Resampling.LANCZOS)
                encoded_size = new_size
            else:
                encoded_size = original_size

            # Convert to base64
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            img_bytes = buffer.getvalue()
            base64_string = base64.b64encode(img_bytes).decode('utf-8')

            return json.dumps({
                "success": True,
                "base64": base64_string,
                "format": img_format or "PNG",
                "original_size": list(original_size),
                "encoded_size": list(encoded_size),
                "file_size_bytes": len(img_bytes)
            }, indent=2)

        except Exception as e:
            return json.dumps({
                "error": f"Failed to process image: {str(e)}",
                "success": False
            })

    except Exception as e:
        return json.dumps({
            "error": f"Error converting image to base64: {str(e)}",
            "success": False
        })


if __name__ == "__main__":
    import uvicorn

    # Get port from environment or use default
    port = int(os.environ.get("MCP_PORT", 8000))
    host = os.environ.get("MCP_HOST", "0.0.0.0")

    print(f"Starting Explanation Generation MCP Server on {host}:{port}")

    # Run the server
    mcp.run(transport="sse", host=host, port=port)
