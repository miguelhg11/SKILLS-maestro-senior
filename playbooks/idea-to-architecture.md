---
name: playbook-idea-to-architecture
description: A step-by-step guide to transforming a vague idea into a technical specification. Orchestrates Research, API Design, and Infrastructure skills.
---

# Playbook: From Idea to Architecture

## Purpose
To move from "I have an idea" to "I have a spec" without skipping critical validation steps. This playbook orchestrates the use of multiple atomic skills to ensure a solid foundation.

## Phase 1: Deep Research (The "Why" & "What")
**Skill**: `advanced-research-methodology` & `notebooklm-research`

1.  **Define the Problem**: Use the *Cynefin Framework* to categorize the problem (Simple, Complicated, Complex).
2.  **Gather Intelligence**:
    *   Execute `scripts/deep_search.py` on competitors/domain.
    *   Ingest top 10 URLs into NotebookLM.
    *   Ask: "What are the standard failure modes in this domain?"
3.  **Draft Requirements**:
    *   Create a `product-requirements.md`.
    *   Define **Non-Functional Requirements** (NFRs) early:
        *   Latency (e.g., < 200ms)
        *   Scale (e.g., 10k daily users)
        *   Compliance (e.g., GDPR)

## Phase 2: Domain Modeling & API Contract
**Skill**: `designing-apis` & `database-design`

1.  **Identify Resources**: List the Nouns (e.g., `User`, `Order`, `Shipment`).
2.  **Define Relations**: Draw an Entity-Relationship Diagram (Mermaid).
3.  **Draft OpenAPI Spec**:
    *   Create `openapi.yaml`.
    *   **HARD RULE**: No query strings in server URLs.
    *   **HARD RULE**: Strict typing for enums.
4.  **Review**: Validate against the "12-Factor App" principles (Statelessness).

## Phase 3: Infrastructure Design
**Skill**: `architecting-distributed-systems` & `writing-infrastructure-code`

1.  **Select Pattern**: Monolith vs. Microservices? (Default to Modular Monolith unless scale demands otherwise).
2.  **Define Stack**:
    *   Frontend: Next.js / React
    *   Backend: FastAPI / Node.js
    *   Database: Postgres (Relational) or DynamoDB (Access Patterns known).
3.  **Draft IaC Spec**:
    *   Create `terraform/` structure.
    *   **HARD RULE**: State must be remote (S3) and encrypted.
    *   **HARD RULE**: Tagging strategy defined from Day 1.

## Deliverable Checkpoint
Before writing code, you must have:
*   [ ] `product-requirements.md` (Validated by Research)
*   [ ] `openapi.yaml` (The Contract)
*   [ ] `architecture-diagram.png` (The Map)
*   [ ] `terraform/plan` (The Terrain)
