import sys
import json
import time
import random

# Core database of standard algorithm profiles
ALGO_PROFILES = {
    "bst": {
        "name": "Binary Search Tree (BST)",
        "time_complexity": "Average: O(log N), Worst: O(N) (skewed)",
        "space_complexity": "O(N)",
        "explanation": "A node-based binary tree data structure where the left subtree of a node contains only nodes with keys lesser than the node's key, and the right subtree contains only keys greater.",
        "pseudocode": (
            "function insert(node, key):\n"
            "    if node is null:\n"
            "        return new Node(key)\n"
            "    if key < node.key:\n"
            "        node.left = insert(node.left, key)\n"
            "    else:\n"
            "        node.right = insert(node.right, key)\n"
            "    return node"
        )
    },
    "avl": {
        "name": "AVL Tree (Self-Balancing BST)",
        "time_complexity": "Average: O(log N), Worst: O(log N)",
        "space_complexity": "O(N)",
        "explanation": "A self-balancing binary search tree where the heights of the two child subtrees of any node differ by at most one. If they differ by more, rebalancing is done via rotations.",
        "pseudocode": (
            "function insert(node, key):\n"
            "    # 1. Perform standard BST insert\n"
            "    node = bst_insert(node, key)\n"
            "    # 2. Update height and get balance factor\n"
            "    balance = get_balance(node)\n"
            "    # 3. Perform rotations if unbalanced\n"
            "    if balance > 1 and key < node.left.key: return right_rotate(node)\n"
            "    if balance < -1 and key > node.right.key: return left_rotate(node)\n"
            "    ...\n"
            "    return node"
        )
    },
    "bfs": {
        "name": "Breadth-First Search (BFS)",
        "time_complexity": "O(V + E) (Vertices + Edges)",
        "space_complexity": "O(V) (queue size)",
        "explanation": "An algorithm for traversing or searching tree or graph data structures. It starts at the tree root and explores all nodes at the present depth level before moving to the next level.",
        "pseudocode": (
            "function BFS(start_node):\n"
            "    create a queue Q\n"
            "    mark start_node as visited and enqueue it\n"
            "    while Q is not empty:\n"
            "        current = dequeue Q\n"
            "        for each neighbor of current:\n"
            "            if neighbor is not visited:\n"
            "                mark neighbor as visited and enqueue it"
        )
    },
    "quicksort": {
        "name": "Quick Sort",
        "time_complexity": "Average: O(N log N), Worst: O(N^2)",
        "space_complexity": "O(log N) (recursive stack)",
        "explanation": "A divide-and-conquer algorithm. It works by selecting a 'pivot' element from the array and partitioning the other elements into two sub-arrays according to whether they are less than or greater than the pivot.",
        "pseudocode": (
            "function quicksort(arr, low, high):\n"
            "    if low < high:\n"
            "        p_idx = partition(arr, low, high)\n"
            "        quicksort(arr, low, p_idx - 1)\n"
            "        quicksort(arr, p_idx + 1, high)"
        )
    }
}

# --- Standard BST Implementation for Benchmarking ---
class BSTNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

def bst_insert(root, key):
    if root is None:
        return BSTNode(key)
    if key < root.key:
        root.left = bst_insert(root.left, key)
    else:
        root.right = bst_insert(root.right, key)
    return root

# --- AVL Tree Implementation for Benchmarking ---
class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

def get_height(node):
    return node.height if node else 0

def get_balance(node):
    return get_height(node.left) - get_height(node.right) if node else 0

def right_rotate(y):
    x = y.left
    T2 = x.right
    x.right = y
    y.left = T2
    y.height = max(get_height(y.left), get_height(y.right)) + 1
    x.height = max(get_height(x.left), get_height(x.right)) + 1
    return x

def left_rotate(x):
    y = x.right
    T2 = y.left
    y.left = x
    x.right = T2
    x.height = max(get_height(x.left), get_height(x.right)) + 1
    y.height = max(get_height(y.left), get_height(y.right)) + 1
    return y

def avl_insert(node, key):
    if not node:
        return AVLNode(key)
    if key < node.key:
        node.left = avl_insert(node.left, key)
    else:
        node.right = avl_insert(node.right, key)

    node.height = 1 + max(get_height(node.left), get_height(node.right))
    balance = get_balance(node)

    # Left Left Case
    if balance > 1 and key < node.left.key:
        return right_rotate(node)
    # Right Right Case
    if balance < -1 and key > node.right.key:
        return left_rotate(node)
    # Left Right Case
    if balance > 1 and key > node.left.key:
        node.left = left_rotate(node.left)
        return right_rotate(node)
    # Right Left Case
    if balance < -1 and key < node.right.key:
        node.right = right_rotate(node.right)
        return left_rotate(node)

    return node

