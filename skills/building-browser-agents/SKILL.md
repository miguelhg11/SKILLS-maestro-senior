---
name: building-browser-agents
description: Build autonomous browser agents that can navigate, extract data, and perform actions on websites. Covers headless automation with Playwright/Puppeteer, anti-detection techniques, handling dynamic content, and integrating with LLMs for somatic control. Use when APIs are unavailable or when automating complex user workflows.
---

# Building Browser Agents

## Purpose

This skill defines patterns for creating autonomous agents that interact with the web through a browser interface. Unlike testing (which verifies expected behavior), browser agents must adapt to unexpected content, handle anti-bot measures, and extract structured data from unstructured interfaces.

## When to Use

**Use this skill when:**
- No public API exists for the target service.
- You need to automate a complex user workflow (e.g., booking, filling forms across pages).
- Scraping highly dynamic Single Page Applications (SPAs).
- Testing UI behavior that requires "fuzzy" or AI-driven interaction.
- Taking screenshots or generating PDFs of dynamic content.

**Skip this skill if:**
- A reliable REST or GraphQL API is available (use `implementing-api-patterns`).
- You strictly need to validate code correctness (use `testing-strategies`).
- Scale is massive and simple HTTP requests suffice (use `ingesting-data`).

## Quick Start

### Playwright Python Agent (Recommended)

Playwright is the modern standard for browser automation due to its reliability and auto-waiting mechanisms.

```python
from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        # Launch browser (headless=False for debugging)
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...",
            viewport={"width": 1280, "height": 720}
        )
        page = context.new_page()
        
        # Navigate with resilience
        try:
            page.goto("https://example.com/login", wait_until="networkidle")
            
            # Interact with selectors (robust selection)
            page.fill('input[name="username"]', "my_agent_user")
            page.fill('input[name="password"]', "secure_password")
            page.click('button[type="submit"]')
            
            # Wait for navigation or dynamic content
            page.wait_for_selector(".dashboard-welcome")
            
            # Extract data
            balance = page.inner_text(".account-balance")
            print(f"Current Balance: {balance}")
            
        except Exception as e:
            print(f"Agent failed: {e}")
            page.screenshot(path="error_state.png")
            
        finally:
            browser.close()

if __name__ == "__main__":
    run()
```

## Core Concepts

### 1. Robust Selectors
Agents fail when selectors break. Use resilient strategies:
- **Text-based**: `page.get_by_text("Login")` (User-facing)
- **Role-based**: `page.get_by_role("button", name="Submit")` (Accessibility-first)
- **Test IDs**: `page.locator('[data-testid="submit-btn"]')` (If you control the codebase)
- **CSS Attributes**: `page.locator('input[name="q"]')` (Stable attributes)

### 2. Handling Dynamic Content
The web is async. Never use fixed sleeps (`time.sleep(5)`).
- **Auto-waiting**: Playwright methods wait for elements to be actionable automatically.
- **Explicit Waits**: `page.wait_for_selector(".result-item")`
- **Network States**: `page.wait_for_load_state("networkidle")`

### 3. Anti-Detection (Stealth)
Websites block bots. Basic evasion techniques:
- **User-Agent Rotation**: Use real user agents.
- **Stealth Plugins**: `playwright-stealth` or modifications to `navigator.webdriver`.
- **Human-like Behavior**: Add random delays, mouse movements, and realistic typing speeds.
- **Browser Contexts**: Use persistent contexts to save cookies/session, or fresh ones to simulate new users.

```python
# Stealth usage with specialized libraries often allows bypassing simple detections
# Example conceptual setup
context = browser.new_context(
    java_script_enabled=True,
    has_touch=False,
    locale="en-US",
    timezone_id="America/New_York"
)
```

## Advanced Patterns

### SOM (Set-of-Mark) Prompting with LLMs
To let an LLM control the browser, you need to "visualize" the page for it.
1. **Inject Labels**: Javascript script draws numbered boxes over interactive elements.
2. **Snapshot**: Take a screenshot with these labels.
3. **Prompt**: Send image to VLM (Vision LLM). "Click on box #5 to Search".
4. **Action**: Agent clicks the coordinate/selector associated with #5.

### Data Extraction Strategies
- **DOM Parsing**: Fast, lightweight. Use Beautiful Soup on `page.content()`.
- **Hybrid**: Use Playwright to render JS, then extract with parsing libs.
- **Vision Extraction**: Screenshot -> OCR/VLM for unselectable text (e.g., inside canvas or images).

### Resume & Recovery
Agents crash.
- **State Serialization**: Save cookies/storageState to disk.
- **Retry Logic**: Wrap actions in retry blocks with exponential backoff.
- **Error Screenshots**: Always capture visuals on failure for debugging.

## Reference Implementations

### Extraction Agent (Typescript)
```typescript
import { chromium } from 'playwright';

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  
  await page.goto('https://news.ycombinator.com/');
  
  // Extract list data
  const articles = await page.evaluate(() => {
    const rows = document.querySelectorAll('.athing');
    return Array.from(rows).map(row => {
      const titleLink = row.querySelector('.titleline > a');
      return {
        title: titleLink?.textContent,
        url: titleLink?.getAttribute('href')
      };
    });
  });

  console.log(JSON.stringify(articles, null, 2));
  await browser.close();
})();
```

## Decision Framework

### Tool Selection
| Technology | Best For | Pros | Cons |
|:---|:---|:---|:---|
| **Playwright** | General Purpose | Fast, reliable, multi-lang | Large dependency |
| **Puppeteer** | Node.js Heavy | Deep Chrome integration | Chrome only |
| **Selenium** | Legacy/Enterprise | Wide compatibility | Slower, verbose |
| **Crawlee** | Large Scale Scraping | Management of queues/proxies | Learning curve |

## Integration with Other Skills
- **`ingesting-data`**: Feed scraped data into your data pipelines.
- **`ai-data-engineering`**: Use scraped content for RAG knowledge bases.
- **`testing-strategies`**: Use similar tools but for verification rather than operation.
