---
name: modern-web-design-2025
description: Implements 2025-2026 web design trends including Agentic UX, Liquid Glass aesthetics, Neurodiversity, and Sustainable Design. Use when creating high-fidelity interfaces, AI-driven applications, or modern premium web experiences.
---

# Modern Web Design Standards (2025-2026)

## Purpose

This skill defines the standards for next-generation web experiences, focusing on the intersection of AI, high-fidelity aesthetics, and inclusive, sustainable design.

## Core Trends

### 1. Agentic UX (AI-Driven Interaction)
Design for systems where the interface is a collaborator, not just a tool.
- **Intent-Aware Layouts:** Interfaces that reconfigure themselves based on user intent.
- **Co-Creation Patterns:** UI elements that allow users to steer AI agents in real-time.
- **Feedback Loops:** Clear visual cues when AI is processing, suggesting, or acting.

### 2. Liquid Glass Aesthetics
The evolution of glassmorphism for the spatial computing era.
- **Translucency & Depth:** Multi-layered blurred surfaces with dynamic shadows.
- **Micro-shadows:** Extremely subtle shadows to define hierarchy without clutter.
- **Fluid Motion:** Smooth transitions that mimic physical inertia.

### 3. Neurodiversity & Cognitive Inclusion
Designing for ALL minds (TDAH, Autism, Dyslexia).
- **Reduced Motion Modes:** Easy toggles to stop all non-essential animations.
- **Focus Modes:** Standardized "Zen" views that remove all peripheral distractions.
- **Dyslexia-Friendly Typography:** Support for specialized fonts and optimized line heights.

### 4. Sustainable "Eco-UX"
Minimizing the digital carbon footprint.
- **Low-Energy Modes:** Dark-mode-first designs and reduced image payloads.
- **Efficient Components:** Skeleton loaders that prevent layout shifts and minimize CPU cycles.

## Implementation Examples

### Liquid Glass CSS Pattern
```css
.liquid-glass-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 24px;
  box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.1);
}
```

### Motion Preference Support
```css
@media (prefers-reduced-motion: reduce) {
  *, ::before, ::after {
    animation-delay: -1ms !important;
    animation-duration: 1ms !important;
    animation-iteration-count: 1 !important;
    background-attachment: initial !important;
    scroll-behavior: auto !important;
    transition-duration: 0s !important;
    transition-delay: 0s !important;
  }
}
```

## How to Use
1. **Identify the Project Tier:** Use for "Premium" or "AI-First" projects.
2. **Apply Design Tokens:** Reference `modern-tokens.json` (to be created).
3. **Validate Accessibility:** Ensure neurodiversity checks are passed.

## References
- `skills/designing-layouts/` - Base layout patterns.
- `skills/design-tokens/` - Core variables.
