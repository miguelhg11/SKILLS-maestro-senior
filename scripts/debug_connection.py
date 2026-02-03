import requests
import json
import os
import re

def debug_notebooklm():
    session = requests.Session()
    cookies_path = "notebooklm_cookies.txt"
    
    if not os.path.exists(cookies_path):
        print(f"Error: {cookies_path} not found")
        return

    with open(cookies_path, 'r', encoding='utf-8') as f:
        cookies_json = json.loads(f.read())
        for cookie in cookies_json:
            session.cookies.set(cookie['name'], cookie['value'], domain=cookie.get('domain', '.google.com'))

    print("Requesting https://notebooklm.google.com ...")
    response = session.get("https://notebooklm.google.com")
    print(f"Status Code: {response.status_code}")
    print(f"Final URL: {response.url}")
    
    with open("debug_notebooklm_home.html", "w", encoding="utf-8") as f:
        f.write(response.text)
    
    # Check for login redirection
    if "ServiceLogin" in response.url or "accounts.google.com" in response.url:
        print("FAIL: Redirected to login. Cookies might be invalid or insufficient.")
    else:
        print("SUCCESS: Stayed in notebooklm.google.com")
        
    # Search for notebook IDs
    matches = re.findall(r'\"([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})\"', response.text)
    print(f"Found IDs: {len(matches)}")
    for m in set(matches):
        print(f" - {m}")

if __name__ == "__main__":
    debug_notebooklm()
