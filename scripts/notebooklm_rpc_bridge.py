import os
import json
import requests
import re
import argparse
from typing import List, Dict, Any

class NotebookLMRPCBridge:
    def __init__(self, cookies_path: str = "notebooklm_cookies.txt"):
        self.cookies_path = cookies_path
        self.session = requests.Session()
        self.base_url = "https://notebooklm.google.com"
        self.load_cookies()

    def load_cookies(self):
        if not os.path.exists(self.cookies_path):
            raise FileNotFoundError(f"Error: {self.cookies_path} not found.")
        
        with open(self.cookies_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            try:
                cookies_json = json.loads(content)
                for cookie in cookies_json:
                    self.session.cookies.set(
                        cookie['name'], 
                        cookie['value'], 
                        domain=cookie.get('domain', '.google.com'),
                        path=cookie.get('path', '/')
                    )
            except json.JSONDecodeError:
                # Basic Netscape format fallback
                for line in content.splitlines():
                    if not line.startswith('#') and '\t' in line:
                        parts = line.split('\t')
                        if len(parts) >= 7:
                            self.session.cookies.set(parts[5], parts[6], domain=parts[0])

    def fetch_notebook_content(self, notebook_id: str) -> List[str]:
        """
        Fetches the notebook page and extracts internal state.
        """
        print(f"Fetching notebook {notebook_id}...")
        url = f"{self.base_url}/notebook/{notebook_id}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        }
        
        try:
            response = self.session.get(url, headers=headers, timeout=15)
            # Save dump for target
            with open(f"debug_{notebook_id}.html", "w", encoding="utf-8") as f:
                f.write(response.text)
            
            if response.status_code != 200:
                print(f"Failed {notebook_id}: {response.status_code}")
                return []
        except Exception as e:
            print(f"Error fetching {notebook_id}: {e}")
            return []

        # Keywords to identify research content
        keywords = ["tendencia", "diseño", "web", "layout", "ux", "ui", "maestro"]
        findings = []
        
        # Search in WIZ_global_data and AF_initDataCallback
        # Using a more direct string search for speed in batch
        for kw in keywords:
            if kw in response.text.lower():
                print(f"Match found for '{kw}' in {notebook_id}")
                # Use regex to extract the sentence/block around it
                matches = re.findall(r'[^.!?]*' + re.escape(kw) + r'[^.!?]*', response.text, re.IGNORECASE)
                for m in matches:
                    if len(m) > 40:
                        findings.append(m.strip())
        
        return list(set(findings))

def main():
    parser = argparse.ArgumentParser(description="NotebookLM RPC Bridge - Batch Scanner")
    parser.add_argument("--ids", nargs="+", help="Notebook IDs to scan")
    parser.add_argument("--target", help="Single target ID")
    args = parser.parse_args()

    bridge = NotebookLMRPCBridge()
    
    ids_to_scan = []
    if args.ids:
        ids_to_scan = args.ids
    elif args.target:
        ids_to_scan = [args.target]
    else:
        # Defaults if none provided (from previous discovery)
        ids_to_scan = [
            "1a6c73f9-b9d8-4763-8077-3a1526e044f2",
            "62e5c8db-3dd2-407c-8d19-32ae4ae799db",
            "953b658a-579b-4b3c-b280-43b3781babf3",
            "71669a91-d5f0-4298-913e-9193178ec62c",
            "f7607d7a-584c-4f35-96fc-f6815c573a6c"
        ]

    all_results = {}
    for nid in ids_to_scan:
        res = bridge.fetch_notebook_content(nid)
        if res:
            all_results[nid] = res

    if all_results:
        print(f"Found content in {len(all_results)} notebooks.")
        with open("research_batch_results.txt", "w", encoding="utf-8") as f:
            for nid, findings in all_results.items():
                f.write(f"=== NOTEBOOK: {nid} ===\n")
                for fnd in findings:
                    f.write(f"- {fnd}\n")
                f.write("\n")
        print("Batch scan complete. Results in research_batch_results.txt")
    else:
        print("No content found in any of the scanned notebooks.")

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