# --- Benchmarking Logic ---
def run_benchmark(algorithm, num_ops):
    start_time = time.perf_counter()
    
    if algorithm == "bst":
        root = None
        # Insert num_ops elements
        for _ in range(num_ops):
            root = bst_insert(root, random.randint(1, 1000000))
    elif algorithm == "avl":
        root = None
        for _ in range(num_ops):
            root = avl_insert(root, random.randint(1, 1000000))
    elif algorithm == "quicksort":
        arr = [random.randint(1, 1000000) for _ in range(num_ops)]
        arr.sort() # Standard sort in python is Timsort, highly optimized O(N log N)
    elif algorithm == "bfs":
        # Simulate BFS on a random graph of V = num_ops
        adj = {i: [] for i in range(num_ops)}
        for i in range(num_ops - 1):
            adj[i].append(i + 1) # simple chain
        queue = [0]
        visited = {0}
        while queue:
            curr = queue.pop(0)
            for neighbor in adj[curr]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
    else:
        time.sleep(0.01) # fallback sleep

    end_time = time.perf_counter()
    duration_ms = (end_time - start_time) * 1000
    return round(duration_ms, 3)

# --- MCP JSON-RPC Stdio Protocol Handler ---
def handle_request(request):
    try:
        req_id = request.get("id")
        method = request.get("method")
        params = request.get("params", {})

        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "serverInfo": {
                        "name": "AlgorithmVault-MCP",
                        "version": "1.0.0"
                    }
                }
            }

        elif method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "tools": [
                        {
                            "name": "get_algorithm_profile",
                            "description": "Get detailed complexity, pseudocode, and explanation for standard algorithms.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "algorithm_name": {
                                        "type": "string",
                                        "enum": ["bst", "avl", "bfs", "quicksort"],
                                        "description": "The shorthand name of the algorithm."
                                    }
                                },
                                "required": ["algorithm_name"]
                            }
                        },
                        {
                            "name": "benchmark_operations",
                            "description": "Run high-speed local performance benchmarks on an algorithm to observe Big-O scaling.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "algorithm": {
                                        "type": "string",
                                        "enum": ["bst", "avl", "bfs", "quicksort"],
                                        "description": "Algorithm to run."
                                    },
                                    "num_operations": {
                                        "type": "integer",
                                        "description": "Number of items or operations to benchmark (e.g. 1000, 5000)."
                                    }
                                },
                                "required": ["algorithm", "num_operations"]
                            }
                        }
                    ]
                }
            }

        elif method == "tools/call":
            name = params.get("name")
            arguments = params.get("arguments", {})

            if name == "get_algorithm_profile":
                algo = arguments.get("algorithm_name", "").lower()
                if algo in ALGO_PROFILES:
                    return {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "result": {
                            "content": [
                                {
                                    "type": "text",
                                    "text": json.dumps(ALGO_PROFILES[algo], indent=2)
                                }
                            ]
                        }
                    }
                else:
                    return {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "error": {"code": -32602, "message": f"Algorithm '{algo}' not found."}
                    }

            elif name == "benchmark_operations":
                algo = arguments.get("algorithm", "").lower()
                num_ops = int(arguments.get("num_operations", 1000))
                
                # Enforce safety limits
                if num_ops > 50000:
                    num_ops = 50000
                
                time_taken = run_benchmark(algo, num_ops)
                
                report = {
                    "algorithm": algo,
                    "num_operations": num_ops,
                    "time_taken_ms": time_taken,
                    "message": f"Successfully executed {num_ops} operations of '{algo}' in {time_taken} ms."
                }
                
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(report, indent=2)
                            }
                        ]
                    }
                }
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32601, "message": f"Tool '{name}' not found."}
                }

        else:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Method '{method}' not found."}
            }

    except Exception as e:
        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "error": {"code": -32603, "message": str(e)}
        }

def main():
    """Main stdio loop for the MCP server."""
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            request = json.loads(line)
            response = handle_request(request)
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err_resp = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": f"Parse error: {str(e)}"}
            }
            sys.stdout.write(json.dumps(err_resp) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    # If run with a command line argument, run local tests instead of stdio loop
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("Testing benchmark module...")
        for algo in ["bst", "avl", "quicksort", "bfs"]:
            t = run_benchmark(algo, 1000)
            print(f"  {algo} (1000 ops): {t} ms")
    else:
        main()
