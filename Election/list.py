import pandas as pd
import random
from datetime import datetime, timedelta

# Configuration
NUM_RECORDS = 600
OUTPUT_FILE = "list.xlsx"

# Name banks
FIRST_NAMES = [
    "Kwaku", "Kwame", "Kofi", "Yaw", "Kwadwo", "Kwabena", "Kojo",
    "Akosua", "Adwoa", "Abena", "Akua", "Yaa", "Afua", "Ama",
    "Emmanuel", "Samuel", "David", "Daniel", "Michael", "Joseph",
    "Priscilla", "Harriet", "Esther", "Grace", "Patricia", "Ebenezer"
]

SURNAMES = [
    "Mensah", "Osei", "Appiah", "Agyei", "Boateng", "Owusu", "Kwarteng",
    "Opoku", "Obeng", "Donkor", "Frimpong", "Addo", "Bonsu", "Antwi",
    "Adjei", "Gyamfi", "Asante", "Agyemang", "Sarpong", "Quaye", "Tetteh"
]

PREFIXES = ["024", "025", "054", "055", "059", "020", "050", "027", "057"]

def get_valid_dob():
    """Generates DOB ensuring the person is strictly between 18 and 34 years old."""
    today = datetime(2026, 8, 27)
    
    # 18 to 34 years ago from today
    min_birth_date = today - timedelta(days=int(34 * 365.25)) # Oldest (34 yo)
    max_birth_date = today - timedelta(days=int(18 * 365.25)) # Youngest (18 yo)
    
    total_days = (max_birth_date - min_birth_date).days
    random_days = random.randint(0, total_days)
    dob = min_birth_date + timedelta(days=random_days)
    return dob.strftime("%Y-%m-%d")

def get_phone():
    """Generates a formatted 10-digit mobile number."""
    prefix = random.choice(PREFIXES)
    suffix = "".join([str(random.randint(0, 9)) for _ in range(7)])
    return f"{prefix}{suffix}"

# Generate 600 rows of data
data = []
for i in range(1, NUM_RECORDS + 1):
    data.append({
        "ID": 200 + i,
        "Full Name": f"{random.choice(FIRST_NAMES)} {random.choice(SURNAMES)}",
        "Date of Birth": get_valid_dob(),
        "Phone Number": get_phone()
    })

# Write directly to list.xlsx
df = pd.DataFrame(data)
df.to_excel(OUTPUT_FILE, index=False)

print(f"File created successfully: {OUTPUT_FILE} ({NUM_RECORDS} rows)")