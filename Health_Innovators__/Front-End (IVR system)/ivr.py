from languages import LANGUAGES
from symptoms import SYMPTOMS
from ai_engine import calculate_urgency, assign_priority
from scheduler import generate_token
from db import save_call
import voice


def _get_input(prompt, allow_voice=True):
    # Try voice listen first (if available), fallback to typed input
    if allow_voice:
        resp = voice.listen(prompt)
        if resp:
            return resp
    # Fallback
    try:
        return input(prompt + " (type): ").strip()
    except Exception:
        return ""


def start_call():
    voice.speak("Welcome to Smart Health IVR. Please select a language from the console list.")
    print("\nSelect Language:")
    for k, v in LANGUAGES.items():
        print(f"{k}. {v['name']}")

    lang = _get_input("Enter language choice number", allow_voice=False)
    language = LANGUAGES.get(lang, LANGUAGES["1"])["name"]
    voice.speak(LANGUAGES.get(lang, LANGUAGES["1"])["welcome"])

    voice.speak("Press 1 for Emergency. Press 2 for Non-Emergency.")
    print("\nPress 1 for Emergency")
    print("Press 2 for Non-Emergency")
    call_type = _get_input("Choice (1/2)")

    if call_type == "1":
        handle_emergency(language)
    else:
        handle_non_emergency(language)


def handle_non_emergency(language):
    voice.speak("Please select your symptom from the list shown on console or say your symptom.")
    print("\nSelect Symptom:")
    for k, v in SYMPTOMS.items():
        print(f"{k}. {v}")

    s = _get_input("Choice number or say symptom")
    symptom = SYMPTOMS.get(s, None)
    if not symptom:
        if s and s.isdigit():
            symptom = SYMPTOMS.get(s, "Unknown")
        else:
            symptom = s or "Unknown"

    age_raw = _get_input("Enter age")
    try:
        age = int(age_raw)
    except Exception:
        age = None

    voice.speak("Select gender: 1 for Male, 2 for Female, 3 for Non-binary")
    print("Gender: 1. Male  2. Female  3. Non-binary")
    gender_map = {"1": "Male", "2": "Female", "3": "Non-binary"}
    gender = gender_map.get(_get_input("Choice"), "Unknown")

    voice.speak("Select status: 1 for Normal, 2 for Child, 3 for Pregnant")
    print("Status: 1. Normal  2. Child  3. Pregnant")
    status_map = {"1": "Normal", "2": "Child", "3": "Pregnant"}
    status = status_map.get(_get_input("Choice"), "Normal")

    past_surgery = _get_input("Past surgery? say yes or no").lower() == "yes"
    medications = _get_input("Current medications (say 'none' if none)")

    data = {
        "symptom": symptom,
        "age": age or 0,
        "status": status,
        "past_surgery": past_surgery,
        "medications": medications
    }

    score = calculate_urgency(data)
    priority = assign_priority(score)
    token = generate_token(priority)

    voice.speak(f"AI Urgency Score is {score}. Priority level {priority}.")
    print(f"\nAI Urgency Score: {score}")
    print(f"Priority Level: {priority}")

    # If AI decides emergency
    if priority in ["A", "B"]:
        voice.speak("Based on the information provided, this case is classified as an emergency.")
        voice.speak("Press 1 to Book Appointment now. Press 2 to End the call.")
        print("1. Book Appointment")
        print("2. Leave / End Call")
        choice = _get_input("Choice (1/2)")
        if choice == "1":
            name = _get_input("Please say or type your full name")
            phone = _get_input("Please say or type your phone number")
            # confirm
            voice.speak(f"Confirming appointment for {name}, phone {phone}. Your token is {token}.")
            save_call({
                "patient_name": name,
                "patient_phone": phone,
                "language": language,
                "call_type": "Non-Emergency (Escalated)",
                "symptom": symptom,
                "age": age,
                "gender": gender,
                "status": status,
                "past_surgery": past_surgery,
                "medications": medications,
                "urgency_score": score,
                "priority": priority,
                "token": token
            })
            voice.speak(f"Your appointment is booked. Token number {token}. Please proceed to the emergency desk.")
        else:
            save_call({
                "patient_name": None,
                "patient_phone": None,
                "language": language,
                "call_type": "Non-Emergency (Escalated-NoBook)",
                "symptom": symptom,
                "age": age,
                "gender": gender,
                "status": status,
                "past_surgery": past_surgery,
                "medications": medications,
                "urgency_score": score,
                "priority": priority,
                "token": token
            })
            voice.speak("Okay. Your details are recorded. Please seek immediate help if condition worsens.")
    else:
        # Non-emergency guidance
        voice.speak("This is classified as non-emergency. Follow routine consultation steps.")
        voice.speak(f"Your token number is {token}. You may wait for routine consultation.")
        save_call({
            "patient_name": None,
            "patient_phone": None,
            "language": language,
            "call_type": "Non-Emergency",
            "symptom": symptom,
            "age": age,
            "gender": gender,
            "status": status,
            "past_surgery": past_surgery,
            "medications": medications,
            "urgency_score": score,
            "priority": priority,
            "token": token
        })

    print("\nYour details have been recorded successfully.")


def handle_emergency(language):
    voice.speak("You selected Emergency. Please briefly describe the patient issue or press/enter 1 to type it.")
    issue = _get_input("Describe the issue or press 1 to type")
    if issue == "1" or issue.strip() == "":
        issue = _get_input("Please type the issue now", allow_voice=False)

    name = _get_input("Please say or type patient's full name")
    phone = _get_input("Please say or type patient's phone number")

    token = generate_token("A")
    voice.speak("Emergency case registered. Generating token now.")
    voice.speak(f"Your priority token is {token}. Please proceed immediately to the emergency desk.")

    save_call({
        "patient_name": name,
        "patient_phone": phone,
        "language": language,
        "call_type": "Emergency",
        "symptom": issue or "Emergency Call",
        "age": None,
        "gender": None,
        "status": None,
        "past_surgery": False,
        "medications": None,
        "urgency_score": 100,
        "priority": "A",
        "token": token
    })
