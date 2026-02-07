def calculate_urgency(data):
    score = 0

    # Symptom risk
    high_risk = ["Chest Pain", "Breathing Difficulty", "Injury / Bleeding"]
    if data["symptom"] in high_risk:
        score += 50
    else:
        score += 20

    # Age risk
    if data["age"] > 60:
        score += 15

    # Status risk
    if data["status"] in ["Child", "Pregnant"]:
        score += 20

    # Past surgery
    if data["past_surgery"]:
        score += 10

    # Medication interaction risk
    if data["medications"]:
        score += 5

    return min(score, 100)


def assign_priority(score):
    if score >= 90:
        return "A"
    elif score >= 70:
        return "B"
    elif score >= 40:
        return "C"
    else:
        return "D"
