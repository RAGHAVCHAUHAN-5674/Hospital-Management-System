import json
import os
from datetime import datetime
# ==========================================
#       RAGHAV CARE HOSPITAL MANAGEMENT
# ==========================================
PATIENT_FILE = "patients.json"
DOCTOR_FILE = "doctors.json"
APPOINTMENT_FILE = "appointments.json"
def load_data(filename):
    if os.path.exists(filename):
        try:
            with open(filename, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            return []
    return []
def save_data(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)
patients = load_data(PATIENT_FILE)
doctors = load_data(DOCTOR_FILE)
appointments = load_data(APPOINTMENT_FILE)
def heading(title):
    print("\n" + "=" * 50)
    print("Raghav CARE HOSPITAL")
    print("=" * 50)
    print(f"{title}")
    print("-" * 50)
def add_patient():
    heading("PATIENT REGISTRATION")
    patient_id = input("Enter Patient ID: ").strip()
    if not patient_id:
        print("Patient ID cannot be empty.")
        return
    if any(p["id"] == patient_id for p in patients):
        print("This Patient ID already exists.")
        return
    name = input("Enter Patient Name: ").strip()
    age = input("Enter Age: ").strip()
    gender = input("Enter Gender: ").strip()
    disease = input("Enter Disease: ").strip()
    phone = input("Enter Phone Number: ").strip()
    if not all([name, age, gender, disease, phone]):
        print("All fields are required.")
        return
    try:
        age = int(age)
        if age <= 0 or age > 120:
            print("Please enter a valid age.")
            return
    except ValueError:
        print("Age must be a number.")
        return
    patient = {
        "id": patient_id,
        "name": name,
        "age": age,
        "gender": gender,
        "disease": disease,
        "phone": phone
    }
    patients.append(patient)
    save_data(PATIENT_FILE, patients)
    print("\nPatient registered successfully!")
def view_patients():
    heading("PATIENT RECORDS")
    if not patients:
        print("No patient records found.")
        return
    for patient in patients:
        print("\nPatient ID :", patient["id"])
        print("Name       :", patient["name"])
        print("Age        :", patient["age"])
        print("Gender     :", patient["gender"])
        print("Disease    :", patient["disease"])
        print("Phone      :", patient["phone"])
        print("-" * 50)
def search_patient():
    heading("SEARCH PATIENT")
    patient_id = input("Enter Patient ID: ").strip()
    for patient in patients:
        if patient["id"] == patient_id:
            print("\nPatient Found!")
            print("-" * 50)
            for key, value in patient.items():
                print(f"{key.title():12}: {value}")
            return
    print("Patient not found.")
def add_doctor():
    heading("DOCTOR REGISTRATION")
    doctor_id = input("Enter Doctor ID: ").strip()
    if not doctor_id:
        print("Doctor ID cannot be empty.")
        return
    if any(d["id"] == doctor_id for d in doctors):
        print("This Doctor ID already exists.")
        return
    name = input("Enter Doctor Name: ").strip()
    specialization = input("Enter Specialization: ").strip()
    phone = input("Enter Phone Number: ").strip()
    if not all([name, specialization, phone]):
        print("All fields are required.")
        return
    doctor = {
        "id": doctor_id,
        "name": name,
        "specialization": specialization,
        "phone": phone
    }
    doctors.append(doctor)
    save_data(DOCTOR_FILE, doctors)
    print("\nDoctor registered successfully!")
def view_doctors():
    heading("DOCTOR DIRECTORY")
    if not doctors:
        print("No doctor records found.")
        return
    for doctor in doctors:
        print("\nDoctor ID      :", doctor["id"])
        print("Name           :", doctor["name"])
        print("Specialization :", doctor["specialization"])
        print("Phone          :", doctor["phone"])
        print("-" * 50)
def book_appointment():
    heading("BOOK APPOINTMENT")
    patient_id = input("Enter Patient ID: ").strip()
    doctor_id = input("Enter Doctor ID: ").strip()
    patient = next(
        (p for p in patients if p["id"] == patient_id), None
    )
    doctor = next(
        (d for d in doctors if d["id"] == doctor_id), None
    )
    if patient is None:
        print("Patient ID not found. Register the patient first.")
        return
    if doctor is None:
        print("Doctor ID not found. Register the doctor first.")
        return
    date = input("Enter Appointment Date (DD-MM-YYYY): ").strip()
    time = input("Enter Appointment Time (e.g. 11:00 AM): ").strip()
    try:
        datetime.strptime(date, "%d-%m-%Y")
    except ValueError:
        print("Invalid date. Use DD-MM-YYYY format.")
        return
    if not time:
        print("Appointment time cannot be empty.")
        return
    appointment = {
        "patient_id": patient_id,
        "patient_name": patient["name"],
        "doctor_id": doctor_id,
        "doctor_name": doctor["name"],
        "date": date,
        "time": time
    }
    appointments.append(appointment)
    save_data(APPOINTMENT_FILE, appointments)
    print("\nAppointment booked successfully!")
    print("Patient:", patient["name"])
    print("Doctor :", doctor["name"])
    print("Date   :", date)
    print("Time   :", time)
def view_appointments():
    heading("APPOINTMENT SCHEDULE")
    if not appointments:
        print("No appointments found.")
        return
    for appointment in appointments:
        print("\nPatient    :", appointment["patient_name"])
        print("Patient ID :", appointment["patient_id"])
        print("Doctor     :", appointment["doctor_name"])
        print("Doctor ID  :", appointment["doctor_id"])
        print("Date       :", appointment["date"])
        print("Time       :", appointment["time"])
        print("-" * 50)
def generate_bill():
    heading("HOSPITAL BILLING")
    patient_id = input("Enter Patient ID: ").strip()
    patient = next(
        (p for p in patients if p["id"] == patient_id), None
    )
    if patient is None:
        print("Patient not found. Please register first.")
        return
    try:
        consultation_fee = float(
            input("Enter Consultation Fee (Rs.): ")
        )
        medicine_fee = float(
            input("Enter Medicine Fee (Rs.): ")
        )
        if consultation_fee < 0 or medicine_fee < 0:
            print("Fees cannot be negative.")
            return
    except ValueError:
        print("Please enter valid numeric fees.")
        return
    total = consultation_fee + medicine_fee
    print("\n" + "=" * 50)
    print("Raghav CARE HOSPITAL")
    print("BILL RECEIPT")
    print("=" * 50)
    print("Patient ID:", patient["id"])
    print("Patient Name:", patient["name"])
    print("-" * 50)
    print(f"Consultation Fee : Rs. {consultation_fee:.2f}")
    print(f"Medicine Fee: Rs. {medicine_fee:.2f}")
    print("-" * 50)
    print(f"TOTAL AMOUNT:Rs. {total:.2f}")
    print("=" * 50)
    print("THANK YOU FOR VISITING!")
    print("=" * 50)
def admin_login():
    print("\nRAGHAV CARE HOSPITAL")
    print("ADMIN LOGIN")
    username = input("Enter Username: ")
    password = input("Enter Password: ")
    if username == "admin" and password == "ritik123":
        print("Login Successful!")
        return True
    else:
        print("Invalid Username or Password!")
        return False
def main():
    while True:
        print("\n")
        print("*" * 50)
        print("Raghav CARE HOSPITAL")
        print("MANAGEMENT SYSTEM")
        print("*" * 50)
        print("1. Register New Patient")
        print("2. View All Patients")
        print("3. Search Patient")
        print("4. Register New Doctor")
        print("5. View All Doctors")
        print("6. Book Appointment")
        print("7. View Appointments")
        print("8. Generate Hospital Bill")
        print("9. Exit")
        choice = input("\nEnter your choice (1-9): ").strip()
        if choice == "1":
            add_patient()
        elif choice == "2":
            view_patients()
        elif choice == "3":
            search_patient()
        elif choice == "4":
            add_doctor()
        elif choice == "5":
            view_doctors()
        elif choice == "6":
            book_appointment()
        elif choice == "7":
            view_appointments()
        elif choice == "8":
            generate_bill()
        elif choice == "9":
            print("\nThank you for using Raghav CARE HOSPITAL!")
            print("Have a nice day!")
            break
        else:
            print("Invalid choice! Enter a number from 1 to 9.")
if __name__ == "__main__":
    if admin_login():
        main()
    else:
        print("Access Denied!")