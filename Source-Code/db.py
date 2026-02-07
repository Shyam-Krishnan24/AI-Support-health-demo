import traceback
import os

# Force SQLite fallback to avoid crashing on environments where mysql C-extension
# causes access violations (can be enabled via env var later if needed).
USE_SQLITE = True

import sqlite3


def get_db_path():
    """Get the database path - stored in the same directory as db.py"""
    db_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(db_dir, "health.sqlite")


def get_connection():
    # Always use sqlite for stability in the prototype environment
    # Database stored in Frontend folder for consistency
    return sqlite3.connect(get_db_path())


def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    if USE_SQLITE:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS ivr_calls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT,
            patient_phone TEXT,
            language TEXT,
            call_type TEXT,
            symptom TEXT,
            age INTEGER,
            gender TEXT,
            patient_status TEXT,
            past_surgery INTEGER,
            medications TEXT,
            urgency_score INTEGER,
            priority_level TEXT,
            token TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
    else:
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

    if USE_SQLITE:
        cursor.execute("""
        INSERT INTO ivr_calls
        (patient_name, patient_phone, language, call_type, symptom, age, gender, patient_status,
         past_surgery, medications, urgency_score, priority_level, token)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            data.get("patient_name"),
            data.get("patient_phone"),
            data.get("language"),
            data.get("call_type"),
            data.get("symptom"),
            data.get("age"),
            data.get("gender"),
            data.get("status"),
            1 if data.get("past_surgery") else 0,
            data.get("medications"),
            data.get("urgency_score"),
            data.get("priority"),
            data.get("token")
        ))
    else:
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
    row = cursor.fetchone()
    count = row[0] if row else 0
    if count == 0:
        samples = [
            ("Alice","+911234567890","English","Non-Emergency","Fever",30,"Female","Normal",0,"Paracetamol",30,"C","C-ER-001"),
            ("Bob","+919876543210","English","Emergency","Chest Pain",65,"Male","Normal",1,"Aspirin",95,"A","A-ER-001"),
            ("Carol","+911112223334","Tamil","Non-Emergency","Headache",25,"Female","Normal",0,"",20,"D","D-ER-001"),
        ]
        if USE_SQLITE:
            cursor.executemany("""
            INSERT INTO ivr_calls
            (patient_name, patient_phone, language, call_type, symptom, age, gender, patient_status,
             past_surgery, medications, urgency_score, priority_level, token)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, samples)
        else:
            cursor.executemany("""
            INSERT INTO ivr_calls
            (patient_name, patient_phone, language, call_type, symptom, age, gender, patient_status,
             past_surgery, medications, urgency_score, priority_level, token)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, samples)
        conn.commit()

    cursor.close()
    conn.close()
