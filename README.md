# Health_Innovators

Call Entry (IVR Start)

Greet the caller.

  Ask them to choose:
  Press 1 for Emergency
  Press 2 for Non-Emergency

Emergency Flow (Option 1)
Collect:
Patient issue (voice or keypad)
User personal details (name, phone number)
Automatically prioritize appointment booking
Confirm details with the caller
Generate a token number
Announce and send the token number to the patient
End call

Non-Emergency Flow (Option 2)
Collect the following inputs step by step:
Issue description
Symptoms (choose from pre-loaded list: 1–9)
Age
Gender:
Press 1 for Male
Press 2 for Female
Status:
Press 1 for Normal
Press 2 for Child
Press 3 for Pregnant
Medication background details

AI Decision Engine
Analyze all collected inputs
Decide whether the case is:
Emergency
Non-Emergency

If AI Classifies as Emergency
Explain clearly why it is considered an emergency
Give options:
Press 1 to Book Appointment
Press 2 to Leave / End Call
If booking:
Collect remaining user details
Confirm appointment
End call

If AI Classifies as Non-Emergency
Provide appropriate guidance or next steps
