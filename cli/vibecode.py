import sys
import argparse
import requests
import getpass

API_BASE = "http://127.0.0.1:8000/api"

def check_server():
    """Verify that the FastAPI backend is running."""
    try:
        requests.get(f"{API_BASE}/vault/status", timeout=2)
        return True
    except requests.exceptions.RequestException:
        print("❌ Error: VibeCode Academy Backend Server is not running on port 8000.")
        print("Please start it first using: npm start or python backend/main.py")
        return False

def handle_insert(prompt, eli5):
    if not check_server():
        return
        
    print(f"📡 Sending instruction to VibeCode Coordinator: '{prompt}'...")
    try:
        res = requests.post(
            f"{API_BASE}/session",
            json={"prompt": prompt, "eli5_mode": eli5}
        )
        if res.status_code != 200:
            print("❌ Coordinator Agent pipeline failed.")
            return
            
        data = res.json()
        print("\n=== 🛡️ Security Guard Sanitization Audit ===")
        print(f"Raw Input:      {data['security']['raw_prompt']}")
        print(f"Sanitized LLM:  {data['security']['sanitized_prompt']}")
        print(f"Redactions:     {data['security']['redacted_items_count']} items secured.")
        
        print("\n=== 📐 Algorithm Insertion Traversal Trace ===")
        for i, step in enumerate(data["trace"]):
            narrative = step["metaphor"] if eli5 else step["explanation"]
            print(f"Step {i+1}: {narrative}")
            
        print("\n=== 🎓 Coordinator Agent Summary ===")
        print(data["summary"])
        
    except Exception as e:
        print("❌ Connection error:", str(e))

def handle_benchmark(algo, ops):
    if not check_server():
        return
        
    print(f"📊 Querying MCP Server to benchmark {ops} operations of '{algo}'...")
    try:
        res = requests.post(
            f"{API_BASE}/benchmarks/run",
            json={"algorithm": algo, "num_operations": ops}
        )
        if res.status_code != 200:
            print("❌ Benchmark execution failed.")
            return
            
        data = res.json()
        print("\n=== 📈 MCP Server Benchmark Report ===")
        print(f"Algorithm:       {data['algorithm'].upper()}")
        print(f"Operations (N):  {data['num_operations']}")
        print(f"Time Elapsed:    {data['time_taken_ms']} ms")
        print(f"Big-O Estimate:  {data['complexity']}")
        print("Metrics successfully logged in local database.")
        
    except Exception as e:
        print("❌ Connection error:", str(e))

def handle_vault():
    if not check_server():
        return
        
    print("🔐 Secure Academic Vault Decryptor")
    passcode = getpass.getpass("Enter Vault Passcode: ")
    
    try:
        res = requests.post(
            f"{API_BASE}/vault/unlock",
            json={"passcode": passcode}
        )
        if res.status_code == 400:
            print("❌ Decryption failed! Invalid Vault Passcode (AES-256-GCM integrity check failed).")
            return
        elif res.status_code == 404:
            print("❌ No profile found. Please create a student profile first in the web dashboard.")
            return
            
        data = res.json()
        print("\n=== 🔓 Cryptographic Decryption Complete ===")
        print(f"Decrypted Profile: {data['profile']}")
        print(f"Grades & Logs:     {data['grades']}")
        
    except Exception as e:
        print("❌ Connection error:", str(e))

def handle_challenges():
    if not check_server():
        return
        
    try:
        res = requests.get(f"{API_BASE}/challenges")
        if res.status_code != 200:
            print("❌ Failed to fetch challenges.")
            return
            
        data = res.json()
        print("\n=== 🏆 Active Recall Study Challenges ===")
        print(f"{'Challenge Name':<30} | {'Status':<12} | {'Score':<6}")
        print("-" * 55)
        for c in data:
            print(f"{c['challenge_name']:<30} | {c['status']:<12} | {c['score']:<6}")
            
    except Exception as e:
        print("❌ Connection error:", str(e))

def main():
    parser = argparse.ArgumentParser(description="VibeCode Academy CLI - Academic Agent Skill")
    subparsers = parser.add_subparsers(dest="command")
    
    # Insert command
    parser_ins = subparsers.add_parser("insert", help="Insert list of values into a visual data structure")
    parser_ins.add_argument("prompt", type=str, help="Plain English description (e.g. 'insert 10, 5, 20')")
    parser_ins.add_argument("--eli5", action="store_true", help="Use simplified everyday metaphors")
    
    # Benchmark command
    parser_bench = subparsers.add_parser("benchmark", help="Benchmark performance using custom MCP server")
    parser_bench.add_argument("algorithm", choices=["bst", "avl", "bfs", "quicksort"], help="Target algorithm")
    parser_bench.add_argument("operations", type=int, help="Number of operations to execute")
    
    # Vault command
    subparsers.add_parser("vault", help="Decrypt and view the student secure academic vault")
    
    # Challenge command
    subparsers.add_parser("challenges", help="List active recall study challenges and scores")
    
    args = parser.parse_args()
    
    if args.command == "insert":
        handle_insert(args.prompt, args.eli5)
    elif args.command == "benchmark":
        handle_benchmark(args.algorithm, args.operations)
    elif args.command == "vault":
        handle_vault()
    elif args.command == "challenges":
        handle_challenges()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
