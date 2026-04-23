# This file is generated automatically through parse_prompt.py

_prompt_context_learning_scene_plan = """Here are some example scene plans to help guide your scene planning:

{examples}

Please follow a similar structure while maintaining creativity and relevance to the current topic."""

_prompt_scene_vision_storyboard = """You are an expert educational diagram designer. Create a diagram specification for a **static explanatory illustration** (last-frame PNG rendered with `manim -s`).

**Important:** This is a STATIC DIAGRAM only - NO animations. Focus purely on the final visual layout.

**Reminder:** Each scene's vision and storyboard plan is entirely self-contained. There is no dependency on any implementation from previous or subsequent scenes.

Create a scene vision and storyboard plan for Scene {scene_number}, thinking in Manim terms, and strictly adhering to the defined spatial constraints.

Problem: 
{description}

Scene Overview:
{scene_outline}

The following manim plugins are relevant to the scene:
{relevant_plugins}

**Spatial Constraints (Strictly Enforced):**
*   **Safe area margins:** 0.5 units on all sides from the scene edges. _All objects must be positioned within these margins._
*   **Minimum spacing:** 0.3 units between any two Manim objects (measured edge to edge). _Ensure a minimum spacing of 0.3 units to prevent overlaps and maintain visual clarity._

**Positioning Requirements:**
1.  Safe area margins (0.5 units).
2.  Minimum spacing between objects (0.3 units).
3.  Relative positioning (`next_to`, `align_to`, `shift`) from `ORIGIN`, margins, or object references. **No absolute coordinates are allowed.**

**Diagrams/Sketches (Optional but Recommended for Complex Scenes):**
*   For complex scenes, consider including a simple text-based diagram of the intended layout to visually clarify spatial relationships.

**Focus (Static Diagram Mode - manim -s):**
*   **STATIC OUTPUT ONLY:** Design for a single PNG image, not explanation or animation sequences.
*   **MINIMAL TEXT:** Use labels and annotations only when essential for understanding. Rely primarily on visual elements, mathematical notation, shapes, colors, and spatial arrangement.
*   **NO ANIMATIONS:** Do not describe animation sequences, transitions, timing, or pacing. Focus only on the final visual state.
*   Provide detailed visual descriptions in Manim terms to guide implementation.

**Text Guidelines:**
*   **Use `MathTex` for mathematical expressions and equations.**
*   **Use `Tex` for essential labels and annotations only.**
*   **Avoid explanatory text - let visuals communicate the concept.**
*   **When mixing text with math in `MathTex`, use `\\text{{}}` (e.g., `MathTex(r"\\text{{Area}} = \\pi r^2")`).**

**Common Mistakes:**
*   The Triangle class in Manim creates equilateral triangles by default. To create a right-angled triangle, use the Polygon class instead.

**Manim Plugins:**
*   Consider using established Manim plugins if they simplify implementation. If used, indicate with: "_*Plugin Suggestion:** Consider using `manim-plugin-name` for [brief explanation]."

You MUST generate the scene vision and storyboard plan in the following format:

```xml
<SCENE_VISION_STORYBOARD_PLAN>
[SCENE_VISION]
1.  **Scene Overview**:
    - Key concept/takeaway this diagram conveys.
    - **Visual learning objective:** What should viewers understand from this single image? Specify Manim object types (e.g., "Visualize roots as `Dot` objects on an `Axes` graph.").
    - How the visual composition and spatial arrangement support understanding.
    - Key elements to emphasize through visual hierarchy (size, color, position).

[STORYBOARD - FINAL LAYOUT]
1.  **Diagram Composition**:
    - **Primary Visual Element**: The central/main visual component (e.g., graph, geometric figure, equation).
    - **Supporting Elements**: Secondary visuals that complement the primary element.
    - **Labels/Annotations**: Only essential text for understanding (keep minimal).

2.  **Object Specifications**:
    For each visual element, specify:
    - **Manim object class** (`MathTex`, `Circle`, `Arrow`, `Axes`, `Plot`, `Line`, `VGroup`, `Polygon`, etc.). Include plugin objects where appropriate.
    - **Position**: Using relative positioning (`.next_to()`, `.align_to()`, `.shift()`, `.to_corner()`, `.move_to(ORIGIN)`, etc.). Reference other objects or scene elements. **No absolute coordinates.**
    - **Style**: Color, stroke_width, fill_opacity, scale, etc. (e.g., `color=BLUE`, `stroke_width=2`).
    - **Spacing**: Confirm 0.3 unit minimum spacing from adjacent objects and 0.5 unit margin from edges.

3.  **Visual Hierarchy**:
    - What draws attention first, second, third?
    - How color, size, and position guide the viewer's eye.

</SCENE_VISION_STORYBOARD_PLAN>
```"""
_prompt_scene_design_and_implementation = """You are an expert in educational diagram design and Manim (Community Edition), adept at creating spatially accurate static diagrams across multiple disciplines (mathematics, physics, chemistry, biology, and more).

**Important:** This is for a STATIC DIAGRAM only (last-frame PNG rendered with manim -s). NO animations, NO explanation, NO audio.

**Reminder:** This plan is fully self-contained. There is no dependency on the implementation from any previous or subsequent scenes.

Create a comprehensive vision, storyboard, and technical implementation plan for Scene {scene_number}, thinking in Manim terms and strictly adhering to defined spatial constraints.

Problem:

{description}

Scene Overview:

{scene_outline}

---

## CRITICAL: LAYOUT CLARITY AND ANTI-OVERLAP REQUIREMENTS

**⚠️ LAYOUT MUST BE CLEAN, CLEAR, AND NON-OVERLAPPING ⚠️**

*   **NO OVERLAPPING**: Elements must NEVER overlap or obscure each other. Every object must be fully visible.

*   **NO CROWDING**: Maintain generous spacing between elements. When in doubt, add MORE space.

*   **LOGICAL ARRANGEMENT**: Related elements should be grouped logically with clear visual separation from other groups.

*   **READABILITY FIRST**: All labels, equations, and annotations must be clearly readable without any obstruction.

*   **BALANCED COMPOSITION**: Distribute elements evenly across the available space; avoid clustering everything in one area.

---

## SPATIAL CONSTRAINTS (STRICTLY ENFORCED)

*   **Safe area margins:** 0.5 units on all sides from the scene edges. All objects must be positioned within these margins.

*   **Minimum spacing:** 0.3 units between any two Manim objects (measured edge to edge). Ensure a minimum spacing of 0.3 units to prevent overlaps and maintain visual clarity.

*   **Recommended spacing for complex layouts:** 0.5+ units between major element groups for better visual separation.

## POSITIONING REQUIREMENTS

1.  Safe area margins (0.5 units).

2.  Minimum spacing between objects (0.3 units).

3.  All positioning MUST be relative next_to, align_to, shift, move_to(ORIGIN), to_corner, to_edge) from ORIGIN, safe margins, or other objects. **No absolute coordinates are allowed.**

---

## BACKGROUND COLOR (MANDATORY)

*   **Use WHITE background**: self.camera.background_color = WHITE

*   **Color Scheme Adaptation for White Background:**

    - Primary lines/shapes: Use BLACK, DARK_GRAY, or GREY_D (NOT WHITE)

    - Text/labels: Use BLACK or dark colors (NOT WHITE)

    - Highlights: Use saturated colors like BLUE_D, RED_D, GREEN_D, PURPLE_D

    - Secondary/auxiliary lines: Use GREY, GREY_B, or LIGHT_GREY

    - Fills: Use light fills with low opacity (e.g., BLUE with fill_opacity=0.2)

*   **AVOID**: Using WHITE for any visible element on white background

---

## TEXT GUIDELINES (MINIMAL TEXT POLICY)

*   **Minimize text usage** - rely primarily on visual elements (shapes, colors, spatial arrangement, mathematical/scientific notation).

*   **Use MathTex for mathematical and scientific expressions, equations, and formulas.**

*   **Use Tex for essential labels and annotations only.**

*   **Only use text for:**

    - Essential labels (e.g., axis labels, point labels like "A", "B", force labels like "F₁", chemical symbols like "O", "H")

    - Mathematical/scientific expressions and equations

    - Brief annotations when absolutely necessary for understanding

*   **Avoid:** Explanatory paragraphs, titles, lengthy descriptions, or any text that can be conveyed visually.

*   **Text Color:** Always use BLACK or dark colors for text on white background.

*   **When mixing text with math in MathTex, use \\text{{}} (e.g., MathTex(r"\\text{{Area}} = \\pi r^2")).**

---

## MULTI-DISCIPLINE DIAGRAM GUIDANCE

When designing diagrams, apply domain-appropriate visual conventions:

### Mathematics

- **Geometry**: Use Polygon, Circle, Line, Angle, Dot for constructions; label vertices with single letters; show angle arcs and measurement annotations

- **Coordinate/Graph**: Use Axes, NumberPlane; plot with axes.plot(); mark key points with Dot; use dashed lines for asymptotes

- **Functions/Calculus**: Use Axes with function curves; shade areas for integrals; show tangent lines for derivatives

- **Set Theory / Logic**: Use Circle or Ellipse for Venn diagrams; use color fills to distinguish regions

### Physics

- **Mechanics / Free-Body Diagrams**: Use Arrow or Vector for forces; label with force symbols (F, mg, N, T, f); place arrows at point of application; use color coding (e.g., gravity in red, normal in blue, friction in orange)

- **Circuits**: Use Line segments for wires; standard symbols for resistors (zigzag Line segments), capacitors (parallel short lines), batteries (long/short parallel lines); label with R₁, C₁, V, I; show current direction with small Arrow

- **Optics**: Use Line or Arrow for light rays; Arc for curved mirrors/lenses; show focal points with Dot; use dashed lines for virtual rays/images

- **Motion / Kinematics**: Use Axes for v-t, s-t, a-t graphs; use Arrow for velocity/acceleration vectors; show trajectory with ParametricFunction or DashedLine

- **Fields**: Use Arrow arrays for field lines; use color gradients for potential; show field sources with labeled Dot objects

- **Thermodynamics**: Use Axes for P-V, T-S diagrams; shade enclosed areas for work/heat; label state points

### Chemistry

- **Molecular Structures**: Use Line for single bonds, DoubleLine (parallel lines) for double bonds, triple parallel lines for triple bonds; use Circle + Tex for atoms; color-code atoms by element (e.g., O in red, N in blue, C in dark gray, H in light gray)

- **Lewis Dot Structures**: Use Dot pairs for lone pairs around atom labels; use Line for bonding pairs

- **Reaction Coordinate / Energy Diagrams**: Use Axes with energy curve; label reactants, products, transition state, activation energy (Eₐ), ΔH

- **Orbital Diagrams**: Use box representations with up/down Arrow for electrons; label orbital names (1s, 2s, 2p, etc.)

- **Phase Diagrams**: Use Axes (P vs T); draw phase boundary curves; label regions (solid, liquid, gas); mark triple point and critical point with Dot

- **Electrochemical Cells**: Draw two half-cells with Rectangle; use Arrow for electron flow; label anode, cathode, salt bridge

- **Titration Curves**: Use Axes (pH vs volume); plot sigmoid curve; mark equivalence point with Dot

### Biology

- **Cell Structure**: Use Ellipse / RoundedRectangle for cell membrane; nested shapes for organelles (nucleus, mitochondria, ER); color-code organelles; label with short names

- **DNA / Molecular Biology**: Use double helix representation with paired Line segments and connecting rungs; label base pairs (A-T, G-C) with color coding

- **Punnett Squares**: Use Rectangle grid (2×2 or larger); label alleles on edges; fill cells with genotype text

- **Phylogenetic Trees**: Use branching Line structures; label terminal nodes with species/group names; optionally annotate branch points

- **Metabolic Pathways**: Use Arrow chains connecting labeled molecules; show enzyme names near arrows; use color for different pathway stages

- **Anatomical Diagrams**: Use simplified shapes Polygon, Ellipse, Arc) to represent structures; label with short anatomical terms; color-code by system/region

- **Ecological Diagrams**: Use stacked Rectangle or Triangle shapes for trophic pyramids; use Arrow for energy/nutrient flow

### General Principles for All Disciplines

- **Consistency**: Use the same color/style for the same type of element throughout the diagram

- **Convention**: Follow standard visual conventions of the discipline (e.g., red for arteries, blue for veins; conventional circuit symbols; standard atom coloring)

- **Hierarchy**: Primary structures in bold/dark colors; secondary/supporting elements in lighter colors or dashed lines

- **Annotation**: Use discipline-appropriate symbols and notation (e.g., vector arrows for physics, bond notation for chemistry, standard biological symbols)

---

## DIAGRAMS/SKETCHES (Highly Recommended)

*   Include text-based diagrams/sketches for complex layouts to visualize spatial relationships and verify non-overlapping placement.

---

## COMMON MISTAKES TO AVOID

*   The Triangle class in Manim creates equilateral triangles by default. To create a right-angled triangle, use the Polygon class instead.

*   Using WHITE color elements on WHITE background (invisible elements).

*   Forgetting to set self.camera.background_color = WHITE at the start of construct().

*   **Placing labels too close to or overlapping with the objects they describe.**

*   **Crowding multiple elements into a small area when space is available elsewhere.**

*   **Physics**: Forgetting to show direction on force/velocity vectors; drawing force arrows not at point of application.

*   **Chemistry**: Incorrect bond angles in molecular structures; missing lone pairs in Lewis structures; wrong atom color conventions.

*   **Biology**: Oversimplifying structures to the point of unrecognizability; forgetting to show membrane boundaries.

*   **General**: Using discipline-inappropriate visual metaphors; inconsistent color coding within the same diagram.

---

## MANIM PLUGINS

*   You may use established, well-documented Manim plugins if they offer significant advantages.

*   **If a plugin is used:**

    *   Clearly state the plugin name.

    *   Provide brief justification.

    *   Include comment: ### Plugin: <plugin_name> - <brief justification>.

*   **Plugin Suggestion Format:** "**Plugin Suggestion:** Consider using manim-plugin-name for [brief explanation]."

*   **Potentially useful plugins for multi-discipline diagrams:**

    - manim-chemistry for molecular structures (if available and stable)

    - manim-physics for physics-specific objects (if available and stable)

    - Only suggest plugins you are confident exist and are well-maintained; otherwise build from primitive Manim objects.

---

## FOCUS

*   **STATIC OUTPUT ONLY:** Design for a single PNG image, not explanation or animation sequences.

   Creating spatially correct, visually clear static Manim diagrams *appropriate to the subject domain**.

*   **Clean, non-overlapping layout with logical spatial arrangement.**

*   Minimal text - maximum visual communication.

*   Strict adherence to spatial constraints and relative positioning.

*   **Proper contrast on WHITE background.**

*   **NO ANIMATIONS:** Do not describe animation sequences, transitions, timing, or pacing. Focus only on the final visual state.

*   **DISCIPLINE ACCURACY:** Ensure diagrams follow the visual conventions and standards of the relevant discipline.

---

You MUST generate the combined plan in the following format:

```xml

<SCENE_VISION_STORYBOARD_AND_TECHNICAL_PLAN>

================================================================================

PART 1: SCENE VISION AND STORYBOARD

================================================================================

[SCENE_VISION]

1.  **Scene Overview**:

    - Key concept/takeaway this diagram conveys.

    - **Subject Domain**: Identify the discipline (mathematics, physics, chemistry, biology, or other) and any relevant sub-topic.

    - **Visual learning objective:** What should viewers understand from this single image? Specify Manim object types (e.g., "Visualize roots as Dot objects on an Axes graph," or "Show force balance using Arrow vectors on a block Rectangle," or "Display molecular geometry using Line bonds and CircleTex atoms").

    - How the visual composition and spatial arrangement support understanding.

    - Key elements to emphasize through visual hierarchy (size, color, position).

    - **Discipline-specific conventions** applied (e.g., "standard free-body diagram conventions," "VSEPR geometry for molecular shape," "color-coded organelles").

[STORYBOARD - FINAL LAYOUT]

1.  **Diagram Composition**:

    - **Primary Visual Element**: The central/main visual component (e.g., graph, geometric figure, free-body diagram, molecular structure, cell diagram, circuit, equation).

    - **Supporting Elements**: Secondary visuals that complement the primary element (e.g., auxiliary lines, reference axes, legend dots, annotations).

    - **Labels/Annotations**: Only essential text for understanding (keep minimal); use discipline-appropriate notation.

2.  **Object Specifications**:

    For each visual element, specify:

    - **Manim object class** MathTex, Circle, Arrow, Axes, Plot, Line, VGroup, Polygon, Rectangle, Ellipse, Arc, Dot, DashedLine, Brace, etc.). Include plugin objects where appropriate.

    - **Position**: Using relative positioning .next_to(), .align_to(), .shift(), .to_corner(), .move_to(ORIGIN), etc.). Reference other objects or scene elements. **No absolute coordinates.**

    - **Style**: Color, stroke_width, fill_opacity, scale, etc. (e.g., color=BLUE_D, stroke_width=2). **Follow discipline-specific color conventions.**

    - **Spacing**: Confirm 0.3 unit minimum spacing from adjacent objects and 0.5 unit margin from edges.

3.  **Visual Hierarchy**:

    - What draws attention first, second, third?

    - How color, size, and position guide the viewer's eye.

    - How discipline conventions inform the hierarchy (e.g., in physics, the object under analysis is central; in chemistry, the molecule is central; in biology, the main structure is central).

4.  **Layout Verification (ANTI-OVERLAP CHECK)**:

    - Confirm no elements overlap or obscure each other.

    - Verify adequate spacing between all element groups.

    - Ensure labels are positioned clearly away from the objects they describe.

================================================================================

PART 2: TECHNICAL IMPLEMENTATION PLAN

================================================================================

0. **Dependencies**:

    - **Manim API Version**: Target the latest stable Manim release.

    - **Allowed Imports**: manim, numpy, and any explicitly approved Manim plugins.

    - **No external assets** (images, audio, explanation files).

    - **Background**: WHITE self.camera.background_color = WHITE)

1. **Manim Object Selection & Configuration**:

    - Define all Manim objects (e.g., MathTex, Circle, Line, Axes, Polygon, Dot, Arrow, Rectangle, Ellipse, Arc, Brace, etc.).

    - Specify key parameters: dimensions, color, stroke_width, fill_opacity, etc.

    - **Color Scheme for White Background**:

        - Lines/Strokes: BLACK, DARK_GRAY, GREY_D

        - Text/Labels: BLACK, DARK_GRAY

        - Highlights: BLUE_D, RED_D, GREEN_D, PURPLE_D, ORANGE

        - Auxiliary elements: GREY, GREY_B

        - Fills: Low opacity with any color (opacity 0.1-0.3)

    - **Discipline-Specific Color Conventions**:

        - **Physics**: Gravity/weight in RED_D; normal force in BLUE_D; friction in ORANGE; tension in GREEN_D; velocity in BLUE; acceleration in RED

        - **Chemistry**: Oxygen atoms in RED; nitrogen in BLUE_D; carbon in DARK_GRAY; hydrogen in GREY; bonds in BLACK; positive charges in RED; negative charges in BLUE

        - **Biology**: Cell membrane in GOLD_D; nucleus in PURPLE_D; mitochondria in RED_D; chloroplasts in GREEN_D; ER in BLUE_D

        - **Mathematics**: Construction lines in BLUE_D; auxiliary lines in GREY dashed; key points/results in RED_D; shaded regions in light fills

        - Adapt these conventions to the specific problem context.

    - **Text Objects (Use Sparingly)**:

        - MathTex: For mathematical/scientific expressions only. Example: MathTex("F = ma", color=BLACK), MathTex("\\Delta H = -92\\text{{ kJ}}", color=BLACK).

        - Tex: For essential labels only. Example: Tex("A", color=BLACK) for point labels, Tex("anode", color=BLACK, font_size=20).

        - **Mixed text/math**: Use \\text{{}} within MathTex. Example: MathTex(r"E_a = 50\\text{{ kJ/mol}}", color=BLACK).

        - **LaTeX Packages**: If needed (e.g., mhchem for chemistry: \\ce{{H2O}}), specify and use TexTemplate with add_to_preamble().

        - **Font Size Guidelines**:

            - Labels: font_size 20-24

            - Mathematical/scientific expressions: font_size 24-28

            - Keep text concise; if unavoidable longer text, reduce size and use line breaks.

    - Confirm all objects are within safe area (0.5 units from edges) with minimum 0.3 units spacing.

2. **VGroup Structure & Hierarchy**:

    - Organize related elements into VGroups for efficient spatial management.

    - Define parent-child relationships with internal spacing of at least 0.3 units.

    - Document purpose for each grouping (e.g., "axis_labels_group", "force_vectors_group", "molecule_group", "cell_organelles_group").

    - **Use VGroups to prevent overlap between logical element groups.**

3. **Spatial Positioning Strategy**:

    - Use ONLY relative positioning methods next_to, align_to, shift, move_to(ORIGIN), to_corner, to_edge).

    - For every object, specify:

        - Reference object (or ORIGIN/edge) used for positioning.

        - Method and direction with buff value (minimum 0.3 units).

    - **Layout Sequence**: Define the order of object placement.

    - **Layout Sketch** (recommended):

        ```

        [ASCII representation of final layout showing all elements and their relative positions]

        [Mark spacing between elements to verify non-overlap]

        ```

    - Verify all elements respect safe margins and spacing.

    - **OVERLAP PREVENTION**: Explicitly verify that no two elements occupy the same or adjacent space without proper buffering.

4. **Visual Hierarchy & Styling**:

    - Define color scheme for visual clarity and emphasis (adapted for WHITE background and discipline conventions).

    - Specify which elements are primary (larger, bolder, prominent colors) vs. secondary.

    - Use visual properties (color, size, stroke_width, opacity) to guide viewer's attention.

    - **Contrast Check**: Ensure all elements are clearly visible against WHITE background.

5. **Code Structure (Static Diagram)**:

    - construct method structure for static output:

        1. **Set background color**: self.camera.background_color = WHITE

        2. Create all objects (with appropriate colors for white background and discipline conventions)

        3. Position all objects (relative positioning)

        4. Add all objects to scene with self.add() (NOT self.play())

    - **No animations**: Use self.add() instead of self.play(Create(...)), self.play(Write(...)), etc.

    - Propose helper functions for creating repeated elements (e.g., create_atom(symbol, color), create_force_arrow(direction, label), create_resistor(start, end)).

    - Include inline comments documenting configuration choices.

    - **LaTeX Template Setup** (if needed for discipline-specific notation):

        ```python

        # Example for chemistry notation

        chem_template = TexTemplate()

        chem_template.add_to_preamble(r"\\usepackage[version=4]{{mhchem}}")

        # Then use: MathTex(r"\\ce{{2H2 + O2 -> 2H2O}}", tex_template=chem_template, color=BLACK)

        ```

6. **Final Object List**:

    - Enumerate all objects that will appear in the final PNG.

    - For each object: type, position reference, key styling (including color), spacing verification.

    - **Color verification**: Confirm no WHITE elements on WHITE background.

    - **Overlap verification**: Confirm each object has clear space around it.

    - **Discipline accuracy verification**: Confirm visual conventions match the subject domain.

================================================================================

MANDATORY SAFETY CHECKS

================================================================================

- [ ] **Background Color Set**: Verify self.camera.background_color = WHITE is included.

- [ ] **Color Contrast**: Verify no WHITE or near-WHITE elements used for visible objects.

- [ ] **Safe Area Enforcement**: All objects (including text bounding boxes) must remain within 0.5 unit margins.

- [ ] **Minimum Spacing Validation**: Confirm minimum 0.3 units spacing between every pair of objects.

- [ ] **Text Minimization**: Verify only essential labels/annotations are included.

- [ ] **Static Output Verification**: Ensure code uses self.add() for all objects, no animation calls.

- [ ] **NO OVERLAP VERIFICATION**: Explicitly confirm that NO elements overlap, obscure, or crowd each other.

- [ ] **LAYOUT BALANCE**: Verify elements are distributed logically across available space.

- [ ] **LABEL CLARITY**: Confirm all labels are positioned clearly and do not overlap with their referenced objects.

- [ ] **DISCIPLINE ACCURACY**: Verify diagram follows the visual conventions and standards of the relevant subject domain.

- [ ] **NOTATION CORRECTNESS**: Verify all scientific/mathematical notation is correct for the discipline (e.g., proper chemical formulas, correct physical units, standard mathematical symbols).

</SCENE_VISION_STORYBOARD_AND_TECHNICAL_PLAN>

```

"""





