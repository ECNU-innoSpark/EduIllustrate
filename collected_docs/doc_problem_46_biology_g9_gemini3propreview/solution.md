# problem_46_biology_g9

**Problem Statement:**

As shown in the figure, a schematic represents the structure of a certain gene (labeled with $^{15}$N) in a eukaryotic cell. In this gene, Cytosine (C) accounts for 30% of all bases. Which of the following statements is correct?

A. Helicase acts on both sites ① and ②.
B. In one nucleotide strand of this gene, the ratio (C+G)/(A+T) is 3:2.
C. If the Thymine (T) after site ① changes to Adenine (A), after $n$ replications, the altered gene accounts for 1/4 of the total.
D. After this gene replicates 3 times in a culture medium containing $^{14}$N, the DNA molecules containing $^{14}$N account for 3/4 of the total.

**Solution Approach:**

We will analyze the DNA structure shown in the diagram to identify the chemical bonds at sites ① and ②. Then, we will apply Chargaff's rules to calculate base ratios for statement B. Finally, we will use the principles of semi-conservative replication to evaluate the outcomes of mutation (statement C) and isotope labeling (statement D).

![](scene1.png)

**Step 1: Analyzing Enzyme Action Sites (Option A)**

Let's identify the structures labeled in the diagram:
- **Site ①:** The arrow points to the connection between the phosphate group of one nucleotide and the sugar of the next. This is a **phosphodiester bond**, which forms the stable backbone of the DNA strand.
- **Site ②:** The arrow points to the connection between complementary bases (e.g., between C and G). These are **hydrogen bonds**, which hold the two strands together.

**Function of Helicase:**
Helicase is an enzyme involved in DNA replication that "unzips" the double helix. It does this by breaking the **hydrogen bonds** between base pairs to separate the strands. Therefore, helicase acts on **site ②**.

Enzymes that act on site ① (phosphodiester bonds) include restriction enzymes (which cut DNA) and DNA ligase (which joins DNA).

*Conclusion:* Statement A claims helicase acts on both ① and ②, which is **incorrect**.

![](scene2.png)

**Step 2: Calculating Base Ratios (Option B)**

We are given that Cytosine (C) accounts for 30% of the total bases in the gene.

According to base-pairing rules (Chargaff's rules):
- The amount of C equals the amount of G ($C = G$).
- The amount of A equals the amount of T ($A = T$).

**Calculations:**
1. Since $C = 30\%$, then $G = 30\%$.
2. The sum of C and G is $30\% + 30\% = 60\%$.
3. The remaining bases are A and T. Total bases = 100%.
$A + T = 100\% - (C + G) = 100\% - 60\% = 40\%$.
4. Since $A = T$, then $A = 20\%$ and $T = 20\%$.

**Ratio Calculation:**
The ratio of (C + G) to (A + T) for the entire DNA molecule is:
$$ \frac{C+G}{A+T} = \frac{60\%}{40\%} = \frac{3}{2} $$

**Single Strand Property:**
Because of complementary base pairing, the number of $(C+G)$ on one strand corresponds to the number of $(G+C)$ on the complementary strand. Similarly, $(A+T)$ on one strand corresponds to $(T+A)$ on the other. Therefore, the ratio $\frac{C+G}{A+T}$ is constant for both the double strand and each individual single strand.

*Conclusion:* Statement B states the ratio is 3:2, which is **correct**.

![](scene3.png)

**Step 3: Analyzing Replication with Isotopes (Option D)**

The gene is initially labeled with $^{15}$N (both strands). It replicates 3 times in a medium containing $^{14}$N.

**Replication Tracking:**
- **Start (Gen 0):** 1 molecule, both strands $^{15}$N.
- **Round 1:** 2 molecules. Each has one original $^{15}$N strand and one new $^{14}$N strand. (All contain $^{14}$N).
- **Round 2:** 4 molecules. The 2 $^{15}$N strands are conserved in 2 hybrid molecules. The other 2 molecules are purely $^{14}$N.
- **Round 3:** 8 molecules ($2^3$). The 2 original $^{15}$N strands still exist, forming 2 hybrid molecules ($^{15}$N/$^{14}$N). The remaining $8 - 2 = 6$ molecules consist entirely of new strands ($^{14}$N/$^{14}$N).

**Evaluating the Statement:**
The question asks for the proportion of DNA molecules **containing** $^{14}$N.
- Hybrid molecules ($^{15}$N/$^{14}$N) contain $^{14}$N.
- Pure molecules ($^{14}$N/$^{14}$N) contain $^{14}$N.
- Since every newly synthesized strand is $^{14}$N, **every single resulting DNA molecule** (8 out of 8) contains at least one $^{14}$N strand.
- Proportion = $8/8 = 100\%$.

Statement D claims this proportion is 3/4 (which would be the proportion of molecules containing *only* $^{14}$N). Therefore, Statement D is **incorrect**.

**Step 4: Analyzing Mutation (Option C)**

If the base T at site ① changes to A, we have a point mutation on one strand.
- **Before Replication:** One strand has the mutation (A), the other has the original sequence (complementary to T, which is A). *Note: This creates a mismatch or represents a change in the template.*
- **Replication:** The DNA strands separate.
1. The mutated strand (A) serves as a template and pairs with T, creating a mutant gene (A-T pair).
2. The original complementary strand serves as a template and creates the original gene sequence.
- **Result:** 50% of the daughter molecules will carry the mutation, and 50% will be normal. This 1/2 ratio persists through subsequent generations ($n$ replications) because the mutant line breeds true and the normal line breeds true.

Statement C claims the altered gene accounts for 1/4. This is **incorrect**; it should be 1/2.

**Final Conclusion**

- **A is False:** Helicase only acts on hydrogen bonds (②), not phosphodiester bonds (①).
- **B is True:** The base ratio (C+G)/(A+T) is 3:2 for the gene and its individual strands.
- **C is False:** A mutation on one strand results in 50% (1/2) of the progeny carrying the mutation, not 1/4.
- **D is False:** All resulting DNA molecules (100%) contain the new isotope $^{14}$N, not 3/4.

**Correct Answer:** B

