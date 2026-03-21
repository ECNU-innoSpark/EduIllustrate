#!/usr/bin/env python3
"""
Convert solution.md files to HTML pages for GitHub Pages
"""

import os
import re
from pathlib import Path

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
            padding: 2rem;
        }}

        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            padding: 3rem;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}

        .back-link {{
            display: inline-block;
            margin-bottom: 2rem;
            color: #667eea;
            text-decoration: none;
            font-weight: 500;
        }}

        .back-link:hover {{
            text-decoration: underline;
        }}

        h1 {{
            color: #667eea;
            margin-bottom: 2rem;
            font-size: 2rem;
            border-bottom: 3px solid #667eea;
            padding-bottom: 0.5rem;
        }}

        h2 {{
            color: #764ba2;
            margin-top: 2rem;
            margin-bottom: 1rem;
            font-size: 1.5rem;
        }}

        h3 {{
            color: #555;
            margin-top: 1.5rem;
            margin-bottom: 0.75rem;
        }}

        p {{
            margin-bottom: 1rem;
        }}

        strong {{
            color: #444;
        }}

        img {{
            max-width: 100%;
            height: auto;
            display: block;
            margin: 2rem auto;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}

        ul, ol {{
            margin-left: 2rem;
            margin-bottom: 1rem;
        }}

        li {{
            margin-bottom: 0.5rem;
        }}

        .mjx-math {{
            font-size: 1.1em;
        }}

        .problem-statement {{
            background: #f8f9fa;
            padding: 1.5rem;
            border-left: 4px solid #667eea;
            margin: 1.5rem 0;
        }}

        .options {{
            background: #fff3cd;
            padding: 1rem;
            border-radius: 4px;
            margin: 1rem 0;
        }}

        .conclusion {{
            background: #d4edda;
            padding: 1.5rem;
            border-left: 4px solid #28a745;
            margin: 1.5rem 0;
        }}

        .verification {{
            background: #e7f3ff;
            padding: 1rem;
            border-radius: 4px;
            margin: 1rem 0;
        }}

        code {{
            background: #f4f4f4;
            padding: 0.2rem 0.4rem;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }}
    </style>
</head>
<body>
    <div class="container">
        <a href="../../index.html" class="back-link">← Back to Examples</a>
        {content}
    </div>
</body>
</html>
"""

def markdown_to_html(md_text):
    """Convert markdown to HTML with basic formatting"""
    html = md_text

    # Convert headers
    html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^\*\*(.*?):\*\*$', r'<h2>\1</h2>', html, flags=re.MULTILINE)

    # Convert images
    html = re.sub(r'!\[\]\((.*?)\)', r'<img src="\1" alt="Diagram">', html)

    # Convert inline math $...$ to \(...\) for MathJax
    html = re.sub(r'\$\$(.+?)\$\$', r'\\[\1\\]', html)
    html = re.sub(r'\$(.+?)\$', r'\\(\1\\)', html)

    # Convert bold
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)

    # Convert list items
    html = re.sub(r'^- (.*?)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    html = re.sub(r'^([A-D])\. (.*?)$', r'<li><strong>\1.</strong> \2</li>', html, flags=re.MULTILINE)

    # Wrap consecutive <li> in <ul>
    html = re.sub(r'(<li>.*?</li>)\n(?!<li>)', r'<ul>\1</ul>\n', html, flags=re.DOTALL)
    html = re.sub(r'(<li>.*?</li>)\n(<li>)', r'\1\2', html, flags=re.DOTALL)
    html = re.sub(r'(<ul>.*?</ul>)', r'\1', html, flags=re.DOTALL)

    # Wrap text in paragraphs
    lines = html.split('\n')
    new_lines = []
    in_para = False

    for line in lines:
        stripped = line.strip()
        if not stripped:
            if in_para:
                new_lines.append('</p>')
                in_para = False
            new_lines.append(line)
        elif stripped.startswith('<'):
            if in_para:
                new_lines.append('</p>')
                in_para = False
            new_lines.append(line)
        else:
            if not in_para:
                new_lines.append('<p>')
                in_para = True
            new_lines.append(line)

    if in_para:
        new_lines.append('</p>')

    html = '\n'.join(new_lines)

    # Add special styling classes
    html = re.sub(r'<h2>Problem Statement</h2>(.*?)(?=<h2>|$)',
                  r'<h2>Problem Statement</h2><div class="problem-statement">\1</div>',
                  html, flags=re.DOTALL)
    html = re.sub(r'<h2>Options</h2>(.*?)(?=<h2>|$)',
                  r'<h2>Options</h2><div class="options">\1</div>',
                  html, flags=re.DOTALL)
    html = re.sub(r'<h2>Conclusion</h2>(.*?)(?=<h2>|$)',
                  r'<h2>Conclusion</h2><div class="conclusion">\1</div>',
                  html, flags=re.DOTALL)
    html = re.sub(r'<h2>Verification</h2>(.*?)(?=<h2>|$)',
                  r'<h2>Verification</h2><div class="verification">\1</div>',
                  html, flags=re.DOTALL)

    return html

def process_example_folder(folder_path):
    """Process a single example folder"""
    solution_md = folder_path / 'solution.md'
    if not solution_md.exists():
        print(f"Skipping {folder_path.name}: no solution.md found")
        return

    # Read markdown
    with open(solution_md, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Extract title from first line
    title_match = re.match(r'^# (.+)$', md_content, re.MULTILINE)
    title = title_match.group(1) if title_match else folder_path.name

    # Convert to HTML
    html_content = markdown_to_html(md_content)

    # Apply template
    full_html = HTML_TEMPLATE.format(title=title, content=html_content)

    # Write HTML file
    solution_html = folder_path / 'solution.html'
    with open(solution_html, 'w', encoding='utf-8') as f:
        f.write(full_html)

    print(f"Generated {solution_html}")

def main():
    examples_dir = Path('examples')

    if not examples_dir.exists():
        print("Error: examples directory not found")
        return

    # Process each example folder
    for folder in examples_dir.iterdir():
        if folder.is_dir():
            process_example_folder(folder)

    print("\nAll HTML files generated successfully!")

if __name__ == '__main__':
    main()