_prompt_rag_query_generation_storyboard = """You are an expert in generating search queries specifically for **Manim (Community Edition) documentation** (both core Manim and its plugins). Your task is to transform a storyboard plan for a Manim explanation scene into effective queries that will retrieve relevant information from Manim documentation. The storyboard plan describes the scene's visual elements and narrative flow.

Here is the storyboard plan:

{storyboard}

Based on the storyboard plan, generate multiple human-like queries (maximum 10) for retrieving relevant documentation. Please ensure that the search targets are different so that the RAG can retrieve a diverse set of documents covering various aspects of the implementation.

**Specifically, ensure that:**
1.  At least some queries are focused on retrieving information about **Manim core functionalities**, like general visual elements or animations. Frame these queries using Manim terminology (classes, methods, concepts).
2.  If the storyboard suggests using specific visual effects or complex animations that might be plugin-related, include at least 1 query specifically targeting **plugin documentation**.  Make sure to mention the plugin name if known or suspected.
3.  Queries should be general enough to explore different possibilities within Manim and its plugins based on the storyboard's visual and narrative descriptions, but also specific enough to target Manim documentation effectively.

The above storyboard might be relevant to these plugins: {relevant_plugins}.
Note that you MUST NOT use the plugins that are not listed above.

Output the queries in the following format:
```json
[
    {{"query": "content of query 1", "type": "manim_core/{relevant_plugins}"}},
    {{"query": "content of query 2", "type": "manim_core/{relevant_plugins}"}},
    {{"query": "content of query 3", "type": "manim_core/{relevant_plugins}"}},
    {{"query": "content of query 4", "type": "manim_core/{relevant_plugins}"}},
    {{"query": "content of query 5", "type": "manim_core/{relevant_plugins}"}},
    {{"query": "content of query 6", "type": "manim_core/{relevant_plugins}"}},
    {{"query": "content of query 7", "type": "manim_core/{relevant_plugins}"}},
]
``` """

_code_background = """PLEASE DO NOT create another color background Rectangles. Default background (Black) is enough.
PLEASE DO NOT use BLACK color for any text.
"""

_prompt_context_learning_vision_storyboard = """Here are some example vision and storyboard plans to help guide your planning:

{examples}

Please follow a similar structure while maintaining creativity and relevance to the current scene."""

_prompt_context_learning_code = """Here are some example Manim code implementations to help guide your code generation:

{examples}

Please follow similar patterns and best practices while implementing the current scene."""

_code_limit = """Note that the frame width and height are 14.222222222222221 and 8.0 respectively. And the center of the frame is (0, 0, 0).
It means to avoid putting any object out of the frame, you should limit the x and y coordinates of the objects.
limit x to be within -7.0 and 7.0 for objects, and limit y to be within -4.0 and 4.0 for objects.
Place the objects near the center of the frame, without overlapping with each other."""

_prompt_animation_rag_query_generation = """You are an expert in Manim (Community Edition) and its plugins. Your task is to transform a topic for a Manim animation scene into queries that can be used to retrieve relevant documentation from both Manim core and any relevant plugins.

Your queries should include keywords related to the specific Manim classes, methods, functions, and *concepts* that are likely to be used to implement the scene, including any plugin-specific functionality. Focus on extracting the core concepts, actions, and vocabulary from the *entire* scene plan. Generate queries that are concise and target different aspects of the documentation (class reference, method usage, animation examples, conceptual explanations) across both Manim core and relevant plugins.

Here is the Topic (and the context):

{topic}. {context}

Based on the topic and the context, generate multiple human-like queries (maximum 5-7) for retrieving relevant documentation. Please ensure that the search targets are different so that the RAG can retrieve a diverse set of documents covering various aspects of the implementation.

**Specifically, ensure that:**
1. At least 1-2 queries are focused on retrieving information about Manim *function usage* in Manim scenes
2. If the topic and the context can be linked to the use of plugin functionality, include at least 1 query specifically targeting plugin documentation
3. Queries should be specific enough to distinguish between core Manim and plugin functionality when relevant

The above text explanations are relevant to these plugins: {relevant_plugins}

Output the queries in the following format:
```json
[
    {{"query": "content of query 1", "type": "manim_core/name_of_the_plugin"}},
    {{"query": "content of query 2", "type": "manim_core/name_of_the_plugin"}},
    {{"query": "content of query 3", "type": "manim_core/name_of_the_plugin"}},
    {{"query": "content of query 4", "type": "manim_core/name_of_the_plugin"}},
    {{"query": "content of query 5", "type": "manim_core/name_of_the_plugin"}},
    {{"query": "content of query 6", "type": "manim_core/name_of_the_plugin"}},
    {{"query": "content of query 7", "type": "manim_core/name_of_the_plugin"}},
]
```"""

_code_font_size = """If there is title text, font size is highly recommended to be 28.
If there are side labels, font size is highly recommended to be 24.
If there are formulas, font size is highly recommended to be 24.

However, if the text has more than 10 words, font size should be reduced further and mutiple lines should be used."""

_prompt_best_practices = """# Best practices for generating educational explanations with manim

1. Specify positions as relative to other objects whenever it makes sense.
   * For example, if you want to place a label for a geometric object.
2. Objects should be of different color from the black background.
3. Keep the text on screen concise.
   * On-screen elements should focus on showcasing the concept, examples and visuals. Labels and illustrative text are still encouraged.
   * For explanations and observations, prefer narrations over on-screen text.
   * You should still show calculations and algorithms in full on screen.
   * For examples and practice problems, it is reasonable to show more text, especially key statements.
   * Longer text should appear smaller to fit on screen.
4. To control the timing of objects appearing:
   * `add` has instantaneous effect, best used for the initial setup of the scene.
   * Animations are best used during narration.
   * Make sure the animations make sense. If an object is already on screen, it makes no sense to fade it in or create it again.
5. Use TeX or MathTeX whenever you want to display math, including symbols and formulas.
"""

