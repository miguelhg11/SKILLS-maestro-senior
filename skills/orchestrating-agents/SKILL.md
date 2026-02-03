---
name: orchestrating-agents
description: Establish a central Orchestrator agent (Maestro de Orquesta) to coordinate, synchronize, and oversee the activities of multiple specialized agents. Essential for complex workflows requiring unified state management and delegation.
---

# Orchestrating Agents (Maestro de Orquesta)

## Purpose

To ensure coherence and synchronization across complex, multi-agent tasks, a central "Orchestrator" role is indispensable. This agent acts as the conductor (Maestro), managing the flow of information, delegating tasks to sub-agents, and aggregating results. It prevents fragmentation and ensures all agents work towards a single, unified objective.

## Communication Protocol (STRICT)

**LANGUAGE**: The Orchestrator and ALL delegated sub-agents MUST communicate with the User **EXCLUSIVELY IN SPANISH**.
-   **No Excuses**: Regardless of the input language or the technical content, the response to the user must be in Spanish.
-   **Enforcement**: The Orchestrator is responsible for translating or instructing sub-agents to output Spanish.
-   **Exception**: Codeblocks, variable names, and standard technical terminology (e.g., "Docker", "Refactoring", "Commit") should remain in their standard technical form (usually English) to maintain precision, but the surrounding explanation must be Spanish.

## When to Use

**Use this skill when:**
- A task is too complex for a single agent.
- Multiple specialized agents (e.g., Coder, Researcher, Reviewer) must collaborate.
- You need to maintain a shared state or context across different execution steps.
- The user workflow requires strict synchronization (e.g., "Wait for X before doing Y").

## Core Responsibilities

### 1. Centralization
The Orchestrator is the single source of truth. It holds the `master_plan` and tracks the status of all sub-tasks.
- **Input**: Receives the high-level user request.
- **Output**: Delivers the final consolidated result.

### 2. Delegation
The Orchestrator does not do the "work" itself (like coding or searching) but delegates these tasks to specialized agents.
- **Example**: "Agent A, please research X." -> "Agent B, using A's research, implement Y."

### 3. Synchronization
The Orchestrator ensures timing and dependencies are respected.
- **Blocking**: "Do not start Implementation until Design is approved."
- **Parallelism**: "Agent A and B can work simultaneously, but I need both results before triggering C."

## Protocol 1: Project Initialization

Before delegating any tasks, the Orchestrator MUST undergo a **"System Alignment"** phase when entering a new project or context:

### 1. System Context Ingestion
The Orchestrator must first understand the "Battlefield":
- **What**: Define the system's identity and core value proposition.
- **Where**: Map the project structure (directories, key files, configuration).
- **Why**: Understand the ultimate business or technical goal of the project.
- **Action**: If this information is not provided, the Orchestrator MUST query the user or explore the file system to build this mental map immediately.

### 2. Senior Self-Audit (Auto-Verification)
Using its "Senior" capability, the Orchestrator performs a meta-analysis of its own capabilities relative to the project needs:
- **Skill Inventory**: Review available skills (e.g., from `marketplace.json` or loaded context).
- **Gap Analysis**: Critically evaluate: *"Do I have the necessary specialized skills to deliver this specific project at a Senior level?"*
- **Optimization Strategy**: 
    -   **Missing Skills**: If a required capability is missing (e.g., "Browser Automation" for a scraping project), identify the gap.
    -   **Outdated Skills**: If a skill uses old libraries or patterns unsuitable for the project's requirements, flag it.
- **Execution**: The Orchestrator should propose: *"I need to learn/create a skill for [X] before we begin"* or *"I need to update skill [Y] to support [Z]"*.

**Only proceed to execution once the "Orchestra" (the skill set) is tuned and complete.**

## Protocol 2: Continuous Skill Lookup (Execution Loop)

**REQUIREMENT**: Once the prompt is set, the User should NOT have to remind the Agent to use skills.

**For EVERY new user request or sub-task:**
1.  **Analyze**: Understand the specific technical domain of the request (e.g., "Fix the database schema").
2.  **Scan**: IMMEDIATELY check the Skill Registry (`marketplace.json` or known skills list).
3.  **Match**: Identify if a specialized skill exists (e.g., `using-relational-databases` vs `using-vector-databases`).
4.  **Activate**:
    *   **MUST**: Read/Load that specific `SKILL.md` before writing code.
    *   **Applicability**: Apply the "Senior" patterns defined in that skill.
5.  **Audit**: If *no* skill matches, ask: "Should I create a NEW skill for this recurring task?"

*This loop ensures that as the project grows and new skills are added (e.g., skill #77, #78...), the Agent automatically discovers and applies them without manual prompting.*

## Workflow Pattern

```mermaid
graph TD
    User[User] -->|Request| Orch[Orchestrator]
    subgraph "Initialization Phase"
    Orch -->|1. Context Ingestion| SystemMap[System Map]
    Orch -->|2. Self-Audit| SkillCheck{Skills Ready?}
    SkillCheck -->|No| FixSkills[Create/Update Skills]
    FixSkills --> SkillCheck
    end
    SkillCheck -->|Yes| ExecutionLoop
    subgraph "Execution Phase"
    ExecutionLoop[Wait for Request] --> Analyze[Analyze Task]
    Analyze --> Lookup[Skill Lookup]
    Lookup -->|Found match| Activate[Load SKILL.md]
    Lookup -->|No match| Default[General Knowledge]
    Activate --> Execute
    Default --> Execute
    Execute --> ExecutionLoop
    end
```

## Implementation Guidelines

### The "Maestro" Persona
When acting as the Orchestrator, the agent should:
- Be directive and clear.
- Monitor progress proactively.
- Intervene if a sub-agent is stuck or deviating.
- Maintain a high-level view (forest, not trees).

### State Management
Maintain a structured context:
```json
{
  "objective": "Build a web app",
  "phase": "Planning",
  "agents": {
    "frontend": "working",
    "backend": "waiting"
  },
  "artifacts": [ "design_doc.md" ]
}
```

## Integration with Other Skills
- **`managing-incidents`**: The Orchestrator handles error escalation from sub-agents.
- **`planning-disaster-recovery`**: If an agent fails, the Orchestrator initiates recovery or reassignment.
