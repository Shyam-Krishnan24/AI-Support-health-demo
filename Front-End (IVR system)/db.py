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
    (language, call_type, symptom, age, gender, patient_status,
     past_surgery, medications, urgency_score, priority_level, token)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
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
