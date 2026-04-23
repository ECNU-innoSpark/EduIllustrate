import os
import re
import subprocess
import asyncio
from PIL import Image
from typing import Optional, List
import traceback
import sys

from src.core.parse_explanation import (
    get_images_from_explanation,
    image_with_most_non_black_space
)
from mllm_tools.vertex_ai import VertexAIWrapper
from mllm_tools.gemini import GeminiWrapper

class ExplanationRenderer:
    """Class for rendering and combining Manim animation explanations."""

    def __init__(self, output_dir="output", print_response=False, use_visual_fix_code=False, scene_model=None):
        """Initialize the ExplanationRenderer.

        Args:
            output_dir (str, optional): Directory for output files. Defaults to "output".
            print_response (bool, optional): Whether to print responses. Defaults to False.
            use_visual_fix_code (bool, optional): Whether to use visual fix code. Defaults to False.
            scene_model: Optional model wrapper used to decide explanation-vs-image inputs for visual fix.
        """
        self.output_dir = output_dir
        self.print_response = print_response
        self.use_visual_fix_code = use_visual_fix_code
        self.scene_model = scene_model

    async def render_scene(self, code: str, file_prefix: str, curr_scene: int, curr_version: int, code_dir: str, media_dir: str, max_visual_retries: int = 3, use_visual_fix_code=False, visual_self_reflection_func=None, banned_reasonings=None, scene_trace_id=None, topic=None, session_id=None, implementation_plan: str = "", problem_image: Optional[Image.Image] = None):
        """Render a single scene and optionally apply visual fixes.

        Args:
            code (str): The Manim code to render
            file_prefix (str): Prefix for output files
            curr_scene (int): Current scene number
            curr_version (int): Current version number (managed by caller)
            code_dir (str): Directory for code files
            media_dir (str): Directory for media output
            max_visual_retries (int, optional): Maximum visual fix retry attempts. Defaults to 3.
            use_visual_fix_code (bool, optional): Whether to use visual fix code. Defaults to False.
            visual_self_reflection_func (callable, optional): Function for visual self-reflection. Defaults to None.
            banned_reasonings (list, optional): List of banned reasoning strings. Defaults to None.
            scene_trace_id (str, optional): Scene trace identifier. Defaults to None.
            topic (str, optional): Topic name. Defaults to None.
            session_id (str, optional): Session identifier. Defaults to None.
            implementation_plan (str, optional): Implementation plan for reference. Defaults to "".
            problem_image (Image.Image, optional): Original problem diagram for comparison. Defaults to None.

        Returns:
            tuple: (code, curr_version, error_message) where error_message is None on success
        """
        try:
            # Execute manim in a thread to prevent blocking
            file_path = os.path.join(code_dir, f"{file_prefix}_scene{curr_scene}_v{curr_version}.py")

            # Construct scene class name (e.g., Scene1, Scene2, etc.)
            scene_class_name = f"Scene{curr_scene}"

            result = await asyncio.to_thread(
                subprocess.run,
                ["manim", "-pql", "-s", file_path, scene_class_name, "--media_dir", media_dir, "--progress_bar", "none"],
                capture_output=True,
                text=True
            )

            # if result.returncode != 0, manim failed - return error immediately
            if result.returncode != 0:
                error_msg = result.stderr
                with open(os.path.join(code_dir, f"{file_prefix}_scene{curr_scene}_v{curr_version}_error.log"), "w") as f:
                    f.write(f"Manim render error (returncode={result.returncode}):\n{error_msg}\n")
                return code, curr_version, error_msg

            # returncode == 0 means success, even if there are warnings in stderr
            # Log warnings if present but don't treat them as errors
            if result.stderr and result.stderr.strip():
                with open(os.path.join(code_dir, f"{file_prefix}_scene{curr_scene}_v{curr_version}_warnings.log"), "w") as f:
                    f.write(f"Manim warnings (non-fatal):\n{result.stderr}\n")

            # Manim succeeded, optionally apply visual fixes
            if use_visual_fix_code and visual_self_reflection_func and banned_reasonings:
                visual_retries = 0
                while visual_retries < max_visual_retries:
                    # Find the PNG from the current version (the one we just rendered)
                    media_input = self._find_last_frame_png(media_dir, file_prefix, curr_scene, curr_version)

                    if not media_input:
                        print(f"Warning: Could not find rendered PNG for scene {curr_scene} v{curr_version}, skipping visual fix")
                        break

                    new_code, log = await visual_self_reflection_func(
                        code,
                        media_input,
                        scene_trace_id=scene_trace_id,
                        topic=topic,
                        scene_number=curr_scene,
                        session_id=session_id,
                        implementation=implementation_plan,
                        problem_image=problem_image
                    )

                    # Save visual fix log with current version number
                    with open(os.path.join(code_dir, f"{file_prefix}_scene{curr_scene}_v{curr_version}_vfix_log.txt"), "w") as f:
                        f.write(log)

                    # Validate new_code is not empty
                    if not new_code or not new_code.strip():
                        print(f"Visual fix returned empty code, stopping visual fixes")
                        break

                    # Check for termination markers (LGTM or banned reasonings)
                    if "<LGTM>" in log or any(word in log for word in banned_reasonings):
                        print(f"Visual fix completed for scene {curr_scene} v{curr_version} (LGTM)")
                        break

                    # If new_code is the same as old code, no need to continue
                    if new_code.strip() == code.strip():
                        print(f"Visual fix returned unchanged code, stopping visual fixes")
                        break

                    # Apply visual fix: increment version and save new code
                    curr_version += 1
                    code = new_code
                    new_file_path = os.path.join(code_dir, f"{file_prefix}_scene{curr_scene}_v{curr_version}.py")
                    with open(new_file_path, "w") as f:
                        f.write(code)
                    print(f"Visual fix applied, saved to v{curr_version}")

                    # Re-render with visually fixed code
                    result = await asyncio.to_thread(
                        subprocess.run,
                        ["manim", "-pql", "-s", new_file_path, scene_class_name, "--media_dir", media_dir, "--progress_bar", "none"],
                        capture_output=True,
                        text=True
                    )

                    if result.returncode != 0:
                        # Visual fix caused render failure, revert
                        print(f"Visual fix v{curr_version} caused render failure, reverting to v{curr_version - 1}")
                        error_msg = result.stderr
                        with open(os.path.join(code_dir, f"{file_prefix}_scene{curr_scene}_v{curr_version}_render_error.log"), "w") as f:
                            f.write(f"Visual fix render failed:\n{error_msg}\n")
                        # Revert to previous version
                        curr_version -= 1
                        # Reload previous working code
                        prev_file_path = os.path.join(code_dir, f"{file_prefix}_scene{curr_scene}_v{curr_version}.py")
                        with open(prev_file_path, "r") as f:
                            code = f.read()
                        break

                    # Log warnings if present
                    if result.stderr and result.stderr.strip():
                        with open(os.path.join(code_dir, f"{file_prefix}_scene{curr_scene}_v{curr_version}_warnings.log"), "w") as f:
                            f.write(f"Manim warnings (non-fatal):\n{result.stderr}\n")

                    print(f"Visual fix v{curr_version} rendered successfully")
                    visual_retries += 1
                    # Loop continues: next iteration will analyze the newly rendered version


            # Mark success
            print(f"Successfully rendered scene {curr_scene} v{curr_version}")
            with open(os.path.join(self.output_dir, file_prefix, f"scene{curr_scene}", "succ_rendered.txt"), "w") as f:
                f.write(f"v{curr_version}")

            return code, curr_version, None

        except Exception as e:
            error_msg = str(e)
            with open(os.path.join(code_dir, f"{file_prefix}_scene{curr_scene}_v{curr_version}_error.log"), "w") as f:
                f.write(f"Exception during render:\n{error_msg}\n")
            return code, curr_version, error_msg

    def _find_last_frame_png(self, media_dir: str, file_prefix: str, scene_number: int, version_number: int) -> Optional[str]:
        """Find last-frame PNG produced by `manim -s`.

        Expected location (as per your convention):
          {media_dir}/images/{file_prefix}_scene{scene_number}_v{version_number}/
        """
        img_dir = os.path.join(media_dir, "images", f"{file_prefix}_scene{scene_number}_v{version_number}")
        if not os.path.isdir(img_dir):
            return None

        pngs = [os.path.join(img_dir, f) for f in os.listdir(img_dir) if f.lower().endswith('.png')]
        if not pngs:
            return None

        pngs.sort(key=lambda p: os.path.getmtime(p), reverse=True)
        return pngs[0]

    def export_scene_png_to_doc(self, media_dir: str, file_prefix: str, scene_number: int, version_number: int) -> Optional[str]:
        """Copy the last-frame PNG into {output_dir}/{file_prefix}/doc for Markdown embedding."""
        src = self._find_last_frame_png(media_dir, file_prefix, scene_number, version_number)
        if not src:
            return None

        dst_dir = os.path.join(self.output_dir, file_prefix, "doc")
        os.makedirs(dst_dir, exist_ok=True)
        dst = os.path.join(dst_dir, f"scene{scene_number}.png")

        with Image.open(src) as img:
            img.save(dst, 'PNG', optimize=True)

        return dst

    def run_manim_process(self,
                          topic: str):
        """Run manim on all generated manim code for a specific topic.

        Args:
            topic (str): Topic name to process

        Returns:
            subprocess.CompletedProcess: Result of the final manim process
        """
        file_prefix = topic.lower()
        file_prefix = re.sub(r'[^a-z0-9_]+', '_', file_prefix)
        search_path = os.path.join(self.output_dir, file_prefix)
        # Iterate through scene folders
        scene_folders = [f for f in os.listdir(search_path) if os.path.isdir(os.path.join(search_path, f))]
        scene_folders.sort()  # Sort to process scenes in order

        for folder in scene_folders:
            folder_path = os.path.join(search_path, folder)

            # Get all Python files in version order
            py_files = [f for f in os.listdir(folder_path) if f.endswith('.py')]
            py_files.sort(key=lambda x: int(x.split('_v')[-1].split('.')[0]))  # Sort by version number

            for file in py_files:
                file_path = os.path.join(folder_path, file)
                try:
                    media_dir = os.path.join(self.output_dir, file_prefix, "media")
                    result = subprocess.run(
                        f"manim -qh {file_path} --media_dir {media_dir}",
                        shell=True,
                        capture_output=True,
                        text=True
                    )
                    if result.returncode != 0:
                        raise Exception(result.stderr)
                    print(f"Successfully rendered {file}")
                    break  # Move to next scene folder if successful
                except Exception as e:
                    print(f"Error rendering {file}: {e}")
                    error_log_path = os.path.join(folder_path, f"{file.split('.')[0]}_error.log") # drop the extra py
                    with open(error_log_path, "w") as f:
                        f.write(f"Error:\n{str(e)}\n")
                    print(f"Error log saved to {error_log_path}")
        return result

    def create_snapshot_scene(self, topic: str, scene_number: int, version_number: int, return_type: str = "image"):
        """Create a snapshot of the explanation for a specific topic and scene.

        Args:
            topic (str): Topic name
            scene_number (int): Scene number
            version_number (int): Version number
            return_type (str, optional): Type of return value - "path" or "image". Defaults to "image".

        Returns:
            Union[str, PIL.Image]: Path to saved image or PIL Image object

        Raises:
            FileNotFoundError: If no mp4 files found in explanation folder
        """
        file_prefix = topic.lower()
        file_prefix = re.sub(r'[^a-z0-9_]+', '_', file_prefix)
        search_path = os.path.join(self.output_dir, file_prefix)
        explanation_folder_path = os.path.join(search_path, "media", "explanations", f"{file_prefix}_scene{scene_number}_v{version_number}", "1080p60")
        os.makedirs(explanation_folder_path, exist_ok=True)
        snapshot_path = os.path.join(explanation_folder_path, "snapshot.png")
        # Get the mp4 explanation file from the explanation folder path
        explanation_files = [f for f in os.listdir(explanation_folder_path) if f.endswith('.mp4')]
        if not explanation_files:
            raise FileNotFoundError(f"No mp4 files found in {explanation_folder_path}")
        video_path = os.path.join(explanation_folder_path, explanation_files[0])
        saved_image = image_with_most_non_black_space(get_images_from_explanation(video_path), snapshot_path, return_type=return_type)
        return saved_image

    def combine_explanations(self, topic: str):
        """Combine all explanations and subtitle files for a specific topic using ffmpeg.

        Args:
            topic (str): Topic name to combine explanations for

        This function will:
        - Find all scene explanations and subtitles
        - Combine explanations with or without audio
        - Merge subtitle files with correct timing
        - Save combined explanation and subtitles to output directory
        """
        file_prefix = topic.lower()
        file_prefix = re.sub(r'[^a-z0-9_]+', '_', file_prefix)
        search_path = os.path.join(self.output_dir, file_prefix, "media", "explanations")

        # Create output directory if it doesn't exist
        explanation_output_dir = os.path.join(self.output_dir, file_prefix)
        os.makedirs(explanation_output_dir, exist_ok=True)

        output_video_path = os.path.join(explanation_output_dir, f"{file_prefix}_combined.mp4")
        output_srt_path = os.path.join(explanation_output_dir, f"{file_prefix}_combined.srt")
        
        if os.path.exists(output_video_path) and os.path.exists(output_srt_path):
            print(f"Combined explanation and subtitles already exist at {output_video_path}, not combining again.")
            return

        # Get scene count from outline
        scene_outline_path = os.path.join(self.output_dir, file_prefix, f"{file_prefix}_scene_outline.txt")
        if not os.path.exists(scene_outline_path):
            print(f"Warning: Scene outline file not found at {scene_outline_path}. Cannot determine scene count.")
            return
        with open(scene_outline_path) as f:
            plan = f.read()
        scene_outline = re.search(r'(<SCENE_OUTLINE>.*?</SCENE_OUTLINE>)', plan, re.DOTALL).group(1)
        scene_count = len(re.findall(r'<SCENE_(\d+)>[^<]', scene_outline))

        # Find all scene folders and explanations
        scene_folders = []
        for root, dirs, files in os.walk(search_path):
            for dir in dirs:
                if dir.startswith(file_prefix + "_scene"):
                    scene_folders.append(os.path.join(root, dir))

        scene_explanations = []
        scene_subtitles = []

        for scene_num in range(1, scene_count + 1):
            folders = [f for f in scene_folders if int(f.split("scene")[-1].split("_")[0]) == scene_num]
            if not folders:
                print(f"Warning: Missing scene {scene_num}")
                continue

            folders.sort(key=lambda f: int(f.split("_v")[-1]))
            folder = folders[-1]

            explanation_found = False
            subtitles_found = False
            for filename in os.listdir(os.path.join(folder, "1080p60")):
                if filename.endswith('.mp4'):
                    scene_explanations.append(os.path.join(folder, "1080p60", filename))
                    explanation_found = True
                elif filename.endswith('.srt'):
                    scene_subtitles.append(os.path.join(folder, "1080p60", filename))
                    subtitles_found = True

            if not explanation_found:
                print(f"Warning: Missing explanation for scene {scene_num}")
            if not subtitles_found:
                scene_subtitles.append(None)

        if len(scene_explanations) != scene_count:
            print("Not all explanations/subtitles are found, aborting explanation combination.")
            return

        try:
            import ffmpeg # You might need to install ffmpeg-python package: pip install ffmpeg-python
            from tqdm import tqdm

            print("Analyzing explanation streams...")
            # Check if explanations have audio streams
            has_audio = []
            for explanation in tqdm(scene_explanations, desc="Checking audio streams"):
                probe = ffmpeg.probe(explanation)
                audio_streams = [stream for stream in probe['streams'] if stream['codec_type'] == 'audio']
                has_audio.append(len(audio_streams) > 0)

            print("Preparing explanation combination...")
            # If any explanation has audio, we need to ensure all explanations have audio streams
            if any(has_audio):
                # Create list to store explanation and audio streams
                streams = []
                for explanation, has_aud in tqdm(list(zip(scene_explanations, has_audio)), desc="Processing explanations"):
                    if has_aud:
                        # Explanation has audio, use as is
                        input_vid = ffmpeg.input(explanation)
                        streams.extend([input_vid['v'], input_vid['a']])
                    else:
                        # Explanation lacks audio, add silent audio
                        input_vid = ffmpeg.input(explanation)
                        # Generate silent audio for the duration of the explanation
                        probe = ffmpeg.probe(explanation)
                        duration = float(probe['streams'][0]['duration'])
                        silent_audio = ffmpeg.input(f'anullsrc=channel_layout=stereo:sample_rate=44100',
                                                  f='lavfi', t=duration)['a']
                        streams.extend([input_vid['v'], silent_audio])
                    
                print("Combining explanations with audio...")
                try:
                    # Concatenate all streams using optimized CPU encoding settings
                    concat = ffmpeg.concat(*streams, v=1, a=1, unsafe=True)
                    process = (
                        concat
                        .output(output_video_path,
                               **{'c:v': 'libx264',
                                  'c:a': 'aac',
                                  'preset': 'veryfast',    # Changed from ultrafast for better speed/quality balance
                                  'crf': '28',             # Same quality setting
                                  'threads': '0',          # Use all CPU threads
                                  'tune': 'fastdecode',    # Optimize for decoding speed
                                  'profile:v': 'baseline', # Simpler profile for faster encoding
                                  'level': '4.0',
                                  'x264-params': 'aq-mode=0:no-deblock:no-cabac:ref=1:subme=0:trellis=0:weightp=0',  # Added aggressive speed optimizations
                                  'movflags': '+faststart',
                                  'stats': None,
                                  'progress': 'pipe:1'})
                        .overwrite_output()
                        .run_async(pipe_stdout=True, pipe_stderr=True)
                    )
                    
                    # Process progress output
                    while True:
                        line = process.stdout.readline().decode('utf-8')
                        if not line:
                            break
                        if 'frame=' in line:
                            sys.stdout.write('\rProcessing: ' + line.strip())
                            sys.stdout.flush()
                    
                    # Wait for the process to complete and capture output
                    stdout, stderr = process.communicate()
                    print("\nEncoding complete!")
                    
                except ffmpeg.Error as e:
                    print(f"FFmpeg stdout:\n{e.stdout.decode('utf8')}")
                    print(f"FFmpeg stderr:\n{e.stderr.decode('utf8')}")
                    raise
            else:
                # No explanations have audio, concatenate explanation streams only
                streams = []
                for explanation in tqdm(scene_explanations, desc="Processing explanations"):
                    streams.append(ffmpeg.input(explanation)['v'])
                
                print("Combining explanations without audio...")
                try:
                    concat = ffmpeg.concat(*streams, v=1, unsafe=True)
                    process = (
                        concat
                        .output(output_video_path,
                               **{'c:v': 'libx264',
                                  'preset': 'medium',
                                  'crf': '23',
                                  'stats': None,  # Enable progress stats
                                  'progress': 'pipe:1'})  # Output progress to pipe
                        .overwrite_output()
                        .run_async(pipe_stdout=True, pipe_stderr=True)
                    )
                    
                    # Process progress output
                    while True:
                        line = process.stdout.readline().decode('utf-8')
                        if not line:
                            break
                        if 'frame=' in line:
                            sys.stdout.write('\rProcessing: ' + line.strip())
                            sys.stdout.flush()
                    
                    # Wait for the process to complete and capture output
                    stdout, stderr = process.communicate()
                    print("\nEncoding complete!")
                    
                except ffmpeg.Error as e:
                    print(f"FFmpeg stdout:\n{e.stdout.decode('utf8')}")
                    print(f"FFmpeg stderr:\n{e.stderr.decode('utf8')}")
                    raise
            
            print(f"Successfully combined explanations into {output_video_path}")

            # Handle subtitle combination (existing subtitle code remains the same)
            if scene_subtitles:
                with open(output_srt_path, 'w', encoding='utf-8') as outfile:
                    current_time_offset = 0
                    subtitle_index = 1

                    for srt_file, explanation_file in zip(scene_subtitles, scene_explanations):
                        if srt_file is None:
                            continue

                        with open(srt_file, 'r', encoding='utf-8') as infile:
                            lines = infile.readlines()
                            i = 0
                            while i < len(lines):
                                line = lines[i].strip()
                                if line.isdigit():  # Subtitle index
                                    outfile.write(f"{subtitle_index}\n")
                                    subtitle_index += 1
                                    i += 1

                                    # Time codes line
                                    time_line = lines[i].strip()
                                    start_time, end_time = time_line.split(' --> ')

                                    # Convert time codes and add offset
                                    def adjust_time(time_str, offset):
                                        h, m, s = time_str.replace(',', '.').split(':')
                                        total_seconds = float(h) * 3600 + float(m) * 60 + float(s) + offset
                                        h = int(total_seconds // 3600)
                                        m = int((total_seconds % 3600) // 60)
                                        s = total_seconds % 60
                                        return f"{h:02d}:{m:02d}:{s:06.3f}".replace('.', ',')

                                    new_start = adjust_time(start_time, current_time_offset)
                                    new_end = adjust_time(end_time, current_time_offset)
                                    outfile.write(f"{new_start} --> {new_end}\n")
                                    i += 1

                                    # Subtitle text (could be multiple lines)
                                    while i < len(lines) and lines[i].strip():
                                        outfile.write(lines[i])
                                        i += 1
                                    outfile.write('\n')
                                else:
                                    i += 1

                        # Update time offset using ffprobe
                        probe = ffmpeg.probe(explanation_file)
                        duration = float(probe['streams'][0]['duration'])
                        current_time_offset += duration

            print(f"Successfully combined explanations into {output_video_path}")
            if scene_subtitles:
                print(f"Successfully combined subtitles into {output_srt_path}")

        except Exception as e:
            print(f"Error combining explanations and subtitles: {e}")
            traceback.print_exc()
