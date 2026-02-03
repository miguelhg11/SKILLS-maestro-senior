#!/usr/bin/env python3
import os
import re
import json
import requests
import argparse
import sys
from datetime import datetime
from typing import List, Dict, Any, Optional

class NotebookLMMaster:
    """
    Master Senior NotebookLM Bridge
    Definitive solution for robust knowledge extraction.
    """
    
    def __init__(self, cookies_path: str = "notebooklm_cookies.txt"):
        self.cookies_path = cookies_path
        self.session = requests.Session()
        self.base_url = "https://notebooklm.google.com"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        }
        self.load_cookies()

    def load_cookies(self):
        if not os.path.exists(self.cookies_path):
            print(f"[!] Warning: Cookie file {self.cookies_path} not found.")
            return

        try:
            with open(self.cookies_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content.startswith("["):
                    cookies = json.loads(content)
                    for cookie in cookies:
                        self.session.cookies.set(cookie['name'], cookie['value'], domain=cookie.get('domain', '.google.com'))
                else:
                    # Netscape format fallback
                    for line in content.splitlines():
                        if not line.startswith("#") and "\t" in line:
                            parts = line.split("\t")
                            if len(parts) >= 7:
                                self.session.cookies.set(parts[5], parts[6], domain=parts[0])
            print(f"[+] Loaded cookies from {self.cookies_path}")
        except Exception as e:
            print(f"[!] Error loading cookies: {e}")

    def verify_session(self) -> bool:
        """Verifies if the current session is authenticated."""
        try:
            response = self.session.get(self.base_url, headers=self.headers, timeout=15)
            if "GlifWebSignIn" in response.text or "ServiceLogin" in response.text:
                print("[!] Session expired: Redirected to Login.")
                return False
            if "notebooklm-root" in response.text or "AF_initDataCallback" in response.text:
                print("[+] Session active and verified.")
                return True
            print("[?] Session status ambiguous.")
            return False
        except Exception as e:
            print(f"[!] Connection error: {e}")
            return False

    def discover_notebooks(self) -> List[str]:
        """Scans the home page for notebook IDs."""
        print("[*] Discovering notebooks...")
        try:
            response = self.session.get(self.base_url, headers=self.headers)
            ids = re.findall(r'/notebook/([a-f0-9-]+)', response.text)
            unique_ids = list(set(ids))
            print(f"[+] Found {len(unique_ids)} notebooks: {unique_ids}")
            return unique_ids
        except Exception as e:
            print(f"[!] Discovery failed: {e}")
            return []

    def deep_extract(self, obj: Any, keywords: List[str]) -> List[str]:
        """Recursively find strings containing keywords."""
        results = []
        if isinstance(obj, str):
            if any(k.lower() in obj.lower() for k in keywords):
                if len(obj) > 20: # Filter short/garbage strings
                    results.append(obj)
        elif isinstance(obj, list):
            for item in obj:
                results.extend(self.deep_extract(item, keywords))
        elif isinstance(obj, dict):
            for value in obj.values():
                results.extend(self.deep_extract(value, keywords))
        return results

    def fetch_content(self, notebook_id: str, keywords: List[str] = ["web", "layout", "ux", "ui"]) -> List[str]:
        """Fetches and parses content for a specific notebook."""
        url = f"{self.base_url}/notebook/{notebook_id}"
        print(f"[*] Extracting notebook: {notebook_id}")
        
        try:
            response = self.session.get(url, headers=self.headers, timeout=15)
            findings = []
            
            # 1. Try AF_initDataCallback blocks
            callbacks = re.findall(r'AF_initDataCallback\((.*?)\);', response.text, re.DOTALL)
            for cb in callbacks:
                try:
                    # Clean the callback string to get the data JSON
                    data_match = re.search(r'data:(.*),sideChannel', cb, re.DOTALL)
                    if data_match:
                        data_str = data_match.group(1).strip()
                        data = json.loads(data_str)
                        findings.extend(self.deep_extract(data, keywords))
                except:
                    continue
            
            # 2. Try WIZ_global_data
            wiz_match = re.search(r'WIZ_global_data = ({.*?});', response.text)
            if wiz_match:
                try:
                    wiz_data = json.loads(wiz_match.group(1))
                    findings.extend(self.deep_extract(wiz_data, keywords))
                except:
                    pass
            
            # 3. Direct text scan for long snippets
            long_strings = re.findall(r'\"([^\"]{200,})\"', response.text)
            for s in long_strings:
                if any(k.lower() in s.lower() for k in keywords):
                    findings.append(s)
                    
            unique_findings = list(set(findings))
            return unique_findings
        except Exception as e:
            print(f"[!] Extraction failed for {notebook_id}: {e}")
            return []

def main():
    parser = argparse.ArgumentParser(description="Master Senior NotebookLM Bridge")
    parser.add_argument("--verify", action="store_true", help="Verify session health")
    parser.add_argument("--list", action="store_true", help="List discoverable notebooks")
    parser.add_argument("--extract", type=str, help="Extract content from specific notebook ID")
    parser.add_argument("--scan-all", action="store_true", help="Scan all discovered notebooks")
    args = parser.parse_args()

    bridge = NotebookLMMaster()
    
    if args.verify:
        bridge.verify_session()
        
    elif args.list:
        bridge.discover_notebooks()
        
    elif args.extract:
        results = bridge.fetch_content(args.extract)
        for r in results:
            print(f"\n--- MATCH ---\n{r}")
            
    elif args.scan_all:
        ids = bridge.discover_notebooks()
        all_results = {}
        for nid in ids:
            res = bridge.fetch_content(nid)
            if res:
                all_results[nid] = res
        
        output_file = "master_extraction_results.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(all_results, f, indent=2, ensure_ascii=False)
        print(f"\n[+] Full scan complete. Results saved to {output_file}")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
