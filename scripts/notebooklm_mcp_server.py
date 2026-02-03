import asyncio
import os
import json
import sys
from typing import List, Optional

# --- CRITICAL ENVIRONMENT FIX ---
if os.name == 'nt':
    os.environ["HOME"] = os.environ.get("USERPROFILE", "")

try:
    from mcp.server.fastmcp import FastMCP
    from playwright.async_api import async_playwright, Page, BrowserContext
except ImportError:
    print("Error: Missing dependencies. Run: pip install mcp playwright")
    sys.exit(1)

# Initialize FastMCP Server
mcp = FastMCP("NotebookLM-Senior")

# CDP Configuration
CDP_URL = "http://localhost:9222"

async def get_browser_context(p) -> Optional[BrowserContext]:
    """
    Connects to an existing Chrome instance via CDP.
    """
    try:
        print(f"Connecting to Chrome Gateway at {CDP_URL}...")
        browser = await p.chromium.connect_over_cdp(CDP_URL)
        # Use the first context (usually the default profile)
        if browser.contexts:
            return browser.contexts[0]
        return await browser.new_context()
    except Exception as e:
        print(f"Connection failed: {e}")
        return None

@mcp.tool()
async def check_connection() -> str:
    """
    Verifies if the NotebookLM Gateway is active and authenticated.
    """
    async with async_playwright() as p:
        context = await get_browser_context(p)
        if not context:
            return "Error: Could not connect to Chrome Gateway. Run 'open_notebook_gateway.bat' first."
        
        try:
            pages = context.pages
            # Look for an existing notebooklm tab
            notebook_tab = None
            for page in pages:
                if "notebooklm.google.com" in page.url:
                    notebook_tab = page
                    break
            
            if notebook_tab:
                title = await notebook_tab.title()
                return f"Connected! Found active tab: '{title}'"
            else:
                return "Connected to Gateway, but no NotebookLM tab found. Please navigate to the site."
                
        except Exception as e:
            return f"Error verifying connection: {e}"

@mcp.tool()
async def read_notebook(notebook_id: str) -> str:
    """
    Accesses a specific NotebookLM notebook via the Gateway and extracts content.
    Args:
        notebook_id: The UUID of the notebook (from the URL).
    """
    async with async_playwright() as p:
        context = await get_browser_context(p)
        if not context:
            return "Error: Gateway not running. Please execute 'open_notebook_gateway.bat' manually."

        try:
            # Check if we are already on the right page
            target_url = f"https://notebooklm.google.com/notebook/{notebook_id}"
            page = None
            
            # Reuse existing tab if possible
            for existing_page in context.pages:
                if notebook_id in existing_page.url:
                    page = existing_page
                    await page.bring_to_front()
                    break
            
            if not page:
                print(f"Opening new tab for {notebook_id}...")
                page = await context.new_page()
                await page.goto(target_url)
            
            # Wait for meaningful content
            try:
                # Wait for title to not be generic
                await page.wait_for_function("document.title.includes('Notebook') || document.title.length > 20", timeout=10000)
            except:
                pass # Continue processing anyway

            # Extraction
            title = await page.title()
            
            # 1. Try to get Sources list if visible
            sources_text = ""
            try:
                # Heuristic: look for source chips or list items
                # This selector needs to be generic enough or use text
                sources = await page.get_by_text("Fuentes").first.is_visible()
                if sources:
                   # Try to grab the container nearby
                   pass 
            except:
                pass

            # Dump main text for now
            content = await page.evaluate("document.body.innerText")
            
            # Save full content to debug file
            with open("debug_content.txt", "w", encoding="utf-8") as f:
                f.write(f"Title: {title}\n\n{content}")

            return f"Notebook: {title}\n\nContent Dump saved to debug_content.txt\nPreview:\n{content[:500]}..."
            
        except Exception as e:
            return f"Error reading notebook: {str(e)}"

@mcp.tool()
async def list_notebooks() -> str:
    """
    Lists available notebooks from the main dashboard.
    """
    async with async_playwright() as p:
        context = await get_browser_context(p)
        if not context:
            return "Error: Gateway not running."

        try:
            page = await context.new_page()
            await page.goto("https://notebooklm.google.com/")
            await page.wait_for_timeout(3000)
            
            notebooks = await page.evaluate("""
                () => {
                    const links = Array.from(document.querySelectorAll('a[href*="/notebook/"]'));
                    return links.map(a => ({href: a.href, text: a.innerText}));
                }
            """)
            
            await page.close()
            
            report = "Available Notebooks:\n"
            seen = set()
            for n in notebooks:
                nid = n['href'].split('/notebook/')[-1]
                if nid not in seen:
                    report += f"- ID: {nid} | Title: {n['text']}\n"
                    seen.add(nid)
            
            return report
            
        except Exception as e:
            return f"Error listing notebooks: {str(e)}"

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--test-cdp", action="store_true", help="Verify CDP connection")
    parser.add_argument("--fetch", type=str, help="Fetch specific notebook ID")
    parser.add_argument("--list", action="store_true", help="List notebooks")
    
    args = parser.parse_args()
    
    if args.test_cdp:
        print(asyncio.run(check_connection()))
    elif args.fetch:
        print(asyncio.run(read_notebook(args.fetch)))
    elif args.list:
        print(asyncio.run(list_notebooks()))
    else:
        # Run as MCP Server
        mcp.run()
