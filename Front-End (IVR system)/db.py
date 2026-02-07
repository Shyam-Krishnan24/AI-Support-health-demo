import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="789632145",
        database="health"
    )


def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ivr_calls (
        id INT AUTO_INCREMENT PRIMARY KEY,
        patient_name VARCHAR(100),
        patient_phone VARCHAR(50),
        language VARCHAR(50),
        call_type VARCHAR(20),
        symptom TEXT,
        age INT,
        gender VARCHAR(20),
        patient_status VARCHAR(20),
        past_surgery BOOLEAN,
        medications TEXT,
        urgency_score INT,
        priority_level VARCHAR(5),
        token VARCHAR(20),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    cursor.close()
    conn.close()


def save_call(data):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO ivr_calls
    (patient_name, patient_phone, language, call_type, symptom, age, gender, patient_status,
     past_surgery, medications, urgency_score, priority_level, token)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        data.get("patient_name"),
        data.get("patient_phone"),
        data["language"],
        data["call_type"],
        data["symptom"],
        data["age"],
        data["gender"],
        data["status"],
        data["past_surgery"],
        data["medications"],
        data["urgency_score"],
        data["priority"],
        data["token"]
    ))

    conn.commit()
    cursor.close()
    conn.close()


def populate_sample_data():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM ivr_calls")
    count = cursor.fetchone()[0]
    if count == 0:
        samples = [
            ("Alice","+911234567890","English","Non-Emergency","Fever",30,"Female","Normal",False,"Paracetamol",30,"C","C-ER-001"),
            ("Bob","+919876543210","English","Emergency","Chest Pain",65,"Male","Normal",True,"Aspirin",95,"A","A-ER-001"),
            ("Carol","+911112223334","Tamil","Non-Emergency","Headache",25,"Female","Normal",False,"",20,"D","D-ER-001"),
        ]
        cursor.executemany("""
        INSERT INTO ivr_calls
        (patient_name, patient_phone, language, call_type, symptom, age, gender, patient_status,
         past_surgery, medications, urgency_score, priority_level, token)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, samples)
        conn.commit()

    cursor.close()
    conn.close()
