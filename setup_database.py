import sqlite3
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()
Faker.seed(42)
random.seed(42)

def create_database():
    conn = sqlite3.connect('clinic.db')
    cursor = conn.cursor()

    # Drop tables if they exist for clean setup
    cursor.execute('DROP TABLE IF EXISTS invoices')
    cursor.execute('DROP TABLE IF EXISTS treatments')
    cursor.execute('DROP TABLE IF EXISTS appointments')
    cursor.execute('DROP TABLE IF EXISTS doctors')
    cursor.execute('DROP TABLE IF EXISTS patients')

    # Table 1: patients
    cursor.execute('''
        CREATE TABLE patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            date_of_birth DATE,
            gender TEXT,
            city TEXT,
            registered_date DATE
        )
    ''')

    # Table 2: doctors
    cursor.execute('''
        CREATE TABLE doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            specialization TEXT,
            department TEXT,
            phone TEXT
        )
    ''')

    # Table 3: appointments
    cursor.execute('''
        CREATE TABLE appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            doctor_id INTEGER,
            appointment_date DATETIME,
            status TEXT,
            notes TEXT,
            FOREIGN KEY (patient_id) REFERENCES patients (id),
            FOREIGN KEY (doctor_id) REFERENCES doctors (id)
        )
    ''')
    
    # Table 4: treatments
    cursor.execute('''
        CREATE TABLE treatments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            appointment_id INTEGER,
            treatment_name TEXT,
            cost REAL,
            duration_minutes INTEGER,
            FOREIGN KEY (appointment_id) REFERENCES appointments (id)
        )
    ''')

    # Table 5: invoices
    cursor.execute('''
        CREATE TABLE invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            invoice_date DATE,
            total_amount REAL,
            paid_amount REAL,
            status TEXT,
            FOREIGN KEY (patient_id) REFERENCES patients (id)
        )
    ''')
    
    # Insert Data
    
    # 1. Doctors (15 doctors across 5 specializations)
    specializations = [
        ("Dermatology", "Skin Care"),
        ("Cardiology", "Heart Center"),
        ("Orthopedics", "Bone & Joint"),
        ("General", "Primary Care"),
        ("Pediatrics", "Children's Health")
    ]
    doctors_data = []
    for _ in range(15):
        spec = random.choice(specializations)
        doc_name = fake.name()
        if not doc_name.startswith("Dr."):
            doc_name = "Dr. " + doc_name.split()[-1]
        doctors_data.append((
            doc_name,
            spec[0],
            spec[1],
            fake.phone_number()
        ))
    cursor.executemany('''
        INSERT INTO doctors (name, specialization, department, phone)
        VALUES (?, ?, ?, ?)
    ''', doctors_data)
    
    # 2. Patients (200)
    cities = [fake.city() for _ in range(10)]
    patients_data = []
    for _ in range(200):
        gender = random.choice(['M', 'F'])
        first_name = fake.first_name_male() if gender == 'M' else fake.first_name_female()
        
        patients_data.append((
            first_name,
            fake.last_name(),
            fake.email() if random.random() > 0.2 else None,
            fake.phone_number() if random.random() > 0.1 else None,
            fake.date_of_birth(minimum_age=1, maximum_age=90).isoformat(),
            gender,
            random.choice(cities),
            fake.date_between(start_date='-2y', end_date='today').isoformat()
        ))
    cursor.executemany('''
        INSERT INTO patients (first_name, last_name, email, phone, date_of_birth, gender, city, registered_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', patients_data)
    
    # 3. Appointments (500)
    appointment_statuses = ['Completed', 'Completed', 'Scheduled', 'Cancelled', 'No-Show']
    appointments_data = []
    now = datetime.now()
    for _ in range(500):
        # random date in last 12 months (or future if scheduled)
        days_offset = random.randint(-365, 30)
        app_date = (now + timedelta(days=days_offset)).replace(hour=random.randint(9, 16), minute=random.choice([0, 15, 30, 45]), second=0, microsecond=0)
        
        status = random.choice(appointment_statuses)
        if app_date > now:
            status = random.choice(['Scheduled', 'Cancelled'])
        elif status == 'Scheduled':
            status = 'Completed'

        appointments_data.append((
            random.randint(1, 200),  # patient_id
            random.randint(1, 15),   # doctor_id
            app_date.isoformat(),
            status,
            fake.sentence() if random.random() > 0.5 else None
        ))
    cursor.executemany('''
        INSERT INTO appointments (patient_id, doctor_id, appointment_date, status, notes)
        VALUES (?, ?, ?, ?, ?)
    ''', appointments_data)
    
    # Fetch appointments that are completed for treatments & invoices
    cursor.execute("SELECT id, patient_id, appointment_date FROM appointments WHERE status = 'Completed'")
    completed_appointments = cursor.fetchall()
    
    # 4. Treatments (350)
    treatments_list = ["Consultation", "Follow-up", "Lab Test", "X-Ray", "Physical Therapy", "Vaccination", "Minor Surgery", "ECG", "Skin Biopsy"]
    treatments_data = []
    
    if len(completed_appointments) >= 350:
        selected_appts_for_treatments = random.sample(completed_appointments, 350)
    else:
        selected_appts_for_treatments = [random.choice(completed_appointments) for _ in range(350)]

    for appt in selected_appts_for_treatments:
        appt_id = appt[0]
        t_name = random.choice(treatments_list)
        cost = round(random.uniform(50.0, 5000.0), 2)
        duration = random.choice([15, 30, 45, 60, 90, 120])
        treatments_data.append((appt_id, t_name, cost, duration))
        
    cursor.executemany('''
        INSERT INTO treatments (appointment_id, treatment_name, cost, duration_minutes)
        VALUES (?, ?, ?, ?)
    ''', treatments_data)

    # 5. Invoices (300)
    invoice_statuses = ['Paid', 'Pending', 'Overdue']
    invoices_data = []
    
    if len(completed_appointments) >= 300:
        selected_appts_for_invoices = random.sample(completed_appointments, 300)
    else:
        selected_appts_for_invoices = [random.choice(completed_appointments) for _ in range(300)]
        
    for appt in selected_appts_for_invoices:
        patient_id = appt[1]
        appt_date_str = str(appt[2]).split("T")[0].split(" ")[0]
        
        status = random.choice(invoice_statuses)
        total_amount = round(random.uniform(50.0, 5000.0), 2)
        paid_amount = total_amount if status == 'Paid' else (round(random.uniform(0.0, total_amount * 0.5), 2) if status == 'Pending' else 0.0)
        
        invoices_data.append((
            patient_id,
            appt_date_str,
            total_amount,
            paid_amount,
            status
        ))
        
    cursor.executemany('''
        INSERT INTO invoices (patient_id, invoice_date, total_amount, paid_amount, status)
        VALUES (?, ?, ?, ?, ?)
    ''', invoices_data)
    
    conn.commit()
    conn.close()

    print(f"Created 200 patients, 15 doctors, 500 appointments, 350 treatments, and 300 invoices.")

if __name__ == "__main__":
    create_database()