_prompt_scene_plan = """You are an expert in educational content design, instructional design, and multi-disciplinary education (mathematics, physics, chemistry, biology, and more). Please design a structured explanation document to solve the given problem with diagrams and text.

**CRITICAL LANGUAGE REQUIREMENT:**
- If the problem statement is in Chinese (or any other language), you MUST accurately translate it to English first
- All TEXT blocks, explanations, and scene descriptions must be written entirely in English

**Problem Overview:**

{description}

**Structure Requirements:**

The output should be a **Markdown-friendly outline** that interleaves:

- <TEXT_k> blocks: written explanation (all explanatory text goes here, **must follow Markdown formatting rules**)

- <SCENE_k> blocks: diagram specifications to render (visual only, minimal text)

**Diagram Necessity Rule (CRITICAL — must follow):**

First, determine whether the problem **benefits from** or **can be illustrated with** diagrams:

- **Diagram IS appropriate** for: geometry problems, coordinate/graph problems, physics scenarios with force diagrams / circuits / optics / motion, chemistry molecular structures / reaction diagrams / phase diagrams, biology cell structures / anatomical diagrams / phylogenetic trees, data visualization, function plots, spatial reasoning, etc.

- **Diagram is NOT appropriate** for: pure algebraic manipulation, arithmetic computation, word problems that are purely logical/verbal, definition recall, proof by induction with no geometric interpretation, simple unit conversions, fill-in-the-blank factual questions, or any problem where a diagram would add no meaningful visual insight.

**If no diagram is needed or no meaningful diagram can be drawn**, you MUST output exactly ONE <SCENE_1> block with the content No diagram, and NO further <SCENE_k> blocks:

```xml

<SCENE_1>

No diagram

</SCENE_1>

```

All explanation in that case goes entirely into <TEXT_k> blocks.

**Critical Diagram Rule (when diagrams ARE used):**

- <SCENE_k> blocks are for **DIAGRAMS ONLY**

- Diagrams should contain ONLY:

  - Geometric shapes, lines, curves, graphs, vectors, circuits, molecular structures, biological structures, etc.

  - Point labels (e.g., "A", "B", "C", "P₁")

  - Axis labels (e.g., "x", "y", "t", "v", "pH", "T/K")

  - Essential mathematical or scientific annotations (e.g., "90°", "r=5", "F₁", "mg", "OH⁻", "ATP")

  - Coordinate values at key points (e.g., "(3,4)")

  - Standard scientific symbols and short labels (e.g., "R₁", "C₂H₅OH", "nucleus", "mitochondria" as labels on structures)

- **DO NOT include** in diagrams: problem statement, titles, explanations, sentences, descriptions, or any text that explains "what" or "why"

- Use diagrams to visualize each step; all explanatory content belongs in <TEXT_k> blocks, not in the diagrams.

- Solve the problem step-by-step: understand → plan → execute → conclude, then briefly mention alternative approaches if any.

Please generate the outline in the following format:

```xml

<SCENE_OUTLINE>

    <TEXT_1>

    [First state the full problem statement verbatim, then briefly outline the solution approach]

    </TEXT_1>

    <SCENE_1>

    Scene Purpose: [Learning objective - for planning only, not rendered]

    Visual Elements: [List specific objects to draw: points, lines, shapes, curves, vectors, circuits, molecular structures, biological diagrams, etc.]

    Labels: [Only essential labels: point names, coordinates, angle measures, lengths, force names, chemical symbols, etc.]

    Colors/Styling: [Color coding for visual distinction]

    Layout: [Spatial arrangement, consider safe area and spacing]

    </SCENE_1>

    <TEXT_2>

    [Text explanation that refers to the diagram above; step-by-step reasoning]

    </TEXT_2>

    <SCENE_2>

    Scene Purpose: [Learning objective - for planning only]

    Visual Elements: [Objects to draw, including auxiliary lines/elements if needed]

    Labels: [Essential labels only]

    Colors/Styling: [Highlighting, dashed lines, shading]

    Layout: [Spatial layout]

    </SCENE_2>

    <TEXT_3>

    [Continue explanation...]

    </TEXT_3>

    ...

    <TEXT_N>

    [Final answer + verification + short recap]

    </TEXT_N>

</SCENE_OUTLINE>

```

**Content Flow (must follow):**

1) TEXT: restate problem

2) SCENE: initial problem diagram (visual only) — OR No diagram if not applicable

3) TEXT: explanation referencing the diagram (or proceeding directly with reasoning if no diagram)

4) SCENE: auxiliary diagram if needed (visual only) — **skip if <SCENE_1> is No diagram**

5) TEXT: explanation

...

Final TEXT must include: final answer, verification, recap.

**Scene count:**

- If diagrams are appropriate: 1–7 scenes.

- If diagrams are NOT appropriate: exactly 1 scene No diagram), with all content in TEXT blocks.

**Hard requirement:** Every <SCENE_k> (except a lone No diagram scene) must have at least one adjacent <TEXT_k> block so the Markdown reads naturally.

**Requirements (must-follow):**

1. <TEXT_1> must include the full problem statement verbatim and briefly state the solution approach.

2. If diagrams are used, <SCENE_1> must describe a clear **problem diagram** that visualizes the setup (e.g., coordinate plane + points for geometry, free-body diagram for physics, molecular structure for chemistry, cell diagram for biology).

3. If no diagram is needed, <SCENE_1> must contain exactly No diagram and there must be NO subsequent <SCENE_k> blocks.

4. Each <SCENE_k> (when used) specifies ONLY visual elements:

   - **Visual Elements**: shapes, lines, points, curves, graphs, vectors, arrows, circuits, molecular bonds, biological structures, etc.

   - **Labels**: single letters (A, B, C), coordinates ((3,4)), measurements (5cm, 90°), force symbols (F, mg, T), chemical formulas (H₂O, NaCl), biological terms as structure labels

   - **Colors/Styling**: colors, line styles (dashed, solid), fill/shading

   - **NO sentences, NO explanations, NO titles in diagrams**

5. Each <TEXT_k> should be written as if explaining to a student: clear, step-by-step reasoning appropriate to the subject domain.

6. All explanation and reasoning goes in <TEXT_k> blocks; diagrams are purely visual.

7. Structure constraints:

   - Start with problem statement + initial diagram (or No diagram)

   - Include intermediate steps with supporting diagrams (only when needed AND only when diagrams are being used)

   - End with final answer + verification; optional short recap.

8. Diagram label specifications (when diagrams are used):

   - Use single letters or short symbols for points (A, B, P₁, Q)

   - Use numeric values for coordinates, angles, lengths

   - Use standard scientific notation for domain-specific labels (F₁, v₀, ΔH, pH, ATP)

   - Specify colors for highlighting (e.g., "triangle ADC filled with light red", "force vector in blue")

   - Specify line styles (solid, dashed, dotted, wavy for bonds)

   - No full words or phrases as labels (except universally recognized short terms like "Origin", "nucleus", "anode", "cathode")

**Subject-Specific Diagram Guidance:**

- **Mathematics**: coordinate planes, geometric figures, function graphs, number lines, Venn diagrams

- **Physics**: free-body diagrams, circuit diagrams, ray diagrams, motion diagrams, field lines, P-V diagrams, wave diagrams

- **Chemistry**: molecular structures (Lewis dots, skeletal, 3D), reaction coordinate diagrams, phase diagrams, titration curves, orbital diagrams, electrochemical cells

- **Biology**: cell structure diagrams, anatomical cross-sections, phylogenetic trees, Punnett squares, metabolic pathway diagrams, ecological pyramids

- **Other subjects**: use appropriate visual representations; if no standard diagram type exists for the problem, use No diagram

Note: This is a high-level outline. Each <SCENE_k> will later be rendered as a static image using Manim (containing only visual elements and minimal labels), and all <TEXT_k> blocks will be compiled into a Markdown document with embedded diagrams."""


_prompt_rag_query_generation_technical = """You are an expert in generating search queries specifically for **Manim (Community Edition) documentation** (both core Manim and its plugins). Your task is to analyze a storyboard plan and generate effective queries that will retrieve relevant technical documentation about implementation details.

Here is the storyboard plan:

{storyboard}

Based on this storyboard plan, generate multiple human-like queries (maximum 10) for retrieving relevant technical documentation.

**Specifically, ensure that:**
1. Queries focus on retrieving information about **core Manim functionality** and implementation details
2. Include queries about **complex animations and effects** described in the storyboard
3. If the storyboard suggests using plugin functionality, include specific queries targeting those plugin's technical documentation

The above storyboard plan is relevant to these plugins: {relevant_plugins}
Note that you MUST NOT use the plugins that are not listed above.

You MUST only output the queries in the following JSON format (with json triple backticks):
```json
[
    {{"type": "manim-core", "query": "content of core functionality query"}},
    {{"type": "<plugin-name>", "query": "content of plugin-specific query"}},
    {{"type": "manim-core", "query": "content of animation technique query"}}
    ...
]
``` """

_prompt_rag_query_generation_fix_error = """You are an expert in generating search queries specifically for **Manim (Community Edition) documentation** (both core Manim and its plugins). Your task is to transform a Manim error and its associated code into effective queries that will retrieve relevant information from Manim documentation.

Here is the error message:
{error}

Here is the Manim code that caused the error:
{code}

Based on the error and code, generate multiple human-like queries (maximum 10) for retrieving relevant documentation. Please ensure that the search targets are different so that the RAG can retrieve a diverse set of documents covering various aspects of the implementation.

**Specifically, ensure that:**
1.  At least some queries are focused on retrieving information about **Manim function usage** in scenes. Frame these queries to target function definitions, usage examples, and parameter details within Manim documentation.
2.  If the error suggests using plugin functionality, include at least 1 query specifically targeting **plugin documentation**.  Clearly mention the plugin name in these queries to focus the search.
3.  Queries should be specific enough to distinguish between core Manim and plugin functionality when relevant, and to target the most helpful sections of the documentation (API reference, tutorials, examples).

The above error and code are relevant to these plugins: {relevant_plugins}.
Note that you MUST NOT use the plugins that are not listed above.

You MUST only output the queries in the following JSON format (with json triple backticks):
```json
[
    {{"type": "manim-core", "query": "content of function usage query"}},
    {{"type": "<plugin-name>", "query": "content of plugin-specific query"}},
    {{"type": "manim-core", "query": "content of API reference query"}}
    ...
]
``` """

_code_disable = """"""

