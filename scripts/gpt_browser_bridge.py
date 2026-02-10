import asyncio
import sys
import json
import os
import argparse
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="[GPT_BRIDGE] %(levelname)s: %(message)s"
)
logger = logging.getLogger(__name__)

# Try importing playwright, if not installed, we can't run.
try:
    from playwright.async_api import async_playwright
except ImportError:
    logger.error("Playwright library not found. Please run: pip install playwright")
    sys.exit(1)

class GPTBrowserBridge:
    def __init__(self, cdp_url="http://127.0.0.1:9222"):
        self.cdp_url = cdp_url

    async def send_prompt(self, prompt, model="gpt-4o"):
        async with async_playwright() as p:
            try:
                # Connect to the existing Chrome instance opened by open_gpt_gateway.bat
                browser = await p.chromium.connect_over_cdp(self.cdp_url)
                context = browser.contexts[0]
                pages = context.pages
                
                chat_page = None
                
                # Find the ChatGPT tab
                for page in pages:
                    if "chatgpt.com" in page.url:
                        chat_page = page
                        break
                
                if not chat_page:
                    logger.info("ChatGPT tab not found. Opening new one.")
                    chat_page = await context.new_page()
                    await chat_page.goto("https://chatgpt.com")
                
                # Bring to front
                await chat_page.bring_to_front()
                
                # Wait for interface to settle
                # Try generic editable div if ID fails
                textarea_selector = "#prompt-textarea"
                fallback_selector = "div[contenteditable='true']"
                
                try:
                    await chat_page.wait_for_selector(textarea_selector, state="visible", timeout=5000)
                    target_selector = textarea_selector
                except:
                    logger.info("Standard textarea ID not found, trying fallback contenteditable...")
                    try:
                        await chat_page.wait_for_selector(fallback_selector, state="visible", timeout=5000)
                        target_selector = fallback_selector
                    except:
                        return "Error: Could not find ChatGPT input box. Please ensure you are logged in."

                # Fill Text (Focus + Type to simulate user potentially)
                await chat_page.click(target_selector)
                await chat_page.fill(target_selector, prompt)
                
                # Send Strategy: Click Button OR Press Enter
                # Button usually has data-testid="send-button"
                send_button = chat_page.locator('[data-testid="send-button"]')
                
                if await send_button.count() > 0 and await send_button.is_visible():
                    await send_button.click()
                else:
                    logger.info("Send button not found/visible, pressing Enter.")
                    await chat_page.keyboard.press("Enter")

                # Wait for Response
                # Strategy: Wait for "Stop generating" (start) then wait for it to vanish (end)
                try:
                    # Give it a moment to start generating
                    await chat_page.wait_for_timeout(1000) 
                    
                    # Sometimes the "Stop" button selector is [data-testid="stop-button"]
                    # We wait for the send button to be visible again, which means generation ended.
                    await chat_page.wait_for_selector('[data-testid="send-button"]', timeout=120000)
                except Exception as e:
                    logger.warning(f"Wait for response timeout/issue: {e}")

                # Extract last response
                # We look for all agent responses. 
                # Common selector for bot formatting: .markdown
                # Or specific message containers: [data-message-author-role="assistant"]
                
                responses = await chat_page.locator('[data-message-author-role="assistant"] .markdown').all_inner_texts()
                
                if not responses:
                    # Fallback to just .markdown if role attribute is missing
                    responses = await chat_page.locator('.markdown').all_inner_texts()
                
                if responses:
                    return responses[-1]
                else:
                    return "Error: No response text found after sending."

            except Exception as e:
                logger.error(f"Bridge connection error: {e}")
                return f"Error connecting to Browser Bridge: {e}"

def main():
    parser = argparse.ArgumentParser(description="GPT Browser Bridge")
    parser.add_argument("prompt", nargs="?", help="Prompt to send")
    parser.add_argument("--test", action="store_true", help="Test connection")
    
    args = parser.parse_args()

    # If installed via pip, playwright install might be needed for browsers, 
    # but we are connecting to existing Chrome, so maybe not strictly.
    
    bridge = GPTBrowserBridge()

    if args.test:
        print("Testing Connection to Chrome...")
        # Simple test logic here if needed
        return

    if args.prompt:
        try:
             response = asyncio.run(bridge.send_prompt(args.prompt))
             print(response)
        except Exception as e:
             print(f"Error: {e}")

if __name__ == "__main__":
    main()
