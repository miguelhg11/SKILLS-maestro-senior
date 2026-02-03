---
name: sre-resilience
description: Applying Site Reliability Engineering (SRE) principles to build resilient systems. Covers Service Level Objectives (SLOs), Error Budgets, Post-Mortems, and reliability patterns (Circuit Breaker, Bulkhead, Retry, Fallback). Use when defining system reliability targets, handling partial failures, or operationalizing incident response.
---

# SRE & Resilience Engineering

## Purpose

Shift from "hoping nothing breaks" to "designing for failure". This skill establishes the framework for **SLOs (Service Level Objectives)** and implements architectural patterns that allow systems to degrade gracefully rather than collapse.

## When to Use

Use this skill when:
- Defining "how much downtime is acceptable" (SLO/SLA)
- Designing distributed systems that must survive dependency failures behavior
- Conducting **Blameless Post-Mortems** after an incident
- Implementing client-side resilience (retries, circuit breakers)

## Hard Rules (MUST)
> **Source**: Google SRE Book & Azure Well-Architected Framework

1. **SLO Defined**: Critical user journeys MUST have an SLO (e.g., "99.9% of requests successful"). Metrics without targets are useless.
2. **Fail Gracefully**: If a dependency is down, the system MUST return a degraded response (cached data, default value) or a fast error, NEVER a hang/timeout.
3. **Idempotency**: All retryable operations (network calls) MUST be idempotent.
4. **Timeouts**: Every network call MUST have a configured timeout. Infinite timeouts are FORBIDDEN.
5. **Post-Mortems**: Every customer-impacting incident MUST generate a written post-mortem document focusing on process, not people.

## Core Concepts: reliability Stack

### 1. Indicators & Objectives (SLI/SLO)

- **SLI (Indicator)**: The metric (e.g., Latency).
- **SLO (Objective)**: The target (e.g., < 200ms for 99% of requests).
- **SLA (Agreement)**: The legal contract (money back if violated). **Engineers care about SLOs.**

**Example SLO**:
> "99.9% of user login requests in the last 28 days serve a 200 OK status within 500ms."

### 2. Error Budgets

The gap between perfect reliability (100%) and the SLO (99.9%) is the **Error Budget** (0.1%).
- **Rule**: If you burn the budget, you freeze deployments to focus on stability.
- **Rule**: If you have budget left, you can take risks and ship faster.

## Resilience Patterns (Code Level)

### Circuit Breaker
Stop calling a failing service to prevent cascading failure.

```python
# Conceptual Python Example (using pybreaker)
@circuit_breaker
def call_payment_gateway():
    # If this fails 5 times, the breaker opens.
    # Future calls fail immediately (Fast Fail) without hitting the network.
    pass
```

### Bulkhead
Isolate resources so one failure doesn't crash the whole ship.
*Example*: Use separate Thread Pools (or connection pools) for "User API" vs "Admin API". If Admin is slow, Users are unaffected.

### Retry with Exponential Backoff
Never retry instantly in a tight loop (Thundering Herd).

```python
# Wait 1s, then 2s, then 4s... + Jitter (randomness)
failures = 0
while failures < max_retries:
    try:
        return make_request()
    except NetworkError:
        sleep(2**failures + random.uniform(0, 0.1))
        failures += 1
```

## Incident Response (The OODA Loop)

1. **Observe**: Alerts fire (High Error Rate).
2. **Orient**: Check dashboards. Is it code? Database? Provider?
3. **Decide**: declare Incident. Assign Roles (Commander, Comms, Ops).
4. **Act**: Mitigate (Rollback, Scale Up, Block Traffic). **Fixing the root cause is for later; Mitigation is for NOW.**

## Post-Mortem Template Structure

1. **Summary**: What/When/Where.
2. **Impact**: How many users affected? Data loss?
3. **Root Cause**: The technical "Why".
4. **Trigger**: What action started it?
5. **Timeline**: Minute-by-minute log.
6. **Lessons Learned**: What went well? What went wrong?
7. **Action Items**: Jira tickets to prevent recurrence (Priority 0).

## Troubleshooting "Flaky" Systems

- **Check Timeouts**: Are they too short? Too long?
- **Check Retries**: Are you DDoSing yourself with infinite retries?
- **Check Dependencies**: Is a non-critical dependency (e.g., Avatar Service) blocking the critical path (Login)? -> Make it async or optional.
