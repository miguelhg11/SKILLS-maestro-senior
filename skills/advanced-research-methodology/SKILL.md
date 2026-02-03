---
name: advanced-research-methodology
description: Protocols for advanced research, critical source evaluation (anti-hallucination), and complex problem solving (Cynefin/A3). Use this when rigorous truth-seeking or methodology is required.
triggers:
  - "verified research"
  - "deep analysis"
  - "evaluate sources"
  - "investigate complex problem"
  - "apply scientific method"
---

# Advanced Research Methodology (Cognitive Seniority)

## Purpose
To equip agents with **Epistemological Rigor**. This skill shifts the focus from "Accessing Data" to **"Evaluating Truth"** and **"Structuring Chaos"**. It is the antidote to AI hallucinations and superficial analysis.

## Protocol 1: The Problem Framework (Cynefin)
Before acting, the Agent MUST classify the problem domain to select the strategy:

| Domain | Characteristics | Agent Strategy |
| :--- | :--- | :--- |
| **Clear** | Cause & Effect are obvious. Best practices exist. | **Sense -> Categorize -> Respond** (Standard Ops) |
| **Complicated** | Requires expert analysis. Multiple "good" answers. | **Sense -> Analyze -> Respond** (Deep Work) |
| **Complex** | No right answers, only emergent ones. Unknown unknowns. | **Probe -> Sense -> Respond** (Experimentation) |
| **Chaotic** | Crisis. No clear relationships. | **Act -> Sense -> Respond** (Stabilization) |

**Rule**: Do not apply "Best Practices" (Clear) to "Complex" problems.

## Protocol 2: Source Evaluation (The Truth Filter)
ALL external data must pass these filters before being accepted as "Fact".

### 1. SIFT Method (For Web/Digital)
- **STOP**: Check your own bias. Are you accepting this because it fits the prompt?
- **INVESTIGATE**: Who is the author? What is their agenda?
- **FIND**: Cross-referencing. Do other independent, high-authority sources say the same?
- **TRACE**: Go to the primary source. Don't rely on interpretations of interpretations.

### 2. CRAAP Test (For Academic/Formal)
- **Currency**: Is it outdated? (Crucial for Tech).
- **Relevance**: Does it actually answer the specific question?
- **Authority**: Credentials of the author/publisher.
- **Accuracy**: Is it supported by verifiable evidence?
- **Purpose**: Is it objective or persuasive/sales-oriented?

## Protocol 3: OSINT & Deep Search (Retrieval Standards)
When searching, the Agent must use advanced operators to filter noise:
- **`site:`**: Restrict to authoritative domains (e.g., `site:edu`, `site:github.com`).
- **`filetype:`**: Find deep web documents (`filetype:pdf`, `filetype:csv`).
- **Logic**: Use `AND`, `OR`, `-` (NOT) to refine queries precisely.

## Protocol 4: Problem Solving (Lean/A3)
For organizational or systematic problems, use the **A3 Logic**:
1. **Problem Definition**: What is happening vs. What should happen.
2. **Root Cause Analysis**: 5 Whys / Fishbone Diagram.
3. **Countermeasures**: Proposed solutions addressing root causes.
4. **Verification**: How will we know it worked?

## Workflow Integration
1. **Receive Request**: "Analyze X technology".
2. **Apply Cynefin**: Is this a known tech (Clear) or emerging/unstable (Complex)?
3. **Deep Search**: Use OSINT operators.
4. **Filter**: Apply SIFT/CRAAP to results. discard weak sources.
5. **Synthesize**: Report findings with confidence levels based on evidence quality.