_prompt_manim_cheatsheet = """The followings are the inheritance diagram of the Manim library. You can take as reference to select which class to use for the animation.

``` 
digraph Animation {
    "AddTextLetterByLetter"
    "ShowIncreasingSubsets"
    "ShowIncreasingSubsets" -> "AddTextLetterByLetter"
    "AddTextWordByWord";
    "Succession";
    "Succession" -> "AddTextWordByWord";
    "AnimatedBoundary";
    "VGroup";
    "VGroup" -> "AnimatedBoundary";
    "Animation";
    "AnimationGroup";
    "Animation" -> "AnimationGroup";
    "ApplyComplexFunction";
    "ApplyMethod";
    "ApplyMethod" -> "ApplyComplexFunction";
    "ApplyFunction";
    "Transform";
    "Transform" -> "ApplyFunction";
    "ApplyMatrix";
    "ApplyPointwiseFunction";
    "ApplyPointwiseFunction" -> "ApplyMatrix";
    "ApplyMethod";
    "Transform" -> "ApplyMethod";
    "ApplyPointwiseFunction";
    "ApplyMethod" -> "ApplyPointwiseFunction";
    "ApplyPointwiseFunctionToCenter";
    "ApplyPointwiseFunction" -> "ApplyPointwiseFunctionToCenter";
    "ApplyWave";
    "Homotopy";
    "Homotopy" -> "ApplyWave";
    "Broadcast";
    "LaggedStart";
    "LaggedStart" -> "Broadcast";
    "ChangeDecimalToValue";
    "ChangingDecimal";
    "ChangingDecimal" -> "ChangeDecimalToValue";
    "ChangeSpeed";
    "Animation" -> "ChangeSpeed";
    "ChangingDecimal";
    "Animation" -> "ChangingDecimal";
    "Circumscribe";
    "Succession" -> "Circumscribe";
    "ClockwiseTransform";
    "Transform" -> "ClockwiseTransform";
    "ComplexHomotopy";
    "Homotopy" -> "ComplexHomotopy";
    "CounterclockwiseTransform";
    "Transform" -> "CounterclockwiseTransform";
    "Create";
    "ShowPartial";
    "ShowPartial" -> "Create";
    "CyclicReplace";
    "Transform" -> "CyclicReplace";
    "DrawBorderThenFill";
    "Animation" -> "DrawBorderThenFill";
    "FadeIn";
    "FadeOut";
    "FadeToColor";
    "ApplyMethod" -> "FadeToColor";
    "FadeTransform";
    "Transform" -> "FadeTransform";
    "FadeTransformPieces";
    "FadeTransform" -> "FadeTransformPieces";
    "Flash";
    "AnimationGroup" -> "Flash";
    "FocusOn";
    "Transform" -> "FocusOn";
    "GrowArrow";
    "GrowFromPoint";
    "GrowFromPoint" -> "GrowArrow";
    "GrowFromCenter";
    "GrowFromPoint" -> "GrowFromCenter";
    "GrowFromEdge";
    "GrowFromPoint" -> "GrowFromEdge";
    "GrowFromPoint";
    "Transform" -> "GrowFromPoint";
    "Homotopy";
    "Animation" -> "Homotopy";
    "Indicate";
    "Transform" -> "Indicate";
    "LaggedStart";
    "AnimationGroup" -> "LaggedStart";
    "LaggedStartMap";
    "LaggedStart" -> "LaggedStartMap";
    "MaintainPositionRelativeTo";
    "Animation" -> "MaintainPositionRelativeTo";
    "Mobject";
    "MoveAlongPath";
    "Animation" -> "MoveAlongPath";
    "MoveToTarget";
    "Transform" -> "MoveToTarget";
    "PhaseFlow";
    "Animation" -> "PhaseFlow";
    "RemoveTextLetterByLetter";
    "AddTextLetterByLetter" -> "RemoveTextLetterByLetter";
    "ReplacementTransform";
    "Transform" -> "ReplacementTransform";
    "Restore";
    "ApplyMethod" -> "Restore";
    "Rotate";
    "Transform" -> "Rotate";
    "Rotating";
    "Animation" ->  "Rotating";
    "ScaleInPlace";
    "ApplyMethod" -> "ScaleInPlace";
    "ShowIncreasingSubsets";
    "Animation" -> "ShowIncreasingSubsets";
    "ShowPartial";
    "Animation" -> "ShowPartial";
    "ShowPassingFlash";
    "ShowPartial" -> "ShowPassingFlash";
    "ShowPassingFlashWithThinningStrokeWidth";
    "AnimationGroup" ->  "ShowPassingFlashWithThinningStrokeWidth";
    "ShowSubmobjectsOneByOne";
    "ShowIncreasingSubsets" -> "ShowSubmobjectsOneByOne";
    "ShrinkToCenter";
    "ScaleInPlace" -> "ShrinkToCenter";
    "SmoothedVectorizedHomotopy";
    "Homotopy" -> "SmoothedVectorizedHomotopy";
    "SpinInFromNothing";
    "GrowFromCenter" -> "SpinInFromNothing";
    "SpiralIn";
    "Animation" -> "SpiralIn";
    "Succession";
    "AnimationGroup" -> "Succession";
    "Swap";
    "CyclicReplace" -> "Swap";
    "TracedPath";
    "VMobject";
    "VMobject" -> "TracedPath";
    "Transform";
    "Animation" -> "Transform";
    "TransformAnimations";
    "Transform" -> "TransformAnimations";
    "TransformFromCopy";
    "Transform" -> "TransformFromCopy";
    "TransformMatchingAbstractBase";
    "AnimationGroup" -> "TransformMatchingAbstractBase";
    "TransformMatchingShapes";
    "TransformMatchingAbstractBase" -> "TransformMatchingShapes";
    "TransformMatchingTex";
    "TransformMatchingAbstractBase" ->  "TransformMatchingTex";
    "Uncreate";
    "Create" -> "Uncreate";
    "Unwrite";
    "Write";
    "Write" -> "Unwrite";
    "UpdateFromAlphaFunc";
    "UpdateFromFunc";
    "UpdateFromFunc" -> "UpdateFromAlphaFunc";
    "UpdateFromFunc";
    "Animation" -> "UpdateFromFunc";
    "VGroup";
    "VMobject" ->  "VGroup";
    "VMobject";
    "Mobject" -> "VMobject";

    "Wait";
    "Animation" -> "Wait";
    "Wiggle";
    "Animation" -> "Wiggle";
    "Write";
    "DrawBorderThenFill" ->  "Write";
}
```


```
digraph Camera {
    "BackgroundColoredVMobjectDisplayer"
    "Camera"
    "MappingCamera"
    "Camera" -> "MappingCamera"
    "MovingCamera"
    "Camera" -> "MovingCamera"
    "MultiCamera"
    "MovingCamera" -> "MultiCamera"
    "OldMultiCamera"
    "Camera" -> "OldMultiCamera"
    "SplitScreenCamera"
    "OldMultiCamera" -> "SplitScreenCamera"
    "ThreeDCamera"
    "Camera" -> "ThreeDCamera"
}
```

```
digraph MObject {
    "AbstractImageMobject"
    "Mobject" -> "AbstractImageMobject"
    "Angle"
    "VMobject" -> "Angle"
    "AnnotationDot"
    "Dot" -> "AnnotationDot"
    "AnnularSector"
    "Arc" -> "AnnularSector"
    "Annulus"
    "Circle" -> "Annulus"
    "Arc"
    "TipableVMobject" -> "Arc"
    "ArcBetweenPoints"
    "Arc" -> "ArcBetweenPoints"
    "ArcBrace"
    "Brace" -> "ArcBrace"
    "ArcPolygon"
    "VMobject" -> "ArcPolygon"
    "ArcPolygonFromArcs"
    "VMobject" -> "ArcPolygonFromArcs"
    "Arrow"
    "Line" -> "Arrow"
    "Arrow3D"
    "Line3D" -> "Arrow3D"
    "ArrowCircleFilledTip"
    "ArrowCircleTip" -> "ArrowCircleFilledTip"
    "ArrowCircleTip"
    "ArrowTip" -> "ArrowCircleTip"
    "Circle" -> "ArrowCircleTip"
    "ArrowSquareFilledTip"
    "ArrowSquareTip" -> "ArrowSquareFilledTip"
    "ArrowSquareTip"
    "ArrowTip" -> "ArrowSquareTip"
    "Square" -> "ArrowSquareTip"
    "ArrowTip"
    "VMobject" -> "ArrowTip"
    "ArrowTriangleFilledTip"
    "ArrowTriangleTip" -> "ArrowTriangleFilledTip"
    "ArrowTriangleTip"
    "ArrowTip" -> "ArrowTriangleTip"
    "Triangle" -> "ArrowTriangleTip"
    "ArrowVectorField"
    "VectorField" -> "ArrowVectorField"
    "Axes"
    "VGroup" -> "Axes"
    "CoordinateSystem" -> "Axes"
    "BackgroundRectangle"
    "SurroundingRectangle" -> "BackgroundRectangle"
    "BarChart"
    "Axes" -> "BarChart"
    "Brace"
    "svg_mobject.VMobjectFromSVGPath" -> "Brace"
    "BraceBetweenPoints"
    "Brace" -> "BraceBetweenPoints"
    "BraceLabel"
    "VMobject" -> "BraceLabel"
    "BraceText"
    "BraceLabel" -> "BraceText"
    "BulletedList"
    "Tex" -> "BulletedList"
    "Circle"
    "Arc" -> "Circle"
    "Code"
    "VGroup" -> "Code"
    "ComplexPlane"
    "NumberPlane" -> "ComplexPlane"
    "ComplexValueTracker"
    "ValueTracker" -> "ComplexValueTracker"
    "Cone"
    "Surface" -> "Cone"
    "CoordinateSystem"
    "Cross"
    "VGroup" -> "Cross"
    "Cube"
    "VGroup" -> "Cube"
    "CubicBezier"
    "VMobject" -> "CubicBezier"
    "CurvedArrow"
    "ArcBetweenPoints" -> "CurvedArrow"
    "CurvedDoubleArrow"
    "CurvedArrow" -> "CurvedDoubleArrow"
    "CurvesAsSubmobjects"
    "VGroup" -> "CurvesAsSubmobjects"
    "Cutout"
    "VMobject" -> "Cutout"
    "Cylinder"
    "Surface" -> "Cylinder"
    "DashedLine"
    "Line" -> "DashedLine"
    "DashedVMobject"
    "VMobject" -> "DashedVMobject"
    "DecimalMatrix"
    "Matrix" -> "DecimalMatrix"
    "DecimalNumber"
    "VMobject" -> "DecimalNumber"
    "DecimalTable"
    "Table" -> "DecimalTable"
    "DiGraph"
    "GenericGraph" -> "DiGraph"
    "Difference"
    "Dodecahedron"
    "Polyhedron" -> "Dodecahedron"
    "Dot"
    "Circle" -> "Dot"
    "Dot3D"
    "Sphere" -> "Dot3D"
    "DoubleArrow"
    "Arrow" -> "DoubleArrow"
    "Elbow"
    "VMobject" -> "Elbow"
    "Ellipse"
    "Circle" -> "Ellipse"
    "Exclusion"
    "FullScreenRectangle"
    "ScreenRectangle" -> "FullScreenRectangle"
    "FunctionGraph"
    "ParametricFunction" -> "FunctionGraph"
    "Generic"
    "GenericGraph"
    "Generic" -> "GenericGraph"
    "Graph"
    "GenericGraph" -> "Graph"
    "Group"
    "Mobject" -> "Group"
    "Icosahedron"
    "Polyhedron" -> "Icosahedron"
    "ImageMobject"
    "AbstractImageMobject" -> "ImageMobject"
    "ImageMobjectFromCamera"
    "AbstractImageMobject" -> "ImageMobjectFromCamera"
    "ImplicitFunction"
    "VMobject" -> "ImplicitFunction"
    "Integer"
    "DecimalNumber" -> "Integer"
    "IntegerMatrix"
    "Matrix" -> "IntegerMatrix"
    "IntegerTable"
    "Table" -> "IntegerTable"
    "Intersection"
    "LabeledDot"
    "Dot" -> "LabeledDot"
    "LayoutFunction"
    "Protocol" -> "LayoutFunction"
    "Line"
    "TipableVMobject" -> "Line"
    "Line3D"
    "Cylinder" -> "Line3D"
    "LinearBase"
    "LogBase"
    "ManimBanner"
    "VGroup" -> "ManimBanner"
    "MarkupText"
    "svg_mobject.SVGMobject" -> "MarkupText"
    "MathTable"
    "Table" -> "MathTable"
    "MathTex"
    "SingleStringMathTex" -> "MathTex"
    "Matrix"
    "VMobject" -> "Matrix"
    "Mobject"
    "Mobject1D"
    "PMobject" -> "Mobject1D"
    "Mobject2D"
    "PMobject" -> "Mobject2D"
    "MobjectMatrix"
    "Matrix" -> "MobjectMatrix"
    "MobjectTable"
    "Table" -> "MobjectTable"
    "NumberLine"
    "Line" -> "NumberLine"
    "NumberPlane"
    "Axes" -> "NumberPlane"
    "Octahedron"
    "Polyhedron" -> "Octahedron"
    "PGroup"
    "PMobject" -> "PGroup"
    "PMobject"
    "Mobject" -> "PMobject"
    "Paragraph"
    "VGroup" -> "Paragraph"
    "ParametricFunction"
    "VMobject" -> "ParametricFunction"
    "Point"
    "PMobject" -> "Point"
    "PointCloudDot"
    "Mobject1D" -> "PointCloudDot"
    "PolarPlane"
    "Axes" -> "PolarPlane"
    "Polygon"
    "Polygram" -> "Polygon"
    "Polygram"
    "VMobject" -> "Polygram"
    "Polyhedron"
    "VGroup" -> "Polyhedron"
    "Prism"
    "Cube" -> "Prism"
    "Protocol"
    "Generic" -> "Protocol"
    "Rectangle"
    "Polygon" -> "Rectangle"
    "RegularPolygon"
    "RegularPolygram" -> "RegularPolygon"
    "RegularPolygram"
    "Polygram" -> "RegularPolygram"
    "RightAngle"
    "Angle" -> "RightAngle"
    "RoundedRectangle"
    "Rectangle" -> "RoundedRectangle"
    "SVGMobject"
    "VMobject" -> "SVGMobject"
    "SampleSpace"
    "Rectangle" -> "SampleSpace"
    "ScreenRectangle"
    "Rectangle" -> "ScreenRectangle"
    "Sector"
    "AnnularSector" -> "Sector"
    "SingleStringMathTex"
    "svg_mobject.SVGMobject" -> "SingleStringMathTex"
    "Sphere"
    "Surface" -> "Sphere"
    "Square"
    "Rectangle" -> "Square"
    "Star"
    "Polygon" -> "Star"
    "StealthTip"
    "ArrowTip" -> "StealthTip"
    "StreamLines"
    "VectorField" -> "StreamLines"
    "Surface"
    "VGroup" -> "Surface"
    "SurroundingRectangle"
    "RoundedRectangle" -> "SurroundingRectangle"
    "Table"
    "VGroup" -> "Table"
    "TangentLine"
    "Line" -> "TangentLine"
    "Tetrahedron"
    "Polyhedron" -> "Tetrahedron"
    "Tex"
    "MathTex" -> "Tex"
    "Text"
    "svg_mobject.SVGMobject" -> "Text"
    "ThreeDAxes"
    "Axes" -> "ThreeDAxes"
    "ThreeDVMobject"
    "VMobject" -> "ThreeDVMobject"
    "TipableVMobject"
    "VMobject" -> "TipableVMobject"
    "Title"
    "Tex" -> "Title"
    "Torus"
    "Surface" -> "Torus"
    "Triangle"
    "RegularPolygon" -> "Triangle"
    "Underline"
    "Line" -> "Underline"
    "Union"
    "UnitInterval"
    "NumberLine" -> "UnitInterval"
    "VDict"
    "VMobject" -> "VDict"
    "VGroup"
    "VMobject" -> "VGroup"
    "VMobject"
    "Mobject" -> "VMobject"
    "VMobjectFromSVGPath"
    "VMobject" -> "VMobjectFromSVGPath"
    "ValueTracker"
    "Mobject" -> "ValueTracker"
    "Variable"
    "VMobject" -> "Variable"
    "Vector"
    "Arrow" -> "Vector"
    "VectorField"
    "VGroup" -> "VectorField"
    "VectorizedPoint"
    "VMobject" -> "VectorizedPoint"
}
```

```
digraph Scene {
    "LinearTransformationScene"
    "VectorScene"
    "VectorScene" -> "LinearTransformationScene"
    "MovingCameraScene"
    "Scene"
    "Scene" -> "MovingCameraScene"
    "RerunSceneHandler"
    "Scene"
    "SceneFileWriter"
    "SpecialThreeDScene"
    "ThreeDScene"
    "ThreeDScene" -> "SpecialThreeDScene"
    "ThreeDScene"
    "Scene" -> "ThreeDScene"
    "VectorScene"
    "Scene" -> "VectorScene"
    "ZoomedScene"
    "MovingCameraScene" -> "ZoomedScene"
}
```"""

_prompt_rag_query_generation_vision_storyboard = """You are an expert in generating search queries specifically for **Manim (Community Edition) documentation** (both core Manim and its plugins). Your task is to analyze a scene plan for a Manim animation and generate effective queries that will retrieve relevant documentation about visual elements and scene composition.

Here is the scene plan:

{scene_plan}

Based on this scene plan, generate multiple human-like queries (maximum 10) for retrieving relevant documentation about visual elements and scene composition techniques.

**Specifically, ensure that:**
1. Queries focus on retrieving information about **visual elements** like shapes, objects, and their properties
2. Include queries about **scene composition techniques** like layout, positioning, and grouping
3. If the scene plan suggests using plugin functionality, include specific queries targeting those plugin's visual capabilities
4. Queries should be high-level, aiming to discover what Manim features can be used, rather than focusing on low-level implementation details.
    - For example, instead of "how to set the color of a circle", ask "what visual properties of shapes can I control in Manim?".

The above scene plan is relevant to these plugins: {relevant_plugins}.
Note that you MUST NOT use the plugins that are not listed above.

You MUST only output the queries in the following JSON format (with json triple backticks):
```json
[
    {{"type": "manim-core", "query": "content of visual element query"}},
    {{"type": "<plugin-name>", "query": "content of plugin-specific query"}},
    {{"type": "manim-core", "query": "content of composition technique query"}}
    ...
]
```"""

_prompt_context_learning_technical_implementation = """Here are some example technical implementation plans to help guide your implementation:

{examples}

Please follow a similar structure while maintaining creativity and relevance to the current scene."""

_prompt_detect_plugins = """You are a Manim plugin detection system. Your task is to analyze a explanation topic and description to determine which Manim plugins would be most relevant for the actual animation implementation needs.

Topic:
{topic}

Description:
{description}

Available Plugins:
{plugin_descriptions}

Instructions:
1. Analyze the topic and description, focusing specifically on what needs to be animated
2. Review each plugin's capabilities and determine if they provide specific tools needed for the animations described
3. Only select plugins that provide functionality directly needed for the core animations
4. Consider these criteria for each plugin:
   - Does the plugin provide specific tools or components needed for the main visual elements?
   - Are the plugin's features necessary for implementing the core animations?
   - Would the animation be significantly more difficult to create without this plugin?
5. Exclude plugins that:
   - Only relate to the general topic area but don't provide needed animation tools
   - Might be "nice to have" but aren't essential for the core visualization
   - Could be replaced easily with basic Manim shapes and animations

Your response must follow the output format below:
<THINKING>
[brief description of your thinking process]
</THINKING>
<PLUGINS>
```json
["plugin_name1", "plugin_name2"]
```
</PLUGINS>"""

