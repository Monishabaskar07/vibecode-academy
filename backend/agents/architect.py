import re
import json
from google.adk import Agent

class LocalBST:
    """Helper class to build a BST locally and calculate coordinates and traces."""
    def __init__(self):
        self.nodes = {}
        self.root_id = None
        self.trace = []

    def insert(self, value, eli5_mode=False):
        val_str = str(value)
        if not self.root_id:
            self.root_id = val_str
            self.nodes[val_str] = {
                "id": val_str, "value": value, 
                "left": None, "right": None, 
                "x": 400, "y": 80
            }
            metaphor = "We plant our first seed, {}, right in the center to start our tree!".format(value)
            self.trace.append({
                "type": "insert_root",
                "value": value,
                "node_id": val_str,
                "visited": [val_str],
                "explanation": f"Set {value} as the root node.",
                "metaphor": metaphor
            })
            return

        curr = self.nodes[self.root_id]
        visited = []
        
        while True:
            visited.append(curr["id"])
            curr_val = curr["value"]
            
            if value < curr_val:
                if curr["left"] is None:
                    # Place left
                    curr["left"] = val_str
                    self.nodes[val_str] = {
                        "id": val_str, "value": value,
                        "left": None, "right": None,
                        "x": 0, "y": 0 # to be computed
                    }
                    metaphor = "{} is smaller than {}, so we slide down the left slide to find its home!".format(value, curr_val)
                    self.trace.append({
                        "type": "insert_left",
                        "value": value,
                        "node_id": val_str,
                        "visited": list(visited) + [val_str],
                        "explanation": f"{value} < {curr_val}. Placed {value} to the left of {curr_val}.",
                        "metaphor": metaphor
                    })
                    break
                else:
                    curr = self.nodes[curr["left"]]
            else:
                if curr["right"] is None:
                    # Place right
                    curr["right"] = val_str
                    self.nodes[val_str] = {
                        "id": val_str, "value": value,
                        "left": None, "right": None,
                        "x": 0, "y": 0 # to be computed
                    }
                    metaphor = "{} is bigger than {}, so it climbs up the right ladder to find its home!".format(value, curr_val)
                    self.trace.append({
                        "type": "insert_right",
                        "value": value,
                        "node_id": val_str,
                        "visited": list(visited) + [val_str],
                        "explanation": f"{value} >= {curr_val}. Placed {value} to the right of {curr_val}.",
                        "metaphor": metaphor
                    })
                    break
                else:
                    curr = self.nodes[curr["right"]]

    def compute_coordinates(self, node_id, x, y, x_offset):
        """Recursively calculate balanced x, y coordinates for rendering."""
        if not node_id:
            return
        node = self.nodes[node_id]
        node["x"] = x
        node["y"] = y
        
        # Left child
        if node["left"]:
            self.compute_coordinates(node["left"], x - x_offset, y + 90, x_offset * 0.5)
        # Right child
        if node["right"]:
            self.compute_coordinates(node["right"], x + x_offset, y + 90, x_offset * 0.5)

class ArchitectAgent:
    """
    The DSA Structure Architect Agent.
    Interprets natural language prompts to build data structures.
    """
    def __init__(self):
        # We define a standard ADK agent for integration
        self.adk_agent = Agent(
            name="dsa_architect",
            model="gemini-2.5-flash",
            instruction=(
                "You are a Data Structures and Algorithms visual architect. "
                "Analyze the user's request, extract the numbers to insert, "
                "and explain the tree insertion logic step-by-step."
            )
        )

    def parse_and_build(self, prompt: str, eli5_mode: bool = False) -> dict:
        """
        Extract numbers from the prompt, construct a local BST,
        and generate coordinates, trace steps, and explanations.
        """
        # Find all numbers in the prompt
        numbers = [int(n) for n in re.findall(r'\b\d+\b', prompt)]
        
        if not numbers:
            # Seed default values if none found
            numbers = [15, 10, 20, 8, 12, 17, 25]
            
        # Limit to max 12 numbers for beautiful visual layout
        numbers = numbers[:12]

        bst = LocalBST()
        for num in numbers:
            bst.insert(num, eli5_mode)
            
        # Compute coordinates starting from root (x=400, y=80)
        if bst.root_id:
            bst.compute_coordinates(bst.root_id, 400, 80, 160)

        # Build list format of nodes for frontend
        node_list = list(bst.nodes.values())
        
        # Generate general summary explanation
        summary = (
            f"Created a Binary Search Tree by inserting the elements: {', '.join(map(str, numbers))}. "
            "Smaller values branch left, while larger values branch right."
        )

        return {
            "algorithm": "bst",
            "values": numbers,
            "nodes": node_list,
            "trace": bst.trace,
            "summary": summary
        }

if __name__ == "__main__":
    agent = ArchitectAgent()
    res = agent.parse_and_build("Create a BST with 15, 10, 20, 12", eli5_mode=True)
    print("Nodes calculated:")
    for node in res["nodes"]:
        print(f"  Node {node['value']}: x={node['x']}, y={node['y']}, left={node['left']}, right={node['right']}")
    print("\nTrace sample:")
    print(json.dumps(res["trace"][3], indent=2))
