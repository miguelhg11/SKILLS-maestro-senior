import re
import json
import os

def search_recursive(obj, keywords, seen=None):
    if seen is None:
        seen = set()
    results = []
    if isinstance(obj, str):
        # We also look for strings that might BE JSON themselves
        if obj.startswith('[') or obj.startswith('{'):
            try:
                inner = json.loads(obj)
                results.extend(search_recursive(inner, keywords, seen))
            except:
                pass
        
        if len(obj) > 30 and any(k.lower() in obj.lower() for k in keywords):
            if obj not in seen:
                results.append(obj)
                seen.add(obj)
    elif isinstance(obj, list):
        for item in obj:
            results.extend(search_recursive(item, keywords, seen))
    elif isinstance(obj, dict):
        for value in obj.values():
            results.extend(search_recursive(value, keywords, seen))
    return results

def main():
    html_path = "notebook_rpc_dump.html"
    if not os.path.exists(html_path):
        print(f"Error: {html_path} not found.")
        return

    print("Reading HTML dump...")
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    keywords = ["tendencia", "diseño", "web", "layout", "ux", "ui", "maestro", "senior", "mejora", "architectural", "standards", "modern", "frontend", "visual"]

    all_findings = []

    print("Searching for WIZ_global_data...")
    match = re.search(r'WIZ_global_data\s*=\s*({.*?});', content, re.DOTALL)
    if match:
        try:
            data = json.loads(match.group(1))
            all_findings.extend(search_recursive(data, keywords))
        except:
            pass

    print("Searching for all AF_initDataCallback blocks...")
    # Find anything inside AF_initDataCallback(...)
    blocks = re.findall(r'AF_initDataCallback\((.*?)\);', content, re.DOTALL)
    print(f"Found {len(blocks)} blocks.")
    
    for i, block in enumerate(blocks):
        # Try to find the 'data' part if it's formatted as an object
        # Otherwise try to parse the whole thing as an object or list
        data_match = re.search(r'data:\s*(.*)', block, re.DOTALL)
        content_to_parse = data_match.group(1).strip() if data_match else block.strip()
        
        # Remove trailing comma if exists
        if content_to_parse.endswith(','):
            content_to_parse = content_to_parse[:-1]
            
        try:
            # If it's something like {key: '...', data: [...]}, it's not valid JSON because keys are not quoted
            # We can try to fix it or just extract strings with regex if JSON fails
            try:
                data = json.loads(content_to_parse)
                all_findings.extend(search_recursive(data, keywords))
            except:
                # Regex fallback for strings in the block
                strings = re.findall(r'"((?:[^"\\]|\\.)*)"', content_to_parse)
                for s in strings:
                    s_unquoted = s.replace('\\"', '"').replace('\\n', '\n')
                    if len(s_unquoted) > 50 and any(k in s_unquoted.lower() for k in keywords):
                        all_findings.append(s_unquoted)
        except:
            continue

    if all_findings:
        all_findings = list(set(all_findings))
        print(f"Found {len(all_findings)} relevant snippets.")
        output_path = "research_results_final.txt"
        with open(output_path, "w", encoding="utf-8") as f:
            for i, fnd in enumerate(all_findings):
                f.write(f"--- RESULT {i+1} ---\n{fnd}\n\n")
        print(f"Results saved to {output_path}")
    else:
        print("No relevant content found anywhere.")

if __name__ == "__main__":
    main()
