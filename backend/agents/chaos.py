from google.adk import Agent
from database import get_db_connection

class ChaosAgent:
    """
    The Chaos & Stress Test Agent.
    Analyzes student work, injects edge-case bugs, and adaptively challenges
    the student based on their historical performance.
    """
    def __init__(self):
        self.adk_agent = Agent(
            name="chaos_bug_tester",
            model="gemini-2.5-flash",
            instruction=(
                "You are the Chaos Agent. Your job is to inject bugs, "
                "stress-test data structures, and ask tough edge-case questions "
                "to ensure the student's algorithmic understanding is robust."
            )
        )

    def get_student_difficulty_level(self) -> str:
        """Query the local database to adapt difficulty level."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT SUM(score) FROM challenges")
            total_score = cursor.fetchone()[0] or 0
            conn.close()
        except Exception:
            total_score = 0
            
        if total_score < 50:
            return "Beginner"
        elif total_score < 150:
            return "Intermediate"
        else:
            return "Advanced"

    def inject_chaos(self, current_values: list) -> dict:
        """
        Generate a difficulty-adaptive edge-case challenge and a custom
        multiple-choice quiz question based on the current tree state.
        """
        level = self.get_student_difficulty_level()
        
        if level == "Beginner":
            # Edge Case: Searching for a value not present
            non_existent = 99
            while non_existent in current_values:
                non_existent = random.randint(100, 999)
                
            scenario = (
                f"🚨 [CHAOS INJECTED: Level {level}] - Search Boundary Check!\n"
                f"We are searching for a value that is NOT in the tree: {non_existent}.\n"
                "In a standard implementation, we would traverse all the way to a NULL node. "
                "If our code doesn't handle NULL references properly, it will crash with a NullPointerException!"
            )
            
            quiz_question = {
                "question": f"When searching for {non_existent} in your tree, what triggers the search to terminate?",
                "options": [
                    "It loops infinitely.",
                    "The search pointer reaches a NULL reference, indicating the value is not found.",
                    "The program crashes with an error.",
                    "It returns the root node."
                ],
                "answer_idx": 1,
                "explanation": "When we traverse left or right and find a NULL reference, it means there are no more nodes to check, so the element does not exist."
            }

        elif level == "Intermediate":
            # Edge Case: Duplicate Insertion
            duplicate = current_values[0] if current_values else 15
            scenario = (
                f"🚨 [CHAOS INJECTED: Level {level}] - Duplicate Value Inundation!\n"
                f"We are attempting to insert a value that already exists: {duplicate}.\n"
                "How does your algorithm react? Standard BSTs must either discard duplicates, "
                "store them in a separate count field, or consistently route them to the right."
            )
            
            quiz_question = {
                "question": f"If we insert the value {duplicate} a second time into a standard BST, what happens?",
                "options": [
                    "The tree balance is automatically adjusted.",
                    "The operation is either ignored, or it traverses left/right and attaches as a child depending on convention.",
                    "The original node is overwritten.",
                    "The tree splits into two separate trees."
                ],
                "answer_idx": 1,
                "explanation": "Typically, BSTs either ignore duplicates to save space, or treat them as >= and route them to the right subtree."
            }

        else:
            # Advanced Edge Case: Degenerate tree (skewed)
            scenario = (
                f"🚨 [CHAOS INJECTED: Level {level}] - Degenerate/Skewed Tree Threat!\n"
                "What if our input values are pre-sorted (e.g., 5, 10, 15, 20, 25)?\n"
                "The tree becomes a single line (essentially a linked list)! Our O(log N) search "
                "guarantee degenerates into O(N) linear time. This is where we MUST upgrade "
                "our tree to a self-balancing tree like an AVL Tree or Red-Black Tree."
            )
            
            quiz_question = {
                "question": "What is the worst-case time complexity of inserting N pre-sorted elements into a standard BST?",
                "options": [
                    "O(1)",
                    "O(log N)",
                    "O(N)",
                    "O(N^2)"
                ],
                "answer_idx": 2,
                "explanation": "If inputs are pre-sorted, each new node is placed to the extreme right of the previous one, forming a single chain of height N. Hence, operations take linear O(N) time."
            }

        return {
            "level": level,
            "scenario": scenario,
            "quiz_question": quiz_question
        }

if __name__ == "__main__":
    agent = ChaosAgent()
    res = agent.inject_chaos([15, 10, 20])
    print("Level:    ", res["level"])
    print("Scenario: ")
    print(res["scenario"])
    print("\nQuiz Question:")
    print(res["quiz_question"])
