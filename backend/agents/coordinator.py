from agents.security import SecurityAgent
from agents.architect import ArchitectAgent
from agents.chaos import ChaosAgent

class LearningCoordinatorAgent:
    """
    The central Learning Coordinator Agent.
    Orchestrates the multi-agent execution pipeline:
    Security -> Architect -> Chaos -> Output Compilation.
    """
    
    def __init__(self):
        self.security_agent = SecurityAgent()
        self.architect_agent = ArchitectAgent()
        self.chaos_agent = ChaosAgent()

    def process_session(self, raw_prompt: str, eli5_mode: bool = False) -> dict:
        """
        Run the complete multi-agent pipeline and compile the session payload.
        """
        # 1. Run Security Agent (PII & IP Sanitization)
        sanitized_prompt, pii_map = self.security_agent.sanitize(raw_prompt)
        
        # 2. Run Architect Agent (DSA parsing, layout calculations, traversal tracing)
        architect_res = self.architect_agent.parse_and_build(sanitized_prompt, eli5_mode)
        
        # 3. Run Chaos Agent (difficulty-adaptive edge-case analysis & custom quiz)
        chaos_res = self.chaos_agent.inject_chaos(architect_res["values"])
        
        # 4. Synthesize Audio Narration Script
        # We write a friendly narrator script that explains the nodes being traversed.
        narrations = []
        for step in architect_res["trace"]:
            # Pick metaphor if eli5_mode, else standard explanation
            narrative = step["metaphor"] if eli5_mode else step["explanation"]
            narrations.append(narrative)
            
        # 5. Re-integrate PII locally for the Coordinator's summary response
        # (This simulates the LLM responding back, and we translate it back for the user)
        coordinator_summary = self.security_agent.restore(architect_res["summary"], pii_map)
        
        # Assemble complete visual and interactive state payload
        payload = {
            "security": {
                "is_guarded": True,
                "raw_prompt": raw_prompt,
                "sanitized_prompt": sanitized_prompt,
                "redacted_items_count": len(pii_map)
            },
            "algorithm": architect_res["algorithm"],
            "values": architect_res["values"],
            "nodes": architect_res["nodes"],
            "trace": architect_res["trace"],
            "narrations": narrations,
            "chaos": {
                "level": chaos_res["level"],
                "scenario": chaos_res["scenario"],
                "quiz_question": chaos_res["quiz_question"]
            },
            "summary": coordinator_summary
        }
        
        return payload

if __name__ == "__main__":
    # Quick test of the complete multi-agent coordination
    coordinator = LearningCoordinatorAgent()
    prompt = "Hi I am Alex, testing Homework #2! Let's insert 12, 8, 16 into a BST"
    session = coordinator.process_session(prompt, eli5_mode=True)
    
    print("--- Coordination Pipeline Test ---")
    print("Security Raw:      ", session["security"]["raw_prompt"])
    print("Security Sanitized:", session["security"]["sanitized_prompt"])
    print("Algorithm Values:  ", session["values"])
    print("Chaos Level:       ", session["chaos"]["level"])
    print("Chaos Scenario:    ", session["chaos"]["scenario"])
    print("Summary:           ", session["summary"])
