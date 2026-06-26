import re

class SecurityAgent:
    """
    The Security & IP Guard Agent.
    Protects student privacy and academic IP by redacting sensitive data (PII)
    locally before it is sent to external LLM APIs, and restoring it upon return.
    """
    
    def __init__(self):
        # A simple, high-speed local regex pattern bank for PII detection
        self.patterns = {
            "EMAIL": r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',
            "STUDENT_ID": r'\b\d{7,10}\b', # standard 7-10 digit student IDs
            "STUDENT_NAME": r'\b(Alex|Moniii|John|Sarah|Doe|Smith|Professor)\b', # seed common names, can expand
            "IP_HEADER": r'\b(?:Homework|Assignment|Project|Lab)\s*#?\s*\d+\b' # proprietary assignments
        }

    def sanitize(self, raw_prompt: str) -> tuple[str, dict]:
        """
        Scan and redact PII/IP from the prompt.
        Returns the sanitized prompt and the local key mapping.
        """
        sanitized = raw_prompt
        mapping = {}
        counter = 1
        
        # 1. Redact Emails
        emails = re.findall(self.patterns["EMAIL"], sanitized)
        for email in set(emails):
            placeholder = f"[REDACTED_EMAIL_{counter}]"
            mapping[placeholder] = email
            sanitized = sanitized.replace(email, placeholder)
            counter += 1
            
        # 2. Redact Student IDs
        ids = re.findall(self.patterns["STUDENT_ID"], sanitized)
        for std_id in set(ids):
            placeholder = f"[REDACTED_ID_{counter}]"
            mapping[placeholder] = std_id
            sanitized = sanitized.replace(std_id, placeholder)
            counter += 1
            
        # 3. Redact Assignment Headers (protecting school IP)
        headers = re.findall(self.patterns["IP_HEADER"], sanitized, re.IGNORECASE)
        for header in set(headers):
            placeholder = f"[REDACTED_ASSIGNMENT_{counter}]"
            mapping[placeholder] = header
            sanitized = sanitized.replace(header, placeholder)
            counter += 1

        # 4. Redact Student Names (Case insensitive match from our list)
        for name in ["Moniii", "Alex", "John", "Sarah", "Doe"]:
            # Match word boundary
            matches = re.findall(rf'\b{name}\b', sanitized, re.IGNORECASE)
            for match in set(matches):
                placeholder = f"[REDACTED_STUDENT_{counter}]"
                mapping[placeholder] = match
                sanitized = re.sub(rf'\b{match}\b', placeholder, sanitized)
                counter += 1

        return sanitized, mapping

    def restore(self, sanitized_response: str, mapping: dict) -> str:
        """
        Restore the original PII details in the response for the student.
        """
        restored = sanitized_response
        for placeholder, original in mapping.items():
            restored = restored.replace(placeholder, original)
        return restored

if __name__ == "__main__":
    # Local quick test
    agent = SecurityAgent()
    raw = "Hi, my name is Moniii (student id: 9876543) working on Homework #3. Can you explain AVL trees?"
    sanitized, mapping = agent.sanitize(raw)
    print("Raw:      ", raw)
    print("Sanitized:", sanitized)
    print("Mapping:  ", mapping)
    print("Restored: ", agent.restore(f"Hello [REDACTED_STUDENT_4], let's look at [REDACTED_ASSIGNMENT_3]...", mapping))
