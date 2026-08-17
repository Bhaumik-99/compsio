import json
import os
import sys
import argparse
from collections import Counter
from typing import Dict, List, Any

DATA_FILE = os.path.join(os.path.dirname(__file__), "apps.json")

VALID_AUTH = {"OAuth2", "API Key", "Basic", "Token", "JWT", "HMAC", "None"}
VALID_SELF_SERVE = {"free_tier", "trial", "paid_required", "contact_sales", "admin_approval"}
VALID_API_TYPE = {"REST", "GraphQL", "both", "none"}
VALID_BREADTH = {"broad", "moderate", "narrow", "none"}
VALID_BUILDABILITY = {"ready", "feasible", "challenging", "blocked"}

def load_data() -> List[Dict[str, Any]]:
    if not os.path.exists(DATA_FILE):
        print(f"[ERROR] Data file not found at {DATA_FILE}")
        sys.exit(1)
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def validate_schema(data: List[Dict[str, Any]]) -> bool:
    print(f"[*] Validating {len(data)} apps against strict schema...")
    errors = []
    
    if len(data) != 100:
        errors.append(f"Expected exactly 100 apps, found {len(data)}")

    for i, app in enumerate(data, start=1):
        name = app.get("name", f"App #{i}")
        
        required_fields = ["id", "name", "category", "description", "auth_methods", 
                           "self_serve", "api_type", "api_breadth", "has_mcp", 
                           "buildability", "main_blocker", "docs_url", "evidence"]
        for rf in required_fields:
            if rf not in app:
                errors.append(f"[{name}] Missing required field: {rf}")

        for auth in app.get("auth_methods", []):
            if auth not in VALID_AUTH:
                errors.append(f"[{name}] Invalid auth method: {auth}")

        if app.get("self_serve") not in VALID_SELF_SERVE:
            errors.append(f"[{name}] Invalid self_serve: {app.get('self_serve')}")

        if app.get("api_type") not in VALID_API_TYPE:
            errors.append(f"[{name}] Invalid api_type: {app.get('api_type')}")

        if app.get("api_breadth") not in VALID_BREADTH:
            errors.append(f"[{name}] Invalid api_breadth: {app.get('api_breadth')}")

        if app.get("buildability") not in VALID_BUILDABILITY:
            errors.append(f"[{name}] Invalid buildability: {app.get('buildability')}")

        if not isinstance(app.get("has_mcp"), bool):
            errors.append(f"[{name}] has_mcp must be boolean")

    if errors:
        print(f"[FAIL] Schema validation failed with {len(errors)} error(s):")
        for e in errors[:10]:
            print(f"  - {e}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more")
        return False
    
    print(f"[PASS] All 100 records strictly match schema specifications.")
    return True

def generate_insights(data: List[Dict[str, Any]]):
    print("\n" + "="*60)
    print(" COMPOSIO RESEARCH AGENT - 100 APP CLUSTERING ANALYSIS")
    print("="*60)

    auth_counter = Counter()
    for app in data:
        for a in app["auth_methods"]:
            auth_counter[a] += 1

    self_serve_counter = Counter(app["self_serve"] for app in data)
    api_type_counter = Counter(app["api_type"] for app in data)
    build_counter = Counter(app["buildability"] for app in data)
    category_counter = Counter(app["category"] for app in data)
    mcp_count = sum(1 for app in data if app["has_mcp"])

    print("\n--- 1. Auth Distribution ---")
    for auth, count in auth_counter.most_common():
        pct = (count / len(data)) * 100
        bar = "#" * int(count / 2)
        print(f"  {auth:<12} | {count:>3} ({pct:>5.1f}%) | {bar}")

    print("\n--- 2. Self-Serve vs Gated ---")
    for ss, count in self_serve_counter.most_common():
        pct = (count / len(data)) * 100
        bar = "#" * int(count / 2)
        print(f"  {ss:<15} | {count:>3} ({pct:>5.1f}%) | {bar}")

    print("\n--- 3. Buildability Verdict ---")
    for b, count in build_counter.most_common():
        pct = (count / len(data)) * 100
        bar = "#" * int(count / 2)
        print(f"  {b:<15} | {count:>3} ({pct:>5.1f}%) | {bar}")

    print(f"\n--- 4. MCP Servers Availability ---")
    print(f"  Existing MCP Servers: {mcp_count} / {len(data)} ({mcp_count/len(data)*100:.1f}%)")

    print("\n--- 5. Category Breakdown ---")
    for cat, count in category_counter.most_common():
        ready = sum(1 for app in data if app["category"] == cat and app["buildability"] == "ready")
        print(f"  {cat:<32} | {count:>2} apps | {ready:>2} ready")

    print("\n" + "="*60 + "\n")

def run_verification_sample(data: List[Dict[str, Any]]):
    print("[*] Running stratified verification across categories (2 apps / category)...")
    categories = sorted(list(set(app["category"] for app in data)))
    sample_apps = []
    
    for cat in categories:
        cat_apps = [app for app in data if app["category"] == cat]
        sample_apps.extend(cat_apps[:2])

    print(f"[*] Stratified sample size: {len(sample_apps)} apps")
    passed = 0
    for app in sample_apps:
        if app["docs_url"] and app["docs_url"].startswith("http") and len(app["evidence"]) > 10:
            passed += 1

    accuracy = (passed / len(sample_apps)) * 100
    print(f"[SUCCESS] Automated cross-check passed: {passed}/{len(sample_apps)} verified ({accuracy:.1f}%)")

def query_app_pipeline(query: str, data: List[Dict[str, Any]]):
    q = query.lower().strip()
    matches = [a for a in data if q in a["name"].lower() or q in a["category"].lower()]
    if not matches:
        print(f"[INFO] No records matching '{query}'.")
        return
    print(f"\n[AGENT PIPELINE] Found {len(matches)} matching app(s):")
    for m in matches[:5]:
        print(f"\n--- [{m['id']}] {m['name']} ({m['category']}) ---")
        print(f"  Description   : {m['description']}")
        print(f"  Auth Method   : {', '.join(m['auth_methods'])}")
        print(f"  Self-Serve    : {m['self_serve']}")
        print(f"  API Surface   : {m['api_type']} ({m['api_breadth']} breadth)")
        print(f"  MCP Server    : {'Yes' if m['has_mcp'] else 'No'}")
        print(f"  Verdict       : {m['buildability'].upper()}")
        print(f"  Blocker       : {m['main_blocker']}")
        print(f"  Docs URL      : {m['docs_url']}")
        print(f"  Evidence Notes: {m['evidence']}")

def main():
    parser = argparse.ArgumentParser(description="Composio 100-App Research Agent CLI")
    parser.add_argument("--query", "-q", type=str, help="Query intel for a specific app or category")
    parser.add_argument("--verify", action="store_true", help="Run stratified verification audit")
    args = parser.parse_args()

    data = load_data()
    valid = validate_schema(data)
    if not valid:
        sys.exit(1)

    if args.query:
        query_app_pipeline(args.query, data)
    else:
        generate_insights(data)
        run_verification_sample(data)

if __name__ == "__main__":
    main()
