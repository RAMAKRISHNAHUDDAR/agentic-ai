def plan_study(subject, remaining_topics, available_minutes):
    """Choose the next study session using current progress and time available."""
    if not subject.strip():
        return {"question": "Which subject are you working on?"}
    if remaining_topics <= 0:
        return {"plan": f"All topics covered. Self-test in {subject.strip()} and review any mistakes."}
    if available_minutes < 10:
        return {"plan": f"Use flashcards to recall one key idea in {subject.strip()}."}
    topics = min(remaining_topics, max(1, available_minutes // 20))
    minutes = available_minutes // topics
    return {"plan": f"Work through {topics} of the {remaining_topics} remaining topics in {subject.strip()}, "
                    f"allowing {minutes} minutes per topic. Finish each with a practice question."}
