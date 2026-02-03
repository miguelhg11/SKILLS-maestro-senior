---
name: supply-chain-security
description: Securing the software supply chain to prevent tampering and ensure integrity. Covers SLSA compliance (Levels 1-3), SBOM generation (CycloneDX, SPDX), artifact signing (Sigstore/Cosign), and dependency scanning. Use when hardening CI/CD pipelines, complying with security standards (NIST SSDF), or implementing "Secure by Design" principles.
---

# Supply Chain Security

## Purpose

Secure the entire software delivery lifecycle, from code commit to production deployment. This skill implements the **SLSA (Supply-chain Levels for Software Artifacts)** framework and mandates the use of **SBOMs (Software Bill of Materials)** and immutable audit logs.

## When to Use

Use this skill when:
- Establishing a secure build pipeline (CI/CD)
- Auditing dependencies for vulnerabilities (Log4Shell style risks)
- Ensuring artifacts provenance (verifying *what* code built *this* binary)
- Implementing compliant release processes (FedRAMP, NIST)

## Hard Rules (MUST)
> **Source**: SLSA v1.0 & NIST SP 800-218

1. **Build as Code**: All build steps MUST be defined in version-controlled configuration (e.g., `cloudbuild.yaml`, `.github/workflows`). Manual builds are FORBIDDEN for production.
2. **Provenance**: The build system MUST generate authenticated provenance (metadata) signed by the build service.
3. **Ephemeral Environments**: Builds MUST run in ephemeral, isolated environments (e.g., disposable containers) to prevent contamination.
4. **SBOM Generation**: Every release MUST include a comprehensive SBOM (CycloneDX or SPDX) listing all direct and transitive dependencies.
5. **No Mutable Tags**: Production deployments MUST use immutable SHA/Digest references (e.g., `image@sha256:abc...`), NOT mutable tags like `latest` or `v1`.

## Core Framework: SLSA

### SLSA Levels Summary

| Level | Goal | Requirements |
| :--- | :--- | :--- |
| **L1** | **Documentation** | Build process is scripted and version controlled. |
| **L2** | **Tamper Resistance** | Build runs on a hosted service (not developer laptop) + Provenance generated. |
| **L3** | **Non-Falsifiability** | Build platform is hardened; provenance is verified and signed; isolated build env. |

### Implementation Guide

#### 1. Generate SBOM (CycloneDX)
Use `syft` or language-specific tools to generate a Bill of Materials.

```bash
# Generate SBOM for a container image
syft packages docker:my-app:latest -o cyclonedx-json > sbom.json

# Check for vulnerabilities in the SBOM using Grype
grype sbom:sbom.json
```

#### 2. Sign Artifacts (Cosign / Sigstore)
Ensure that the artifact you built is the one you deploy.

```bash
# Generate key pair
cosign generate-key-pair

# Sign a container image
cosign sign --key cosign.key my-registry.com/my-app@sha256:123...

# Verify signature (in admission controller or deploy script)
cosign verify --key cosign.pub my-registry.com/my-app@sha256:123...
```

#### 3. SLSA Provenance (GitHub Actions)
Use the SLSA generator for GitHub Actions.

```yaml
uses: slsa-framework/slsa-github-generator/.github/workflows/generator_generic_slsa3.yml@v1.4.0
with:
  base64-subjects: "${{ needs.build.outputs.hashes }}"
  prove-subjects-paths: false
```

## Dependency Management

### Lockfiles
**Hard Rule**: All package managers MUST use lockfiles (`package-lock.json`, `go.sum`, `poetry.lock`) to ensure deterministic builds.

### Renovate / Dependabot
Automate dependency updates but enforce strict testing gates.
- **Config**: Group updates to reduce noise.
- **Policy**: Auto-merge patch versions ONLY if tests pass.

## Reference Architecture (Secure Pipeline)

1. **Code**: Developer commits to Git (Signed Commits required).
2. **Build**: CI triggers in isolated runner.
   - Restores dependencies from lockfile.
   - Runs SAST (Static Analysis).
3. **Test**: Unit and Integration tests pass.
4. **Package**: Container image built.
5. **Analyze**: SBOM generated + Vulnerability Scan (Grype/Trivy).
6. **Sign**: Image signed with Cosign (Keyless or Key-based).
7. **Deploy**: Kubernetes Admission Controller (Kyverno/Gatekeeper) verifies signature before pulling.

## Troubleshooting

- **Signature Verification Failed**: Check if the image tag was mutated (someone overwrote `v1`). Move to SHA digests.
- **Vulnerability Noise**: Use `.trivyignore` or similar ONLY for triaged non-exploitable issues with justification.
