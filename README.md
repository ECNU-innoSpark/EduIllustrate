# EduIllustrate: Diagram-Rich K-12 STEM Explanations

This is the GitHub Pages website for the EduIllustrate project.

## About

EduIllustrate is an automated four-stage agentic pipeline that generates diagram-rich explanations for K-12 STEM problems with programmatically rendered static diagrams via Manim.

## Website Structure

- `index.html` - Main landing page with paper abstract and links to examples
- `paper/` - Paper PDF and figures
- `examples/` - Generated problem solutions with diagrams
- `generate_html.py` - Script to convert markdown solutions to HTML

## Viewing the Website

Visit: https://[your-username].github.io/[repo-name]/

## Paper

[Download PDF](paper/EduIllustrate.pdf)

## Example Solutions

The website showcases 9 example problem solutions spanning different grade levels and mathematical concepts, each with:
- Step-by-step explanations
- Geometrically accurate diagrams
- Mathematical formulas rendered with MathJax

## Building

To regenerate HTML from markdown:

```bash
python3 generate_html.py
```

## License

[Add your license information here]