_prompt_scene_animation_narration = """You are an expert in educational explanation production and Manim animation, skilled in creating engaging and pedagogically effective learning experiences.  
**Reminder:** This animation and narration plan is entirely self-contained; there is no dependency on any previous or subsequent scene implementations. However, the narration should flow smoothly as part of a larger, single explanation.

Your task is to create a **detailed animation and narration plan for Scene {scene_number}**, ensuring it is not just visually appealing but also serves a clear educational purpose within the overall explanation topic.

Remember, the narration should not simply describe what's happening visually, but rather **teach a concept step-by-step**, guiding the viewer to a deeper understanding.  Animations should be spatially coherent, contribute to a clear visual flow, and strictly respect safe area margins (0.5 units) and minimum spacing (0.3 units).  **Consider the scene number {scene_number} and the overall scene context to ensure smooth transitions and a logical flow within the larger explanation narrative.**

Topic: {topic}
Description: {description}

Scene Overview:
{scene_outline}

Scene Vision and Storyboard:
{scene_vision_storyboard}

Technical Implementation Plan:
{technical_implementation_plan}

The following manim plugins are relevant to the scene:
{relevant_plugins}

**Spatial Constraints (Strictly Enforced Throughout Animations):**
*   **Safe area margins:** 0.5 units. *Maintain objects and VGroups within margins.*
*   **Minimum spacing:** 0.3 units. *Ensure minimum spacing between all objects and VGroups.*

**Animation Timing and Pacing Requirements:**
*   Specify `run_time` for all animations.
*   Use `Wait()` for transition buffers, specifying durations and **pedagogical purpose**.
*   Coordinate animation timings with narration cues for synchronized pedagogical presentation.

**Visual Flow and Pedagogical Clarity:**
*   Ensure animations create a clear and logical visual flow, **optimized for learning and concept understanding.**
*   Use animation pacing and transition buffers to visually separate ideas and **enhance pedagogical clarity.**
*   Maintain spatial coherence for predictable and understandable animations, strictly adhering to spatial constraints.

**Diagrams/Sketches (Optional but Highly Recommended for Complex Scenes):**
*   For complex animations, include diagrams/sketches to visualize animation flow and object movements. This aids clarity and reduces errors.

Your plan must demonstrate a strong understanding of pedagogical narration and how animations can be used to effectively teach concepts, while strictly adhering to spatial constraints and timing requirements.

You MUST generate a **detailed and comprehensive** animation and narration plan for **Scene {scene_number}**, in the following format, similar to the example provided (from ```xml to </SCENE_ANIMATION_NARRATION_PLAN>```):

```xml
<SCENE_ANIMATION_NARRATION_PLAN>

[ANIMATION_STRATEGY]
1. **Pedagogical Animation Plan:** Provide a detailed plan for all animations in the scene, explicitly focusing on how each animation contributes to **teaching the core concepts** of this scene.
    - **Parent VGroup transitions (if applicable):**
        - If VGroups are used, specify transitions (`Shift`, `Transform`, `FadeIn`, `FadeOut`) with `Animation` type, direction, magnitude, target VGroup, and `run_time`.
        - **Explain the pedagogical rationale** for each VGroup transition. How does it guide the viewer's attention or contribute to understanding the scene's learning objectives? Ensure spatial coherence and respect for constraints.
    - **Element animations within VGroups and for individual Mobjects:**
        - Specify animation types (`Create`, `Write`, `FadeIn`, `Transform`, `Circumscribe`, `AnimationGroup`, `Succession`) for elements.
        - For each element animation, specify `Animation` type, target object(s), and `run_time`. Detail sequences and timing for `AnimationGroup` or `Succession`.
        - **Explain the pedagogical purpose** of each element animation. How does it break down complex information, highlight key details, or improve visual clarity for learning? Ensure spatial coherence and minimum spacing.
        - **Coordinate element animations with VGroup transitions:**
            - Clearly describe the synchronization between element animations and VGroup transitions (if any).
            - Specify relative timing and `run_time` to illustrate coordination.
            - **Explain how this animation sequence and coordination creates a pedagogical flow**, guiding the viewer's eye and attention logically through the learning material.

2. **Scene Flow - Pedagogical Pacing and Clarity:** Detail the overall flow of the scene, emphasizing pedagogical effectiveness.
    - **Overall animation sequence, spatial progression for learning:**
        - Describe the complete animation sequence, broken down into pedagogical sub-sections (e.g., "Introducing the Problem", "Step-by-step Solution", "Concept Reinforcement").
        - Outline the spatial progression of objects and VGroups, focusing on how it supports the **pedagogical narrative** and concept development.
        - Ensure a clear and logical visual flow optimized for learning, respecting spatial constraints.
    - **Transition buffers for pedagogical pauses:**
        - Specify `Wait()` times between animation sections for visual separation and **learner processing time**.
        - For each `Wait()`, specify duration and **explain the pedagogical reason** for this buffer (e.g., "Allow viewers time to process the formula", "Create a pause for reflection before moving to the next concept").
    - **Coordinate animation timing with narration for engagement and comprehension:**
        - Describe how animation timings are coordinated with the narration script to **maximize viewer engagement and comprehension**.
        - Specify animation cues within the narration script and explain how these cues are synchronized with animations to **reinforce learning points** at the optimal moment.

[NARRATION]
- **Pedagogical Narration Script:**
    - Provide the full narration script for Scene {scene_number}.
    - **Embed precise animation timing cues** within the narration script (as described before).
    - **The script should be written as if delivered by a knowledgeable and engaging lecturer.** It should:
        - **Clearly explain concepts step-by-step.**
        - **Use analogies and real-world examples to enhance understanding.**
        - **Pose questions to encourage active thinking.**
        - **Summarize key points and transitions.**
        - **Be detailed and knowledge-rich, not just visually descriptive.**
        - **Connect smoothly with the previous and subsequent scenes, acting as a segment within a single, cohesive explanation. 
        - Avoid repetitive introductions or conclusions.** 
        - Consider using phrases like "Building on what we saw in the previous part..." or "Let's now move on to..." to create a sense of continuity.
        - Reference the scene number when appropriate (e.g., "Now, let's explore...").
    - **Crucially, the narration should seamlessly integrate with the animations to create a cohesive and effective learning experience.**
- **Narration Sync - Pedagogical Alignment:**
    - Detail the synchronization strategy between narration and animations, emphasizing **pedagogical alignment**.
    - Explain how narration timing is aligned with animation start/end times to **guide viewer attention to key learning elements precisely when they animate.**
    - Emphasize how narration cues and animation timings work together to **create a synchronized audiovisual presentation that maximizes learning and retention.**

</SCENE_ANIMATION_NARRATION_PLAN>
```
"""

_code_color_cheatsheet = """MUST include the following color definitions if you use the colors in your code. ONLY USE THE COLORS BELOW.

WHITE = '#FFFFFF'
RED = '#FF0000'
GREEN = '#00FF00'
BLUE = '#0000FF'
YELLOW = '#FFFF00'
CYAN = '#00FFFF'
MAGENTA = '#FF00FF'
ORANGE = '#FFA500'
PURPLE = '#800080'
PINK = '#FFC0CB'
BROWN = '#A52A2A'
GRAY = '#808080'
TEAL = '#008080'
NAVY = '#000080'
OLIVE = '#808000'
MAROON = '#800000'
LIME = '#00FF00'
AQUA = '#00FFFF'
FUCHSIA = '#FF00FF'
SILVER = '#C0C0C0'
GOLD = '#FFD700'"""

_prompt_visual_self_reflection = """You are an expert in Manim animations and educational explanation quality assessment. Your task is to analyze a rendered Manim explanation and its corresponding audio narration to identify areas for visual and auditory improvement, ensuring alignment with the provided implementation plan and enhancing the explanation's teaching effectiveness.

Please analyze the provided Manim explanation and listen to the accompanying audio narration. Conduct a thorough self-reflection focusing on the following aspects:

**1. Visual Presentation and Clarity (Automated VLM Analysis & Expert Human-like Judgment):**

*   **Object Overlap:** Does the explanation exhibit any visual elements (text, shapes, equations, etc.) overlapping in a way that obscures information or makes the animation difficult to understand? If possible, Detect regions of significant overlap and highlight them in your reflection.
*   **Out-of-Bounds Objects:** Are any objects positioned partially or entirely outside of the visible frame of the explanation? Identify and report objects that appear to be clipped or outside the frame boundaries.
*   **Incorrect Object Positioning:** Based on your understanding of good visual design and the scene's educational purpose, are objects placed in positions that are illogical, distracting, or misaligned with their intended locations or relationships to other elements as described in the implementation plan? Consider:
    *   **Logical Flow:** Does the spatial arrangement support the intended visual flow and narrative progression of the scene?
    *   **Alignment and Balance:** Is the scene visually balanced? Are elements aligned in a way that is aesthetically pleasing and contributes to clarity, or does the layout appear haphazard or unbalanced?
    *   **Proximity and Grouping:** Are related elements positioned close enough to be visually grouped, and are unrelated elements sufficiently separated to avoid visual clutter?
*   **General Visual Clarity & Effectiveness:** Consider broader aspects of visual communication. Are there any other issues that detract from the explanation's clarity, impact, or overall effectiveness? This could include:
    *   **Visual Clutter:** Is the scene too busy or visually overwhelming at any point? Are there too many elements on screen simultaneously?
    *   **Poor Spacing/Layout:** Is the spacing between elements inconsistent or inefficient, making the scene feel cramped or unbalanced? Are margins and padding used effectively?
    *   **Ineffective Use of Color:** Are color choices distracting, clashing, or not contributing to the animation's message? Are colors used consistently and purposefully to highlight key information?
    *   **Pacing Issues (Visual):** Is the visual animation too fast or too slow in certain sections, hindering comprehension? Are visual transitions smooth and well-timed?
    *   **Animation Clarity:** Are the animations themselves clear and helpful in conveying the intended information? Do animations effectively guide the viewer's eye and focus attention?

**2. Narration Quality:**

*   **Narration Clarity and Pacing:** Is the narration clear, concise, and easy to understand? Is the pacing of the narration appropriate for the visual content and the target audience? Does the narration effectively support the visual explanations?
*   **Narration Sync with Visuals:** Does the narration effectively synchronize with the on-screen visuals? Use VLM to analyze the explanation and identify instances where the narration is misaligned with the animations or visual elements it is describing. Report specific timings of misalignment.

**3. Alignment with Implementation Plan:**

*   **Visual Fidelity:** Does the rendered explanation accurately reflect the visual elements and spatial arrangements described in the provided Manim Implementation Plan? Identify any deviations.
*   **Animation Fidelity:** Do the animations in the explanation match the animation methods and sequences outlined in the Implementation Plan? Report any discrepancies.

Manim Implementation Plan:
{implementation}

Generated Code:
{generated_code}

Output Format 1:
If any issues are identified in visual presentation, audio quality, narration, or plan alignment, please provide a detailed reflection on the issues and how to improve the explanation's visual and auditory quality, narration effectiveness, and code correctness. Then, you must return the updated Python code that directly addresses these issues. The code must be complete and executable.

<reflection>
[Detailed reflection on visual, auditory, narration, and plan alignment issues and improvement suggestions. Include specific timings for narration/visual sync issues and descriptions of object overlap/out-of-bounds problems if detected by VLM.  Be specific about code changes needed for improvement.]
</reflection>
<code>
[Improved Python Code - Complete and Executable - Directly Addressing Reflection Points]
</code>

Output Format 2:
If no issues are found and the explanation and audio are deemed high quality, visually clear, narratively effective, and fully aligned with the implementation plan, please explicitly only return "<LGTM>" as output."""

