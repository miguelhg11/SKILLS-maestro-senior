---
name: playbook-secure-go-live
description: A pre-flight checklist for deploying production systems. Orchestrates Security, Supply Chain, SRE, and Observability skills to ensure 'Fortress' compliance.
---

# Playbook: Secure Go-Live (Fortress Compliance)

## Purpose
To ensure that NO deployment goes to production without passing strict security, reliability, and observability gates. This is the "Final Exam" for any system.

## Gate 1: Supply Chain Integrity
**Skill**: `supply-chain-security`

*   [ ] **Lockfiles**: Do `package-lock.json` / `go.sum` exist and match the build?
*   [ ] **Clean Build**: Is the build scripted (Dockerfile/GitHub Actions) with NO manual steps?
*   [ ] **SBOM**: Is a CycloneDX SBOM generated for this specific release artifact?
*   [ ] **Scan**: Did `trivy` or `grype` return ZERO critical vulnerabilities?

## Gate 2: Applications Security (AppSec)
**Skill**: `securing-authentication` & `security-hardening`

*   [ ] **Auth**: Are all token secrets 2048-bit+ key length?
*   [ ] **Storage**: Is `LocalStorage` strictly avoided for token storage? (Use HttpOnly Cookies).
*   [ ] **Secrets**: Are ALL secrets injected via environment variables (12-Factor)?
*   [ ] **Headers**: Are `HSTS`, `Content-Security-Policy`, and `X-Frame-Options` active?

## Gate 3: Resilience & SRE
**Skill**: `sre-resilience`

*   [ ] **Timeouts**: Do ALL external calls have a timeout set? (No infinite waits).
*   [ ] **Retries**: Are retries using exponential backoff + jitter?
*   [ ] **Circuits**: Is there a Circuit Breaker for non-critical dependencies?
*   [ ] **Backup**: Is the database backup automated and **tested**?

## Gate 4: Observability (The Eyes)
**Skill**: `implementing-observability`

*   [ ] **Correlation**: Do logs contain `trace_id`?
*   [ ] **Metrics**: Are the "Golden Signals" (Latency, Traffic, Errors, Saturation) being captured?
*   [ ] **Alerts**: Is there an alert for high error rate (>1%) routed to a human?
*   [ ] **SLO**: Is the initial SLO defined (e.g., "99.0% Availability")?

## Gate 5: Performance Verification
**Skill**: `performance-engineering`

*   [ ] **Load**: Did the system survive 110% of expected peak traffic in Staging?
*   [ ] **Vitals**: Is Core Web Vitals LCP < 2.5s?
*   [ ] **Database**: Are there any N+1 query warnings in the logs?

## The "Go" Decision
If ALL checkboxes are ticked:
1.  **Tag** the release (Immutable SemVer).
2.  **Sign** the artifact (Sigstore).
3.  **Deploy**.
