def detect_closure(user_query: str):
    explicit_endings = ["exit", "end conversation", "quit", "goodbye"]
    soft_endings = ["thanks", "i feel better", "that’s enough", "i got it", "no worries", "appreciate it"]
    
    q_lower = user_query.lower()
    if any(phrase in q_lower for phrase in explicit_endings):
        return "explicit"
    elif any(phrase in q_lower for phrase in soft_endings):
        return "soft"
    return None