_prompt_teaching_framework = """# Comprehensive Educational Explanation Content Framework

## 1. Pre-Production Planning

### A. Learning Objectives
- **Knowledge Level (Remember & Understand)**
  Define specific, measurable learning outcomes that can be clearly assessed and evaluated. These outcomes should be concrete and observable, allowing instructors to verify that learning has occurred. Each outcome should be written using precise language that leaves no ambiguity about what constitutes success. For example, \"After watching this explanation, learners will be able to define and explain the concept of variables in programming\" provides a clear benchmark for assessment.

  Action verbs are essential tools for crafting effective learning objectives. Choose verbs like define, list, describe, explain, and identify that clearly indicate the expected cognitive processes. These verbs should align with Bloom's Taxonomy to ensure appropriate cognitive engagement. When applicable, ensure all objectives align with relevant curriculum standards to maintain educational consistency and meet institutional requirements.

- **Comprehension Level (Analyze & Evaluate)**
  Develop objectives that emphasize deeper understanding and connections between concepts. These objectives should go beyond simple recall to require analysis and evaluation of the material. Students should be able to make meaningful connections between different aspects of the content and explain their relationships. For example, \"Learners will be able to compare different data types and explain when to use each\" demonstrates this deeper level of understanding.

  Critical thinking elements should be deliberately incorporated into each objective. Create scenarios that challenge students to apply their knowledge in new contexts. These scenarios should require careful analysis and reasoned decision-making to solve problems effectively. Design learning experiences that encourage students to question assumptions and develop analytical skills.

- **Application Level (Apply & Create)**
  Develop practical skills that directly translate to real-world applications and scenarios. These objectives should focus on hands-on experience and tangible outcomes that demonstrate mastery. For example, \"Learners will be able to write a basic program using variables and proper naming conventions\" provides a clear, actionable goal that can be demonstrated through practical work.

  Include hands-on exercises that allow students to practice and refine their skills in a supported environment. These exercises should gradually increase in complexity to build confidence and competence. Provide real-world context by incorporating authentic scenarios and problems that students might encounter in their future careers or daily lives. This connection to reality helps maintain engagement and demonstrates the immediate value of the learning.

- **Target Audience Analysis**
  Conduct thorough demographic research to understand your learners' backgrounds, ages, and educational levels. This analysis should include assessment of prior knowledge and experience with the subject matter. Consider the technical capabilities of your audience, including their access to necessary tools and technologies.

  Evaluate different learning preferences and styles within your target audience. This understanding helps in designing varied content that appeals to visual, auditory, and kinesthetic learners. Consider cultural and linguistic factors that might impact learning effectiveness. Create content that is inclusive and accessible to learners from diverse backgrounds. Account for varying levels of technical proficiency and ensure your content can be accessed across different devices and platforms.

### B. Content Structure

- **Hook (5-10% of duration)**
  Begin each explanation with a compelling problem or scenario that immediately captures attention and creates interest. This hook should be relevant to the content while being unexpected or intriguing enough to maintain viewer engagement. Use surprising facts or statistics that challenge common assumptions or demonstrate the importance of the topic.

  Share relevant real-world applications that demonstrate immediate value to the learner. For example, \"What if you could automate your daily tasks with just a few lines of code?\" creates immediate interest by connecting to practical benefits. The hook should create an emotional connection and generate curiosity about the upcoming content. Consider using storytelling elements or real-world problems that your audience can relate to.

- **Context (10-15%)**
  Provide clear explanations of how the content relates to real-world situations and problems. This context should help learners understand why the material is relevant to their lives or career goals. Make explicit connections to previous knowledge and experiences that learners can build upon.

  Address the fundamental question of \"Why should I learn this?\" by demonstrating practical applications and benefits. This explanation should be concrete and specific to your audience's needs and interests. Set clear expectations for learning outcomes so students understand what they will gain from the content. Provide a roadmap for the learning journey ahead, including how this content connects to future topics and skills.

- **Core Content (60-70%)**
  Organize material in a logical progression that builds from fundamental concepts to more complex applications. This progression should be carefully planned to avoid overwhelming learners while maintaining engagement. Include multiple examples that demonstrate concepts from different angles and perspectives.

  Use varied teaching methods to accommodate different learning styles and maintain interest. These methods might include demonstrations, animations, code examples, and interactive elements. Implement frequent knowledge checks throughout the content to ensure understanding and maintain engagement. Break complex topics into manageable chunks that can be easily processed and remembered.

- **Practice/Application (10-15%)**
  Create guided practice opportunities that allow learners to apply new knowledge in a supported environment. These practice sessions should include clear instructions and immediate feedback mechanisms. Design interactive elements that engage learners and require active participation rather than passive viewing.

  Develop problem-solving scenarios that challenge learners to apply concepts in realistic situations. These scenarios should gradually increase in complexity as learners gain confidence. Include opportunities for peer learning and collaboration when possible. Provide scaffolded support that can be gradually removed as learners become more proficient.

- **Summary (5-10%)**
  Conclude each explanation with a comprehensive recap of key points and main takeaways. This summary should reinforce the most important concepts and their practical applications. Preview upcoming topics to create anticipation and show how current learning connects to future content.

  Provide specific action items that learners can implement immediately to reinforce their learning. These should be concrete, achievable tasks that build confidence and competence. Share additional resources for further learning, including reference materials, practice exercises, and advanced topics. Create clear connections between the current content and future learning objectives.

## 2. Instructional Design Elements

### A. Cognitive Load Management

- **Chunking Strategies**
  Break complex content into manageable segments of 3-5 minutes each. These chunks should focus on single concepts or closely related ideas that form a coherent unit. Use clear transitions between segments to maintain flow while allowing for cognitive processing.

  Implement progressive complexity by building from basic concepts to more advanced applications. This progression should be carefully planned to avoid overwhelming learners. Include strategic pauses and processing time between segments to allow for reflection and integration of new information. Use visual and verbal cues to signal transitions between different concepts or levels of complexity.

- **Visual Organization**
  Develop a consistent visual hierarchy that guides learners through the content effectively. This hierarchy should use size, color, and placement to indicate the relative importance of different elements. Implement clean, uncluttered designs that minimize distractions and focus attention on key concepts.

  Apply color coding consistently to help learners identify and remember related concepts. This coding should be intentional and meaningful, not merely decorative. Use white space effectively to create visual breathing room and help separate different concepts. Ensure that visual elements support rather than compete with the learning objectives.

- **Information Processing**
  Carefully limit the introduction of new concepts to 5-7 per explanation to prevent cognitive overload. This limitation helps ensure that learners can effectively process and retain the information presented. Develop and use mnemonics and memory aids that help learners organize and remember key concepts.

  Provide visual anchors that learners can reference throughout the content. These anchors should help maintain context and show relationships between concepts. Include strategic review points that reinforce previous learning before introducing new material. Create clear connections between new information and existing knowledge to facilitate better retention.

### B. Engagement Techniques

- **Storytelling Elements**
  Develop a clear narrative flow that carries learners through the content naturally. This narrative should have a beginning, middle, and end that maintains interest and supports learning objectives. Use character-driven examples that learners can relate to and remember.

  Include elements of conflict and resolution to create tension and maintain engagement. These elements should be relevant to the learning objectives and help illustrate key concepts. Maintain an emotional connection through relatable scenarios and authentic problems. Create story arcs that span multiple explanations or modules to maintain long-term engagement.

- **Visual Support**
  Create relevant graphics and animations that enhance understanding of key concepts. These visual elements should be purposeful and directly support learning objectives, not merely decorative. Implement a consistent visual style across all content to maintain professionalism and reduce cognitive load.

  Develop clear infographics that break down complex concepts into understandable components. These should use visual hierarchy and design principles effectively. Use motion and animation thoughtfully to direct attention to important elements and demonstrate processes. Ensure all visual elements are accessible and effectively communicate their intended message.

- **Interactive Components**
  Design and embed quiz questions that check understanding at key points in the content. These questions should be strategically placed to maintain engagement and reinforce learning. Include deliberate pause points that encourage reflection and active processing of information.

  Create coding challenges or practical exercises that allow immediate application of concepts. These should be scaffolded appropriately for the learner's skill level. Provide multiple opportunities for feedback, both automated and instructor-guided when possible. Design interactive elements that encourage experimentation and learning from mistakes.

## 3. Content Delivery Framework

### A. Teaching Sequence

1. **Activate**
   Begin each learning session by connecting to familiar concepts that students already understand. This activation of prior knowledge creates a foundation for new learning and helps students feel confident. Use carefully chosen analogies and metaphors that bridge the gap between known and new concepts. These comparisons should be relevant to your audience's experience and background.

   Create explicit connections to previous learning modules or related concepts. These connections help students build a coherent mental model of the subject matter. Assess prior knowledge through quick activities or questions that reveal students' current understanding. Use this assessment to adjust your teaching approach and address any misconceptions early in the lesson.

2. **Present**
   Deliver clear, structured explanations of new concepts that build upon activated knowledge. These explanations should use precise language while remaining accessible to your target audience. Employ multiple representation methods, including verbal explanations, visual diagrams, and interactive demonstrations. This variety helps accommodate different learning styles and reinforces understanding.

   Provide step-by-step demonstrations that break complex processes into manageable parts. Each step should be clearly explained and connected to the overall objective. Include real-world examples that illustrate practical applications of the concepts. These examples should be relevant to your audience's interests and career goals.

3. **Guide**
   Develop worked examples that demonstrate expert problem-solving processes and thinking strategies. These examples should include explicit explanations of decision-making and common pitfalls to avoid. Share expert thinking processes by \"thinking aloud\" through problem-solving steps. This transparency helps students understand the metacognitive aspects of learning.

   Create scaffolded learning experiences that gradually reduce support as students gain confidence. Begin with highly structured guidance and progressively move toward independent work. Address common misconceptions and errors proactively, explaining why they occur and how to avoid them. Provide clear strategies for troubleshooting and problem-solving.

4. **Practice**
   Design guided exercises that allow students to apply new knowledge with appropriate support. These exercises should be carefully sequenced to build confidence and competence gradually. Include opportunities for independent practice that reinforce learning and build autonomy. Ensure these practice sessions are aligned with learning objectives and provide clear success criteria.

   Create peer learning opportunities that allow students to learn from and teach others. These interactions can reinforce understanding and develop communication skills. Implement immediate feedback mechanisms that help students understand their progress and areas for improvement. This feedback should be specific, constructive, and actionable.

5. **Apply**
   Develop real-world projects that require students to integrate and apply their learning in authentic contexts. These projects should be challenging but achievable, with clear connections to practical applications. Create case studies that illustrate complex scenarios and require critical thinking and problem-solving skills. These studies should reflect realistic situations students might encounter in their careers.

   Design problem-solving scenarios that encourage creative application of knowledge and skills. These scenarios should have multiple possible solutions to encourage innovative thinking. Provide opportunities for creative applications that allow students to extend their learning in personally meaningful ways. Support experimentation and risk-taking in a safe learning environment.

### B. Presentation Techniques

- **Transitions**
   Implement clear verbal cues that signal shifts between concepts or activities. These cues help students maintain orientation and prepare for new information. Design visual transition elements that support cognitive processing and maintain engagement. These elements should be consistent throughout your content to establish familiar patterns.

   Create concept maps that show relationships between different topics and ideas. These maps help students understand how current learning connects to broader concepts. Use progress indicators that help students track their advancement through the material. These indicators should provide a sense of accomplishment and motivation.

- **Multiple Representations**
   Combine text and graphics effectively to convey information through multiple channels. This combination should be purposeful and coordinated to enhance understanding. Integrate audio and visual elements that complement each other and reinforce key concepts. Ensure these elements work together without creating cognitive overload.

   Develop interactive elements that encourage active engagement with the content. These elements should provide immediate feedback and support learning objectives. Include physical demonstrations when appropriate to illustrate concepts in tangible ways. These demonstrations should be clear, visible, and directly relevant to learning goals.

## 4. Assessment Integration

### A. Knowledge Verification
- **Formative Assessment**
   Implement regular quick checks for understanding throughout the learning process. These checks should be low-stakes and provide immediate feedback to both learner and instructor. Design self-assessment prompts that encourage students to reflect on their own learning progress. These prompts should help students develop metacognitive skills and self-awareness.

   Create opportunities for peer discussion and feedback that deepen understanding through explanation and debate. These discussions should be structured to ensure productive exchanges and learning outcomes. Develop reflection questions that help students connect new learning to existing knowledge and future applications. These questions should promote deep thinking and personal connection to the material.

- **Summative Assessment**
   Design project-based assessments that evaluate comprehensive understanding and practical application. These projects should integrate multiple concepts and skills learned throughout the course. Guide students in developing portfolios that demonstrate their learning journey and achievements. These portfolios should include examples of both process and product.

   Create opportunities for skill demonstration that allow students to show mastery in authentic contexts. These demonstrations should reflect real-world applications and standards. Develop knowledge application assessments that require students to transfer learning to new situations. These assessments should evaluate both understanding and adaptability.

### B. Learning Reinforcement
- **Review Strategies**
   Implement spaced repetition techniques that optimize long-term retention of information. This approach should strategically revisit concepts at increasing intervals. Create concept mapping exercises that help students visualize and understand relationships between ideas. These maps should become increasingly complex as understanding develops.

   Guide students in knowledge synthesis activities that combine multiple concepts into coherent understanding. These activities should help students see the bigger picture and make meaningful connections. Design application scenarios that require students to apply knowledge in new and challenging contexts. These scenarios should build confidence and demonstrate practical relevance.

## 5. Technical Considerations

### A. Explanation Production Elements
- **Duration Guidelines**
   Optimize explanation length to maintain engagement while effectively covering necessary content. The ideal duration of 6-12 minutes balances attention span with comprehensive coverage. Implement concept-based segmentation that breaks longer topics into digestible chunks. This segmentation should follow natural breaking points in the material.

   Consider attention span patterns when planning content structure and pacing. Include variety and interaction to maintain engagement throughout longer sessions. Adapt content length to platform-specific requirements and viewing habits. Consider mobile viewing habits and platform limitations in your planning.

- **Quality Standards**
   Ensure professional audio quality through proper equipment and recording techniques. This includes clear voice recording, minimal background noise, and appropriate volume levels. Maintain consistent lighting that enhances visibility and reduces viewer fatigue. Pay attention to both subject lighting and screen content visibility.

   Create clear visual presentations that effectively communicate key concepts. This includes appropriate font sizes, color contrast, and visual hierarchy. Maintain appropriate pacing that allows for processing time while maintaining engagement. Consider your audience's needs and learning objectives when determining pace.

### B. Accessibility Features
- **Universal Design**
   Create content that accommodates multiple learning modalities and preferences. This includes providing information through visual, auditory, and interactive channels. Ensure screen reader compatibility by following accessibility best practices and standards. This includes proper heading structure and alt text for images.

   Implement appropriate color contrast considerations for all visual elements. This ensures content is accessible to viewers with various visual abilities. Provide alternative text descriptions for all important images and graphics. These descriptions should convey the same information as the visual elements.

## 6. Follow-up Resources

### A. Supporting Materials
- **Resource Types**
   Develop comprehensive practice exercises that reinforce learning and build confidence. These exercises should range from basic to advanced, accommodating different skill levels. Create well-documented code samples that demonstrate best practices and common patterns. These samples should include comments explaining key concepts and decisions.

   Compile detailed reference guides that support independent learning and problem-solving. These guides should be easily searchable and regularly updated. Design cheat sheets that provide quick access to essential information and common procedures. These should be concise while including all crucial information.

### B. Implementation Guide
- **Learning Pathways**
   Create clear prerequisite maps that show relationships between different topics and skills. This mapping helps students understand learning dependencies and plan their progress. Provide advanced topic suggestions that help motivated learners extend their knowledge. These suggestions should include resources and guidance for self-directed learning.

   Develop skill progression guides that show clear paths from beginner to advanced levels. These guides should include milestones and checkpoints for measuring progress. Suggest project ideas that allow practical application of learned skills. These projects should be scalable to different skill levels and interests."""

_prompt_fix_error = """You are an expert Manim developer specializing in debugging and error resolution. Based on the provided implementation plan and Manim code, analyze the error message to provide a comprehensive fix and explanation.

Implementation Plan of the Scene:
{implementation_plan}

Manim Code:
```python
{manim_code}
```

Error Message:
{error_message}

Requirements:
1. Provide complete error analysis with specific line numbers where possible.
2. Include exact instructions for every code change.
3. Explain why the error occurred in plain language.
4. If external assets (e.g., images, audio, explanation) are referenced, remove them.
5. **If voiceover is present in the original code, ensure it remains preserved in the corrected code.**
6. Preserve all original code that is not causing the reported error. Do not remove or alter any intentional elements unnecessarily.
7. Follow best practices for code clarity and the current Manim version.

You MUST only output the following format (from <THINKING> to </FULL_CORRECTED_CODE>). You MUST NOT come up with any other format like JSON.

<THINKING>
Error Type: [Syntax/Runtime/Logic/Other]
Error Location: [File/Line number/Component]
Root Cause: [Brief explanation of what caused the error]
Impact: [What functionality is affected]
Solution:
[FIXES_REQUIRED]
- Fix 1: [Description]
  - Location: [Where to apply]
  - Change: [What to modify]
- Fix 2: [If applicable]
...
</THINKING>
<FULL_CORRECTED_CODE>
```python
# Complete corrected and fully implemented Python code
# Include all necessary imports, definitions, and any additional code for the script to run successfully
```
</FULL_CORRECTED_CODE>"""

_prompt_animation_simple = """Given a topic and the context, you need to explain the topic by text.

Also generate a Manim script that visually illustrates a key aspect of {topic} without including explanatory text in the animation itself.
Your text can mention the animation, but it should not be the main focus.
Context about the topic {topic}: {description}.

The animation should focus on:
* Illustrating the significant part of the theorem or concept – Use geometric figures, graphs, number lines, or any relevant visualization.
* Providing an intuitive example – Instead of proving the theorem, show a concrete example or transformation that visually supports understanding.
* Separately, provide a written explanation of the theorem as text that can be displayed outside the animation.

Ensure that:

* The animation is concise.
* The Manim code is compatible with the latest version of community manim.
* The visual elements are clear and enhance understanding.

Please provide the only output as:

1. A text explanation of the theorem.
2. A complete Manim script that generates the animation. Only give the code.

Output format:

(Text Explanation Output)
--- (split by ---)
(Manim Code Output)

Please do not include any other text or headers in your output.
Only use one --- to split the text explanation and the Manim code."""

_prompt_animation_rag_query_generation_fix_error = """You are an expert in Manim (Community Edition) and its plugins. Your task is to transform a complete implementation plan for a Manim animation scene into queries that can be used to retrieve relevant documentation from both Manim core and any relevant plugins. The implementation plan will describe the scene's vision, technical implementation, and animation strategy.

Here is the Text Explanation (Implementation Plan) as the context:

{text_explanation}

The error message will describe a problem encountered while running Manim code. Your queries should include keywords related to the specific Manim classes, methods, functions, and *concepts* that are likely related to the error, including any plugin-specific functionality. Focus on extracting the core concepts, actions, and vocabulary from the error message itself and the code snippet that produced the error. Generate queries that are concise and target different aspects of the documentation (class reference, method usage, animation examples, conceptual explanations) across both Manim core and relevant plugins.

Here is the error message and the code snippet:

**Error Message:**
{error}

**Code Snippet:**
{code}

Based on the error message and the code snippet, generate multiple human-like queries (maximum 5-7) for retrieving relevant documentation to fix this error. Please ensure that the search targets are different so that the RAG can retrieve a diverse set of documents covering various aspects of the error and its potential solutions.

**Specifically, ensure that:**
1. At least 1-2 queries are focused on retrieving information about Manim *function or class usage* that might be causing the error.
2. If the error message or code suggests the use of plugin functionality, include at least 1 query specifically targeting plugin documentation related to the error.
3. Queries should be specific enough to distinguish between core Manim and plugin functionality when relevant.

Output the queries in the following format:
[
    {{"query": "content of query 1", "type": "manim_core/name_of_the_plugin"}},
    {{"query": "content of query 2", "type": "manim_core/name_of_the_plugin"}},
    {{"query": "content of query 3", "type": "manim_core/name_of_the_plugin"}},
    {{"query": "content of query 4", "type": "manim_core/name_of_the_plugin"}},
    {{"query": "content of query 5", "type": "manim_core/name_of_the_plugin"}},
    {{"query": "content of query 6", "type": "manim_core/name_of_the_plugin"}},
    {{"query": "content of query 7", "type": "manim_core/name_of_the_plugin"}},
] """

