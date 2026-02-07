token_counter = {
    "A": 1,
    "B": 1,
    "C": 1,
    "D": 1
}

def generate_token(priority):
    token = f"{priority}-ER-{str(token_counter[priority]).zfill(3)}"
    token_counter[priority] += 1
    return token
