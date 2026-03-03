def should_escalate(sentiment: dict, threshold: float = 0.8) -> bool:
    if sentiment["label"] == "Negative":
        return sentiment["confidence"] > threshold
    return False