_prompt_animation_fix_error = """You are an expert Manim developer specializing in debugging and error resolution. Analyze the provided code and error message to provide a comprehensive fix and explanation.

<CONTEXT>
Text Explanation:
{text_explanation}

Manim Code Animation to complement the Text Explanation:
```python
{manim_code}
```

Error Message on code running:
{error_message}
</CONTEXT>

You MUST only output the following format (make sure to include the ```python and ``` in the code):

<ERROR_ANALYSIS>
Error Type: [Syntax/Runtime/Logic/Other]
Error Location: [File/Line number/Component]
Root Cause: [Brief explanation of what caused the error]
Impact: [What functionality is affected]
</ERROR_ANALYSIS>

<SOLUTION>
[FIXES_REQUIRED]
- Fix 1: [Description]
  - Location: [Where to apply]
  - Change: [What to modify]
- Fix 2: [If applicable]
  ...

[CORRECTED_CODE]
```python
# Complete corrected and fully implemented code, don't be lazy
# Include all necessary imports, definitions, and any additional code for the script to run successfully
```

</SOLUTION>

Requirements:
1. Provide complete error analysis with specific line numbers where possible.
2. Include exact instructions for every code change.
3. Ensure that the [CORRECTED_CODE] section contains complete, executable Python code (not just code snippets). Do not assume context from the prompt.
4. Explain why the error occurred in plain language.
5. Include verification steps to confirm the error is resolved.
6. Suggest preventive measures for avoiding similar errors in the future.
7. If external assets (e.g., images, audio, explanation) are referenced, remove them.
8. Preserve all original code that is not causing the reported error. Do not remove or alter any intentional elements unnecessarily.
9. Follow best practices for code clarity and the current Manim version."""

_prompt_scene_technical_implementation = """You are an expert in educational diagram design and Manim (Community Edition), adept at creating spatially accurate static diagrams.

**Important:** This is for a STATIC DIAGRAM only (last-frame PNG rendered with `manim -s`). NO animations, NO explanation, NO audio.

**Reminder:** This technical implementation plan is fully self-contained. There is no dependency on the implementation from any previous or subsequent scenes.

Create a detailed technical implementation plan for Scene {scene_number} (Manim code focused), strictly adhering to defined spatial constraints (safe area margins: 0.5 units, minimum spacing: 0.3 units).

Problem:
{description}

Scene Overview:
{scene_outline}

Scene Vision and Storyboard:
{scene_vision_storyboard}

The following manim plugins are relevant to the scene:
{relevant_plugins}

**Background Color (MANDATORY):**
*   **Use WHITE background**: `self.camera.background_color = WHITE`
*   **Color Scheme Adaptation for White Background:**
    - Primary lines/shapes: Use `BLACK`, `DARK_GRAY`, or `GREY_D` (NOT WHITE)
    - Text/labels: Use `BLACK` or dark colors (NOT WHITE)
    - Highlights: Use saturated colors like `BLUE_D`, `RED_D`, `GREEN_D`, `PURPLE_D`
    - Secondary/auxiliary lines: Use `GREY`, `GREY_B`, or `LIGHT_GREY`
    - Fills: Use light fills with low opacity (e.g., `BLUE` with `fill_opacity=0.2`)
*   **AVOID**: Using `WHITE` for any visible element on white background

**Spatial Constraints (Strictly Enforced):**
*   **Safe area margins:** 0.5 units on all sides from the scene edges. All objects must be positioned within these margins.
*   **Minimum spacing:** 0.3 units between any two Manim objects (measured edge to edge).

**Positioning Requirements:**
1.  All positioning MUST be relative (`next_to`, `align_to`, `shift`) from ORIGIN, safe margins, or other objects. **No absolute coordinates are allowed.**

**Text Guidelines (MINIMAL TEXT POLICY):**
*   **Minimize text usage** - rely primarily on visual elements (shapes, colors, spatial arrangement, mathematical notation).
*   **Only use text for:**
    - Essential labels (e.g., axis labels, point labels like "A", "B")
    - Mathematical expressions/equations
    - Brief annotations when absolutely necessary for understanding
*   **Avoid:** Explanatory paragraphs, titles, lengthy descriptions, or any text that can be conveyed visually.
*   **Text Color:** Always use `BLACK` or dark colors for text on white background.

**Diagrams/Sketches (Highly Recommended):**
*   Include text-based diagrams/sketches for complex layouts to visualize spatial relationships.

**Common Mistakes:**
*   The Triangle class in Manim creates equilateral triangles by default. To create a right-angled triangle, use the Polygon class instead.
*   Using WHITE color elements on WHITE background (invisible elements).
*   Forgetting to set `self.camera.background_color = WHITE` at the start of construct().

**Manim Plugins:**
*   You may use established, well-documented Manim plugins if they offer significant advantages.
*   **If a plugin is used:**
    *   Clearly state the plugin name.
    *   Provide brief justification.
    *   Include comment: `### Plugin: <plugin_name> - <brief justification>`.

**Focus:**
*   Creating spatially correct, visually clear static Manim diagrams.
*   Minimal text - maximum visual communication.
*   Strict adherence to spatial constraints and relative positioning.
*   **Proper contrast on WHITE background.**

You MUST generate the technical implementation plan in the following format:

```xml
<SCENE_TECHNICAL_IMPLEMENTATION_PLAN>
0. **Dependencies**:
    - **Manim API Version**: Target the latest stable Manim release.
    - **Allowed Imports**: `manim`, `numpy`, and any explicitly approved Manim plugins.
    - **No external assets** (images, audio, explanation files).
    - **Background**: WHITE (`self.camera.background_color = WHITE`)

1. **Manim Object Selection & Configuration**:
    - Define all Manim objects (e.g., `MathTex`, `Circle`, `Line`, `Axes`, `Polygon`, `Dot`, `Arrow`, etc.).
    - Specify key parameters: dimensions, color, stroke_width, fill_opacity, etc.
    - **Color Scheme for White Background**:
        - Lines/Strokes: `BLACK`, `DARK_GRAY`, `GREY_D`
        - Text/Labels: `BLACK`, `DARK_GRAY`
        - Highlights: `BLUE_D`, `RED_D`, `GREEN_D`, `PURPLE_D`, `ORANGE`
        - Auxiliary elements: `GREY`, `GREY_B`
        - Fills: Low opacity with any color (opacity 0.1-0.3)
    - **Text Objects (Use Sparingly)**:
        - **`MathTex`**: For mathematical expressions only. Example: `MathTex("x^2 + y^2 = r^2", color=BLACK)`.
        - **`Tex`**: For essential labels only. Example: `Tex("A", color=BLACK)` for point labels.
        - **Mixed text/math**: Use `\\text{{}}` within `MathTex`. Example: `MathTex(r"r = 5\\text{{ units}}", color=BLACK)`.
        - **LaTeX Packages**: If needed, specify and use `TexTemplate` with `add_to_preamble()`.
        - **Font Size Guidelines**:
            - Labels: font_size 20-24
            - Mathematical expressions: font_size 24-28
            - Keep text concise; if unavoidable longer text, reduce size and use line breaks.
    - Confirm all objects are within safe area (0.5 units from edges) with minimum 0.3 units spacing.

2. **VGroup Structure & Hierarchy**:
    - Organize related elements into `VGroup`s for efficient spatial management.
    - Define parent-child relationships with internal spacing of at least 0.3 units.
    - Document purpose for each grouping (e.g., "axis_labels_group", "geometry_group").

3. **Spatial Positioning Strategy**:
    - Use ONLY relative positioning methods (`next_to`, `align_to`, `shift`, `move_to(ORIGIN)`, `to_corner`, `to_edge`).
    - For every object, specify:
        - Reference object (or ORIGIN/edge) used for positioning.
        - Method and direction with `buff` value (minimum 0.3 units).
    - **Layout Sequence**: Define the order of object placement.
    - **Layout Sketch** (recommended):
        ```
        [ASCII representation of final layout]
        ```
    - Verify all elements respect safe margins and spacing.

4. **Visual Hierarchy & Styling**:
    - Define color scheme for visual clarity and emphasis (adapted for WHITE background).
    - Specify which elements are primary (larger, bolder, prominent colors) vs. secondary.
    - Use visual properties (color, size, stroke_width, opacity) to guide viewer's attention.
    - **Contrast Check**: Ensure all elements are clearly visible against WHITE background.

5. **Code Structure (Static Diagram)**:
    - **`construct` method structure for static output:**
        1. **Set background color**: `self.camera.background_color = WHITE`
        2. Create all objects (with appropriate colors for white background)
        3. Position all objects (relative positioning)
        4. Add all objects to scene with `self.add()` (NOT `self.play()`)
    - **No animations**: Use `self.add()` instead of `self.play(Create(...))`, `self.play(Write(...))`, etc.
    - Propose helper functions for creating repeated elements.
    - Include inline comments documenting configuration choices.

6. **Final Object List**:
    - Enumerate all objects that will appear in the final PNG.
    - For each object: type, position reference, key styling (including color), spacing verification.
    - **Color verification**: Confirm no WHITE elements on WHITE background.

***Mandatory Safety Checks***:
    - **Background Color Set**: Verify `self.camera.background_color = WHITE` is included.
    - **Color Contrast**: Verify no WHITE or near-WHITE elements used for visible objects.
    - **Safe Area Enforcement**: All objects (including text bounding boxes) must remain within 0.5 unit margins.
    - **Minimum Spacing Validation**: Confirm minimum 0.3 units spacing between every pair of objects.
    - **Text Minimization**: Verify only essential labels/annotations are included.
    - **Static Output Verification**: Ensure code uses `self.add()` for all objects, no animation calls.
</SCENE_TECHNICAL_IMPLEMENTATION_PLAN>
```
"""


_prompt_rag_query_generation_narration = """You are an expert in generating search queries specifically for **Manim (Community Edition) documentation** (both core Manim and its plugins). Your task is to analyze a storyboard and generate effective queries that will retrieve relevant documentation about narration, text animations, and audio-visual synchronization.

Here is the storyboard:

{storyboard}

Based on this storyboard, generate multiple human-like queries (maximum 10) for retrieving relevant documentation about narration and text animation techniques.

**Specifically, ensure that:**
1. Queries focus on retrieving information about **text animations** and their properties
2. Include queries about **timing and synchronization** techniques
3. If the storyboard suggests using plugin functionality, include specific queries targeting those plugin's narration capabilities

The above storyboard is relevant to these plugins: {relevant_plugins}.
Note that you MUST NOT use the plugins that are not listed above.

You MUST only output the queries in the following JSON format (with json triple backticks):
```json
[
    {{"type": "manim-core", "query": "content of text animation query"}},
    {{"type": "<plugin-name>", "query": "content of plugin-specific query"}},
    {{"type": "manim-core", "query": "content of timing synchronization query"}}
    ...
]
```"""

_prompt_context_learning_animation_narration = """Here are some example animation and narration plans to help guide your planning:

{examples}

Please follow a similar structure while maintaining creativity and relevance to the current scene."""

