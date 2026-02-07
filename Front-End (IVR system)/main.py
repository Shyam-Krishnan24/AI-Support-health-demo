from ivr import start_call
from db import create_table, populate_sample_data

if __name__ == "__main__":
    create_table()
    try:
        populate_sample_data()
    except Exception:
        pass
    start_call()