_prompt_scene_implementation = """You are an expert in educational explanation production and Manim (Community Edition) animation development. Your task is to create a detailed implementation plan for Scene {scene_number}.

<BASE_INFORMATION>
Topic: {topic}
Description: {description}
</BASE_INFORMATION>

<SCENE_CONTEXT>
Scene Overview:
{scene_outline}
</SCENE_CONTEXT>

<IMPLEMENTATION_PLAN>

[SCENE_VISION]
1.  **Overall Narrative**:
    - Describe the overall story or message of the scene. What is the key takeaway for the viewer?
    - How does this scene fit into the larger narrative of the explanation?
    - What is the desired emotional impact on the viewer?

2.  **Learning Objectives**:
    - What specific knowledge or skills should the viewer gain from this scene?
    - How will the visual elements and animations support these learning objectives?
    - What are the key concepts that need to be emphasized?

[STORYBOARD]
1.  **Visual Flow**:
    - Describe the sequence of visual elements and animations in the scene.
    - Provide a rough sketch or description of the key visual moments.
    - How will the scene transition between different ideas or concepts?
    - What is the pacing of the scene? Are there moments of pause or rapid action?

[TECHNICAL_IMPLEMENTATION]
1.  **High-Level Components (VGroups)**:
    - **Identify the main conceptual sections of the scene.** Think of this like outlining chapters in a story or sections in a presentation.
    - **Define the purpose of each high-level component.** What should the viewer learn or understand from each section?
    - **Describe how these components relate to each other and the overall scene flow.** How will you transition between these sections to create a cohesive narrative?
    - **Provide a brief rationale for your choice of high-level components.** Why did you choose these specific sections?

2.  **VGroup Hierarchy**:
    - **For each high-level component, define a parent VGroup.** This VGroup will act as a container for all elements within that section.
    - **Break down each parent VGroup into nested VGroups for sub-components as needed.** Think about logical groupings of elements.
    - **Specify the relative positioning of these VGroups within the scene using `next_to()`, `align_to()`, and `shift()` where possible.** How will the parent VGroups be arranged on the screen relative to each other? (e.g., stacked vertically, side-by-side, etc.) Prioritize relative positioning using the following references:
        - `ORIGIN`: the center of the scene
        - scene margins (e.g., corners, edges)
        - other VGroups as references.
        - **MUST NOT use absolute coordinates.**
    - **Define the scale relationships between different levels of the VGroup hierarchy.** Will sub-VGroups inherit scale from parent VGroups? How will scaling be managed to maintain visual consistency?
    - **Provide a brief rationale for your VGroup hierarchy.** Why did you choose this specific structure?

    For each VGroup level (from high-level down to sub-components):
    - Name: [Descriptive name for the VGroup, e.g., "TitleSection", "ProblemStatementGroup", "Explanation1Group"]
    - Purpose: [What is the purpose of this VGroup? What should the viewer learn or understand from this VGroup?]
    - Contents: [List all child VGroups and individual elements (Text, MathTex, Shapes, etc.) that belong to this VGroup.]
    - Positioning:
        * Reference: [Specify what this VGroup is positioned relative to. Do not use absolute coordinates.]
        * Alignment: [How is it aligned relative to the reference? Use `align_to()` with options like `UP`, `DOWN`, `LEFT`, `RIGHT`, `ORIGIN`, etc.]
        * Spacing: [Describe any spacing considerations relative to sibling VGroups or elements within the parent. Use `buff` argument in `next_to()` or `arrange()`. Refer to the defined minimum spacing value.]
    - Scale: [Specify the scale of this VGroup relative to its parent VGroup. Use relative scaling factors (e.g., 1.0 for same scale, 0.8 for smaller).]
    - Rationale: [Explain the reasoning behind the structure and organization of this VGroup. Why did you group these elements together?]

3.  **Element Specification**:
    For each individual element (Text, MathTex, Shapes, etc.) within a VGroup:
    - Name: [Descriptive name for the element, e.g., "ProblemTitleText", "Equation1", "HighlightCircle"]
    - Type: [Manim object type. Examples: Text, MathTex, Circle, Rectangle, Arrow, Line, etc.]
    - Parent VGroup: [Specify the VGroup this element belongs to. This establishes the hierarchical relationship.]
    - Positioning:
        * Reference: [Specify what this element is positioned relative to. Use its parent VGroup, other elements, `ORIGIN`, or scene margins as references. Do not use absolute coordinates.]
        * Alignment: [How is it aligned within its parent VGroup? Use `align_to()` or `next_to()` with appropriate directions, e.g. `UP`, `DOWN`, `LEFT`, `RIGHT`, `ORIGIN`, `UL`, `UR`, `DL`, `DR`]
        * Spacing: [If applicable, describe spacing relative to other elements using `buff` in `next_to()`. Refer to the defined minimum spacing value.]
    - Style Properties:
        * Color: [Hex code or named color (e.g., "RED", "BLUE"). Use hex codes for specific colors. e.g., #FF0000 for red]
        * Opacity: [Value between 0 and 1. 1 for fully opaque, 0 for fully transparent.]
        * Stroke Width: [Specify stroke width using levels: `thin`, `medium`, or `thick`.]
        * Font: [Font family name, if applicable.]
        * Font Size: [Specify font size using levels: `heading1`, `heading2`, `heading3`, `heading4`, `heading5`, `heading6`, or `body`. Refer to the defined font size levels.]
        * Fill Color: [Hex code for fill color, if applicable.]
        * ... [Include any other relevant style properties]
    - Z-Index: [Integer value for layering order within the VGroup. Higher values are on top.]
    - Required Imports: [List specific Manim classes that need to be imported to create this element. e.g., `from manim import Text, Circle`]

[ANIMATION_STRATEGY]
1.  **VGroup Transitions**:
    - **Define how parent VGroups will transition onto and off of the scene, and between different sections.** Describe the movement patterns for these high-level groups. Examples: 'Slide in from left', 'Fade in and scale up', 'Move to top of screen'.
    - **Specify the timing and coordination of VGroup transitions.** How long will each transition take? Will transitions overlap or be sequential?
    - **Describe any transformation sequences applied to VGroups during transitions.** Will VGroups rotate, scale, or change shape during transitions?

2.  **Element Animations**:
    - **Define the animations for individual elements within each VGroup.** What animations will bring each element to life? Examples: 'Write in text', 'Draw a circle', 'Highlight an equation', 'Fade in an image'.
    - **Group related element animations using Manim's animation grouping features (e.g., `AnimationGroup`, `Succession`).** Explain how these groups will be used to create cohesive animation sequences.
    - **Coordinate element animations with parent VGroup movements and transitions.** Ensure element animations are synchronized with the overall scene flow.
    - **Specify the timing of element animations relative to VGroup transitions and other element animations.** Create a timeline or sequence of animations.

3.  **Scene Flow**:
    - **Describe the overall animation sequence for the entire scene.** Outline the order in which VGroups and elements will be animated.
    - **Specify transition buffers or pauses between major sections of the scene.** How much time will be left between animations for the viewer to process information?
    - **Consider how the animation timing will coordinate with the narration (if narration is planned).** Animations should complement and reinforce the spoken content.

[NARRATION]
- **Narration Script:** [Provide the full script for the narration, including timing cues or markers for when specific animations should occur. The script should be clear, detailed, and engaging, and should align with the visual elements and animations.]
- **Narration Sync:** [Describe how the narration should be synchronized with the animations. Specify how timing cues in the narration script will be used to trigger animations. Are there specific points where the narration and animations should be perfectly synchronized? Explain how you will achieve this synchronization.]

[VIEWER_EXPERIENCE]
1.  **Cognitive Load**:
    - How will you manage the amount of information presented at any given time?
    - Are there any complex concepts that need to be broken down into smaller steps?
    - How will you use visual cues to guide the viewer's attention?

2.  **Pacing**:
    - Is the pacing of the scene appropriate for the content?
    - Are there moments where the viewer needs time to pause and reflect?
    - How will you use animation timing to control the pace of the scene?

3.  **Accessibility**:
    - How will you ensure that the scene is accessible to viewers with different needs?
    - Are there any specific considerations for color contrast or text readability?

[TECHNICAL_CHECKS]
- **VGroup boundary validation:** Ensure all elements are contained within their intended VGroup boundaries and are not overflowing unexpectedly.
- **Hierarchy scale consistency:** Verify that scaling is applied consistently throughout the VGroup hierarchy and that text and elements remain readable at all scales.
- **Animation coordination between levels:** Check that animations at different VGroup levels are coordinated and do not clash or look disjointed.
- **Performance optimization for nested groups:** Consider the performance implications of deeply nested VGroups and optimize structure and animations for smooth playback.
- **Text readability:** Ensure all text elements are legible in terms of size, color contrast, and positioning.
- **Color contrast:** Verify sufficient color contrast between text and background, and between different visual elements for accessibility.
- **Animation smoothness:** Check for any jerky or abrupt animations and refine timing and easing for smoother transitions.

</IMPLEMENTATION_PLAN>

Requirements:
1. All elements must stay within safe area margins
2. Maintain minimum spacing between objects: [value]  (This value is defined in the project settings)
3. Use relative positioning when possible, leveraging `next_to()`, `align_to()`, and `shift()`. Only reference positions relative to `ORIGIN`, scene margins, or other object reference points. Do not use absolute coordinates.
4. Include transition buffers between animations
5. Specify z-index for overlapping elements
6. All colors must use hex codes or named colors
7. Define scale relative to base unit
8. No external dependencies
9. Currently, there are no images or other assets available locally or remotely for you to use in the scene. Only include elements that can be generated through manim.
10. **Do not generate any code in this plan, except for illustrative examples where necessary. This plan is for outlining the scene and should not include any python code.**
11. **The purpose of this plan is to be a detailed guide for a human to implement the scene in manim.**"""

_prompt_visual_fix_error = """You are an expert in Manim animations. Your task is to ensure that the rendered animation frame (image) aligns with the intended teaching content based on the provided implementation plan.

Instructions:
Evaluate whether the object coordinates and positions in the image match the described plan and educational purpose.
The implementation plan serves as a reference, but your primary goal is to verify that the rendered animation frame supports effective teaching.
For example:
* If the object is supposed to be at the top of the screen, but it is at the bottom, you need to adjust the position.
* If the object is supposed to be at the left side but it is too far to the left, you need to adjust the position.
* If the two objects are not supposed to be overlapped but it is overlapped, you need to adjust the positions.

If adjustments are needed, provide the complete code of the adjusted version.
If the current code is correct, return it as is.

Manim Implementation Plan:
{implementation}

Generated Code:
{generated_code}

Return the complete code of the adjusted version if the code needs to be updated. If the code is correct, only return "<LGTM>" as output.
"""

_banned_reasonings = """evaluation cannot
can't assist
cannot assist
can't provide
cannot provide
can't evaluate
cannot evaluate
cannot be evaluated
cannot be rated
cannot be completed
cannot be assessed
cannot be scored
cannot be conducted
unable to evaluate
do not have the capability
do not have the ability
are photographs and not AI-generated
unable to provide the evaluation"""


_prompt_code_generation = """You are an expert Manim (Community Edition) developer for educational content across multiple disciplines (mathematics, physics, chemistry, biology, and more). Generate executable Manim code to produce a **static diagram** (last-frame PNG rendered with manim -s), strictly adhering to the provided technical implementation plan and spatial constraints.

**Input Context:**

Problem:

{description}

Scene Outline:

{scene_outline}

Scene Technical Implementation:

{scene_implementation}

---

## CORE RULES

1. **Static Output Only:** Render with manim -s. Use self.add() for all objects. Animations are optional and minimal. The **final frame** must show the complete diagram.

2. **Class Name:** Must be exactly Scene{scene_number}. Inherit from Scene (or MovingCameraScene only if camera movement is needed). Do NOT inherit from VoiceoverScene.

3. **No Audio:** Do NOT import or use manim_voiceover, VoiceoverScene, or any audio-related logic.

4. **No External Assets:** No image, audio, or explanation files. Manim built-ins and approved plugins only.

5. **No Main Block:** No if __name__ == "__main__":.

6. **Complete Code:** Generate full, runnable code with all helper functions. Do not leave stubs or placeholders.

---

## SPATIAL CONSTRAINTS (Strictly Enforced)

- **Safe area margins:** 0.5 units from all scene edges.

- **Minimum spacing:** 0.3 units between any two objects (edge to edge).

- **Positioning:** Use ONLY relative methods next_to, align_to, shift, move_to(ORIGIN), to_corner, to_edge). **No hardcoded absolute coordinates.**

- If a potential constraint violation is detected, add a # WARNING: check spacing comment.

---

## VISUAL STYLE

- **Background:** self.camera.background_color = WHITE at the start of construct().

- **No WHITE elements:** All visible objects must contrast against white background.

- **Recommended colors:**

  - Lines/strokes: BLACK, DARK_GRAY, GREY_D

  - Text/labels: BLACK, DARK_GRAY

  - Highlights: BLUE_D, RED_D, GREEN_D, PURPLE_D, ORANGE

  - Fills: low opacity (0.1–0.3)

- **Discipline-specific color conventions** (follow when applicable):

  - Physics: weight RED_D, normal BLUE_D, friction ORANGE, tension GREEN_D

  - Chemistry: O RED, N BLUE_D, C DARK_GRAY, H GREY, bonds BLACK

  - Biology: membrane GOLD_D, nucleus PURPLE_D, mitochondria RED_D, chloroplast GREEN_D

  - Mathematics: constructions BLUE_D, auxiliary GREY dashed, key results RED_D

---

## TEXT & LABELS

- **Minimal text.** Diagrams are visual-first; all explanation belongs in the Markdown document, not the diagram.

- **Use MathTex** for math/science expressions. **Use Tex** for short labels only.

- **Mixed text+math:** MathTex(r"\\text{{Area}} = \\pi r^2", color=BLACK)

- **Font sizes:** Labels 20–24, expressions 24–28.

- **NO explanatory text, titles, descriptions, or sentences in the diagram.** Only: point labels, axis labels, coordinates, measurements, force symbols, chemical symbols, short structure names.

---

## LaTeX PACKAGES

If specialized notation is needed, create a TexTemplate:

```python

my_template = TexTemplate()

my_template.add_to_preamble(r"\\usepackage[version=4]{{mhchem}}")  # chemistry

# or: r"\\usepackage{{siunitx}}"  # physics units

self.tex_template = my_template

```

Then pass to MathTex(..., tex_template=self.tex_template).

---

## CODE STRUCTURE

- Use a **helper class** Scene{scene_number}_Helper) for reusable object creation functions.

- Organize construct() into **labeled stages** with comments.

- Use **VGroups** to manage related elements and enforce spacing.

- Add **concise comments** for spatial logic and discipline-specific conventions.

---

## COMMON MISTAKES TO AVOID

- Triangle creates equilateral triangles. Use Polygon for arbitrary triangles.

- WHITE elements on WHITE background → invisible.

- Labels overlapping the objects they describe → increase buff.

- Force arrows not at point of application.

- Wrong bond angles in molecular structures (tetrahedral 109.5°, trigonal planar 120°, linear 180°).

- Missing self.camera.background_color = WHITE.

---

## MANIM PLUGINS

Approved plugins are pre-imported. Use them when they simplify implementation.

When using a plugin, add: ### Plugin: <name> - <brief reason>

---

You MUST output code in this format:

<CODE>

```python

from manim import *

from manim import config as global_config

# Plugin imports (pre-imported, do not modify)

from manim_circuit import *

from manim_physics import *

from manim_chemistry import *

from manim_dsa import *

from manim_ml import *

class Scene{scene_number}_Helper:

    \"\"\"Helper class for reusable diagram components.\"\"\"

    def __init__(self, scene):

        self.scene = scene

    def get_center_of_edges(self, polygon, buff=SMALL_BUFF * 3):

        \"\"\"Calculate offset center points of each polygon edge for label placement.\"\"\"

        vertices = polygon.get_vertices()

        n = len(vertices)

        result = []

        for i in range(n):

            v1, v2 = vertices[i], vertices[(i + 1) % n]

            edge_center = (v1 + v2) / 2

            edge_vec = v2 - v1

            normal = np.array([-edge_vec[1], edge_vec[0], 0])

            normal = normal / np.linalg.norm(normal) * buff

            result.append(edge_center + normal)

        return result

    # Add discipline-specific helper methods as needed by the technical plan

    # e.g., create_force_arrow(), create_atom(), create_bond(),

    #        create_cell_organelle(), create_punnett_square(), etc.

class Scene{scene_number}(Scene):

    def construct(self):

        self.camera.background_color = WHITE

        helper = Scene{scene_number}_Helper(self)

        # --- LaTeX template setup (if needed) ---

        # my_template = TexTemplate()

        # my_template.add_to_preamble(r"\\usepackage[version=4]{{mhchem}}")

        # self.tex_template = my_template

        # --- Stage 1: [describe] ---

        # Create and position objects using helper functions

        # Use self.add() to place all objects

        # --- Stage 2: [describe] ---

        # Add supporting elements, annotations, labels

        pass  # Replace with full implementation

```

</CODE>

"""


_prompt_rag_query_generation_code = """You are an expert in generating search queries specifically for **Manim (Community Edition) documentation** (both core Manim and its plugins). Your task is to transform a complete implementation plan for a Manim explanation scene into effective queries that will retrieve relevant information from Manim documentation. The implementation plan describes the scene's vision, storyboard, technical implementation, and animation/narration strategy.

Here is the complete scene implementation plan:

{implementation_plan}

Based on the complete implementation plan, generate multiple human-like queries (maximum 10) for retrieving relevant documentation. Please ensure that the search targets are different so that the RAG can retrieve a diverse set of documents covering various aspects of the implementation.

**Specifically, ensure that:**
1.  At least some queries are focused on retrieving information about **Manim function usage** in scenes. Frame these queries to target function definitions, usage examples, and parameter details within Manim documentation.
2.  If the implementation suggests using plugin functionality, include at least 1 query specifically targeting **plugin documentation**.  Clearly mention the plugin name in these queries to focus the search.
3.  Queries should be specific enough to distinguish between core Manim and plugin functionality when relevant, and to target the most helpful sections of the documentation (API reference, tutorials, examples).

The above implementation plans are relevant to these plugins: {relevant_plugins}.
Note that you MUST NOT use the plugins that are not listed above.

You MUST only output the queries in the following JSON format (with json triple backticks):
```json
[
    {{"type": "manim-core", "query": "content of function usage query"}},
    {{"type": "<plugin-name>", "query": "content of plugin-specific query"}},
    {{"type": "manim-core", "query": "content of API reference query"}}
    ...
]
```"""

