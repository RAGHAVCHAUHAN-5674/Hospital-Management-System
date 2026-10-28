import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

# ==================================================
#          RITIK HOSPITAL MANAGEMENT SYSTEM
# ==================================================

PATIENT_FILE = "patients.json"
DOCTOR_FILE = "doctors.json"
APPOINTMENT_FILE = "appointments.json"

BG_COLOR = "#F1F5F9"
NAVY = "#16324F"
BLUE = "#2563EB"
WHITE = "#FFFFFF"
GREEN = "#15803D"
RED = "#DC2626"


# ==================================================
#                 DATA MANAGEMENT
# ==================================================

def load_data(filename):
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)
                return data if isinstance(data, list) else []
        except (json.JSONDecodeError, OSError):
            return []
    return []


def save_data(filename, data):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        return True
    except OSError as error:
        messagebox.showerror("File Error", str(error))
        return False


patients = load_data(PATIENT_FILE)
doctors = load_data(DOCTOR_FILE)
appointments = load_data(APPOINTMENT_FILE)


# ==================================================
#                    MAIN APP
# ==================================================

class HospitalApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Ritik Hospital Management System")
        self.root.geometry("1100x700")
        self.root.minsize(900, 600)
        self.root.configure(bg=BG_COLOR)

        self.show_login()

    # ------------------------------------------------
    # Clear Screen
    # ------------------------------------------------

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # ------------------------------------------------
    # Login Screen
    # ------------------------------------------------

    def show_login(self):
        self.clear_screen()

        main_frame = tk.Frame(self.root, bg=BG_COLOR)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            main_frame,
            text="RITIK HOSPITAL",
            font=("Arial", 28, "bold"),
            fg=NAVY,
            bg=BG_COLOR
        ).pack(pady=(0, 5))

        tk.Label(
            main_frame,
            text="HOSPITAL MANAGEMENT SYSTEM",
            font=("Arial", 12),
            fg="#64748B",
            bg=BG_COLOR
        ).pack(pady=(0, 25))

        login_box = tk.Frame(
            main_frame,
            bg=WHITE,
            padx=35,
            pady=30,
            highlightbackground="#CBD5E1",
            highlightthickness=1
        )
        login_box.pack()

        tk.Label(
            login_box,
            text="Admin Login",
            font=("Arial", 21, "bold"),
            bg=WHITE,
            fg=NAVY
        ).pack(pady=(0, 20))

        tk.Label(
            login_box,
            text="Username",
            font=("Arial", 11),
            bg=WHITE
        ).pack(anchor="w")

        self.username_entry = ttk.Entry(
            login_box,
            width=32,
            font=("Arial", 12)
        )
        self.username_entry.pack(pady=(5, 15), ipady=5)

        tk.Label(
            login_box,
            text="Password",
            font=("Arial", 11),
            bg=WHITE
        ).pack(anchor="w")

        self.password_entry = ttk.Entry(
            login_box,
            width=32,
            show="*",
            font=("Arial", 12)
        )
        self.password_entry.pack(pady=(5, 20), ipady=5)

        tk.Button(
            login_box,
            text="LOGIN",
            command=self.login,
            bg=BLUE,
            fg=WHITE,
            font=("Arial", 12, "bold"),
            relief="flat",
            cursor="hand2",
            width=25,
            pady=10
        ).pack()

        tk.Label(
            login_box,
            text="Admin access only",
            font=("Arial", 9),
            fg="#64748B",
            bg=WHITE
        ).pack(pady=(15, 0))

        self.password_entry.bind(
            "<Return>",
            lambda event: self.login()
        )

        self.username_entry.focus_set()

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if username == "admin" and password == "ritik123":
            self.show_dashboard()
        else:
            messagebox.showerror(
                "Login Failed",
                "Incorrect username or password."
            )

    # ------------------------------------------------
    # Dashboard
    # ------------------------------------------------

    def show_dashboard(self):
        self.clear_screen()

        header = tk.Frame(self.root, bg=NAVY, height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="RITIK HOSPITAL",
            font=("Arial", 22, "bold"),
            bg=NAVY,
            fg=WHITE
        ).pack(side="left", padx=25, pady=20)

        tk.Button(
            header,
            text="Logout",
            command=self.show_login,
            bg=RED,
            fg=WHITE,
            font=("Arial", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=18,
            pady=8
        ).pack(side="right", padx=25)

        tk.Label(
            self.root,
            text="Management Dashboard",
            font=("Arial", 23, "bold"),
            bg=BG_COLOR,
            fg=NAVY
        ).pack(anchor="w", padx=30, pady=(25, 5))

        tk.Label(
            self.root,
            text="Manage hospital patients, doctors, appointments and billing.",
            font=("Arial", 11),
            bg=BG_COLOR,
            fg="#64748B"
        ).pack(anchor="w", padx=30, pady=(0, 20))

        # Statistics Cards
        cards_frame = tk.Frame(self.root, bg=BG_COLOR)
        cards_frame.pack(fill="x", padx=20)

        self.create_card(
            cards_frame, "TOTAL PATIENTS",
            len(patients), 0
        )

        self.create_card(
            cards_frame, "TOTAL DOCTORS",
            len(doctors), 1
        )

        self.create_card(
            cards_frame, "APPOINTMENTS",
            len(appointments), 2
        )

        # Dashboard Buttons
        menu_frame = tk.Frame(self.root, bg=BG_COLOR)
        menu_frame.pack(fill="both", expand=True, padx=25, pady=25)

        buttons = [
            ("Register Patient", self.add_patient),
            ("View / Search Patients", self.view_patients),
            ("Register Doctor", self.add_doctor),
            ("View Doctors", self.view_doctors),
            ("Book Appointment", self.book_appointment),
            ("View Appointments", self.view_appointments),
            ("Generate Bill", self.generate_bill),
        ]

        for index, (label, command) in enumerate(buttons):
            button = tk.Button(
                menu_frame,
                text=label,
                command=command,
                font=("Arial", 12, "bold"),
                bg=WHITE,
                fg=NAVY,
                activebackground=BLUE,
                activeforeground=WHITE,
                relief="flat",
                cursor="hand2",
                padx=10,
                pady=20
            )

            button.grid(
                row=index // 3,
                column=index % 3,
                sticky="nsew",
                padx=10,
                pady=10
            )

        for column in range(3):
            menu_frame.grid_columnconfigure(column, weight=1)

        for row in range(3):
            menu_frame.grid_rowconfigure(row, weight=1)

    def create_card(self, parent, title, value, column):
        card = tk.Frame(
            parent,
            bg=WHITE,
            padx=25,
            pady=15
        )

        card.grid(
            row=0,
            column=column,
            sticky="nsew",
            padx=10
        )

        tk.Label(
            card,
            text=title,
            font=("Arial", 10, "bold"),
            bg=WHITE,
            fg="#64748B"
        ).pack()

        tk.Label(
            card,
            text=str(value),
            font=("Arial", 25, "bold"),
            bg=WHITE,
            fg=BLUE
        ).pack(pady=5)

        parent.grid_columnconfigure(column, weight=1)

    # ------------------------------------------------
    # Common Form Window
    # ------------------------------------------------

    def form_window(self, title, fields, callback):
        window = tk.Toplevel(self.root)
        window.title(title)
        window.geometry("450x570")
        window.configure(bg=WHITE)
        window.transient(self.root)
        window.grab_set()

        tk.Label(
            window,
            text=title,
            font=("Arial", 20, "bold"),
            bg=WHITE,
            fg=NAVY
        ).pack(pady=20)

        form_frame = tk.Frame(window, bg=WHITE)
        form_frame.pack(fill="both", expand=True, padx=35)

        entries = {}

        for field in fields:
            tk.Label(
                form_frame,
                text=field,
                font=("Arial", 11),
                bg=WHITE
            ).pack(anchor="w", pady=(5, 0))

            entry = ttk.Entry(
                form_frame,
                font=("Arial", 11)
            )

            entry.pack(fill="x", ipady=5, pady=(3, 8))
            entries[field] = entry

        def submit():
            values = {
                field: entry.get().strip()
                for field, entry in entries.items()
            }

            if not all(values.values()):
                messagebox.showwarning(
                    "Missing Information",
                    "Please fill in all fields.",
                    parent=window
                )
                return

            callback(values, window)

        tk.Button(
            window,
            text="SAVE RECORD",
            command=submit,
            bg=BLUE,
            fg=WHITE,
            font=("Arial", 11, "bold"),
            relief="flat",
            cursor="hand2",
            pady=10
        ).pack(fill="x", padx=35, pady=20)

    # ------------------------------------------------
    # Register Patient
    # ------------------------------------------------

    def add_patient(self):

        def save(values, window):
            patient_id = values["Patient ID"]

            if any(p["id"] == patient_id for p in patients):
                messagebox.showerror(
                    "Duplicate ID",
                    "This Patient ID already exists.",
                    parent=window
                )
                return

            try:
                age = int(values["Age"])

                if age < 1 or age > 120:
                    raise ValueError

            except ValueError:
                messagebox.showerror(
                    "Invalid Age",
                    "Enter an age between 1 and 120.",
                    parent=window
                )
                return

            patient = {
                "id": patient_id,
                "name": values["Patient Name"],
                "age": age,
                "gender": values["Gender"],
                "disease": values["Disease"],
                "phone": values["Phone"]
            }

            patients.append(patient)

            if not save_data(PATIENT_FILE, patients):
                patients.pop()
                return

            messagebox.showinfo(
                "Success",
                "Patient registered successfully!",
                parent=window
            )

            window.destroy()
            self.show_dashboard()

        self.form_window(
            "Register New Patient",
            [
                "Patient ID",
                "Patient Name",
                "Age",
                "Gender",
                "Disease",
                "Phone"
            ],
            save
        )

    # ------------------------------------------------
    # View and Search Patients
    # ------------------------------------------------

    def view_patients(self):
        window = tk.Toplevel(self.root)
        window.title("Patient Management")
        window.geometry("900x500")

        tk.Label(
            window,
            text="Patient Records",
            font=("Arial", 20, "bold"),
            fg=NAVY
        ).pack(pady=15)

        search_frame = tk.Frame(window)
        search_frame.pack(fill="x", padx=15, pady=5)

        tk.Label(
            search_frame,
            text="Search by ID or Name:"
        ).pack(side="left", padx=5)

        search_entry = ttk.Entry(search_frame)
        search_entry.pack(side="left", fill="x", expand=True)

        columns = (
            "id", "name", "age",
            "gender", "disease", "phone"
        )

        table = ttk.Treeview(
            window,
            columns=columns,
            show="headings"
        )

        headings = {
            "id": "Patient ID",
            "name": "Patient Name",
            "age": "Age",
            "gender": "Gender",
            "disease": "Disease",
            "phone": "Phone"
        }

        for column in columns:
            table.heading(column, text=headings[column])
            table.column(column, width=130)

        table.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        def refresh(event=None):
            for item in table.get_children():
                table.delete(item)

            query = search_entry.get().strip().lower()

            for patient in patients:
                searchable = (
                    str(patient["id"]) + " " +
                    str(patient["name"])
                ).lower()

                if query in searchable:
                    table.insert(
                        "",
                        "end",
                        values=(
                            patient["id"],
                            patient["name"],
                            patient["age"],
                            patient["gender"],
                            patient["disease"],
                            patient["phone"]
                        )
                    )

        search_entry.bind("<KeyRelease>", refresh)
        refresh()

    # ------------------------------------------------
    # Register Doctor
    # ------------------------------------------------

    def add_doctor(self):

        def save(values, window):
            doctor_id = values["Doctor ID"]

            if any(d["id"] == doctor_id for d in doctors):
                messagebox.showerror(
                    "Duplicate ID",
                    "This Doctor ID already exists.",
                    parent=window
                )
                return

            doctor = {
                "id": doctor_id,
                "name": values["Doctor Name"],
                "specialization": values["Specialization"],
                "phone": values["Phone"]
            }

            doctors.append(doctor)

            if not save_data(DOCTOR_FILE, doctors):
                doctors.pop()
                return

            messagebox.showinfo(
                "Success",
                "Doctor registered successfully!",
                parent=window
            )

            window.destroy()
            self.show_dashboard()

        self.form_window(
            "Register New Doctor",
            [
                "Doctor ID",
                "Doctor Name",
                "Specialization",
                "Phone"
            ],
            save
        )

    # ------------------------------------------------
    # View Doctors
    # ------------------------------------------------

    def view_doctors(self):
        window = tk.Toplevel(self.root)
        window.title("Doctor Directory")
        window.geometry("750x400")

        tk.Label(
            window,
            text="Doctor Directory",
            font=("Arial", 20, "bold"),
            fg=NAVY
        ).pack(pady=15)

        columns = (
            "id", "name", "specialization", "phone"
        )

        table = ttk.Treeview(
            window,
            columns=columns,
            show="headings"
        )

        headings = {
            "id": "Doctor ID",
            "name": "Doctor Name",
            "specialization": "Specialization",
            "phone": "Phone"
        }

        for column in columns:
            table.heading(column, text=headings[column])
            table.column(column, width=170)

        for doctor in doctors:
            table.insert(
                "",
                "end",
                values=(
                    doctor["id"],
                    doctor["name"],
                    doctor["specialization"],
                    doctor["phone"]
                )
            )

        table.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

    # ------------------------------------------------
    # Book Appointment
    # ------------------------------------------------

    def book_appointment(self):

        def save(values, window):
            patient = next(
                (
                    p for p in patients
                    if p["id"] == values["Patient ID"]
                ),
                None
            )

            doctor = next(
                (
                    d for d in doctors
                    if d["id"] == values["Doctor ID"]
                ),
                None
            )

            if patient is None:
                messagebox.showerror(
                    "Patient Not Found",
                    "Register the patient first.",
                    parent=window
                )
                return

            if doctor is None:
                messagebox.showerror(
                    "Doctor Not Found",
                    "Register the doctor first.",
                    parent=window
                )
                return

            appointment_date = values["Date"]

            try:
                datetime.strptime(
                    appointment_date,
                    "%d-%m-%Y"
                )
            except ValueError:
                messagebox.showerror(
                    "Invalid Date",
                    "Enter date in DD-MM-YYYY format.",
                    parent=window
                )
                return

            appointment = {
                "patient_id": patient["id"],
                "patient_name": patient["name"],
                "doctor_id": doctor["id"],
                "doctor_name": doctor["name"],
                "date": appointment_date,
                "time": values["Time"]
            }

            appointments.append(appointment)

            if not save_data(
                APPOINTMENT_FILE,
                appointments
            ):
                appointments.pop()
                return

            messagebox.showinfo(
                "Success",
                "Appointment booked successfully!",
                parent=window
            )

            window.destroy()
            self.show_dashboard()

        self.form_window(
            "Book Appointment",
            [
                "Patient ID",
                "Doctor ID",
                "Date",
                "Time"
            ],
            save
        )

    # ------------------------------------------------
    # View Appointments
    # ------------------------------------------------

    def view_appointments(self):
        window = tk.Toplevel(self.root)
        window.title("Appointment Schedule")
        window.geometry("850x420")

        tk.Label(
            window,
            text="Appointment Schedule",
            font=("Arial", 20, "bold"),
            fg=NAVY
        ).pack(pady=15)

        columns = (
            "patient_id",
            "patient_name",
            "doctor_name",
            "date",
            "time"
        )

        table = ttk.Treeview(
            window,
            columns=columns,
            show="headings"
        )

        headings = {
            "patient_id": "Patient ID",
            "patient_name": "Patient Name",
            "doctor_name": "Doctor Name",
            "date": "Date",
            "time": "Time"
        }

        for column in columns:
            table.heading(column, text=headings[column])
            table.column(column, width=155)

        for appointment in appointments:
            table.insert(
                "",
                "end",
                values=(
                    appointment["patient_id"],
                    appointment["patient_name"],
                    appointment["doctor_name"],
                    appointment["date"],
                    appointment["time"]
                )
            )

        table.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

    # ------------------------------------------------
    # Generate Bill
    # ------------------------------------------------

    def generate_bill(self):
        window = tk.Toplevel(self.root)
        window.title("Hospital Billing")
        window.geometry("450x470")
        window.configure(bg=WHITE)
        window.transient(self.root)
        window.grab_set()

        tk.Label(
            window,
            text="HOSPITAL BILLING",
            font=("Arial", 21, "bold"),
            fg=NAVY,
            bg=WHITE
        ).pack(pady=20)

        form = tk.Frame(window, bg=WHITE)
        form.pack(fill="x", padx=30)

        tk.Label(
            form,
            text="Patient ID",
            bg=WHITE
        ).pack(anchor="w")

        patient_id_entry = ttk.Entry(form)
        patient_id_entry.pack(
            fill="x",
            ipady=5,
            pady=(5, 15)
        )

        tk.Label(
            form,
            text="Consultation Fee (Rs.)",
            bg=WHITE
        ).pack(anchor="w")

        consultation_entry = ttk.Entry(form)
        consultation_entry.pack(
            fill="x",
            ipady=5,
            pady=(5, 15)
        )

        tk.Label(
            form,
            text="Medicine Fee (Rs.)",
            bg=WHITE
        ).pack(anchor="w")

        medicine_entry = ttk.Entry(form)
        medicine_entry.pack(
            fill="x",
            ipady=5,
            pady=(5, 15)
        )

        def create_bill():
            patient_id = patient_id_entry.get().strip()

            patient = next(
                (
                    p for p in patients
                    if p["id"] == patient_id
                ),
                None
            )

            if patient is None:
                messagebox.showerror(
                    "Error",
                    "Patient not found.",
                    parent=window
                )
                return

            try:
                consultation = float(
                    consultation_entry.get()
                )

                medicine = float(
                    medicine_entry.get()
                )

                if (
                    consultation < 0
                    or medicine < 0
                ):
                    raise ValueError

            except ValueError:
                messagebox.showerror(
                    "Invalid Amount",
                    "Enter valid non-negative fees.",
                    parent=window
                )
                return

            total = consultation + medicine

            receipt = (
                "================================\n"
                "         RITIK HOSPITAL\n"
                "           BILL RECEIPT\n"
                "================================\n"
                f"Date: {datetime.now():%d-%m-%Y %H:%M}\n"
                f"Patient ID: {patient['id']}\n"
                f"Patient Name: {patient['name']}\n"
                "--------------------------------\n"
                f"Consultation Fee: Rs. {consultation:.2f}\n"
                f"Medicine Fee: Rs. {medicine:.2f}\n"
                "--------------------------------\n"
                f"TOTAL: Rs. {total:.2f}\n"
                "================================\n"
                "     THANK YOU FOR VISITING\n"
            )

            bill_window = tk.Toplevel(window)
            bill_window.title("Bill Receipt")
            bill_window.geometry("450x400")

            bill_text = tk.Text(
                bill_window,
                font=("Courier New", 11),
                wrap="word",
                padx=15,
                pady=15
            )

            bill_text.pack(
                fill="both",
                expand=True,
                padx=10,
                pady=10
            )

            bill_text.insert("1.0", receipt)
            bill_text.config(state="disabled")

            def save_bill():
                filename = (
                    f"bill_{patient['id']}_"
                    f"{datetime.now():%Y%m%d_%H%M%S}.txt"
                )

                try:
                    with open(
                        filename, "w", encoding="utf-8"
                    ) as file:
                        file.write(receipt)

                    messagebox.showinfo(
                        "Saved",
                        f"Bill saved as:\n{filename}",
                        parent=bill_window
                    )
                except OSError as error:
                    messagebox.showerror(
                        "Error",
                        str(error),
                        parent=bill_window
                    )
            tk.Button(
                bill_window,
                text="Save Bill as TXT",
                command=save_bill,
                bg=GREEN,
                fg=WHITE,
                font=("Arial", 11, "bold"),
                relief="flat",
                pady=8
            ).pack(fill="x", padx=10, pady=(0, 10))
        tk.Button(
            window,
            text="GENERATE BILL",
            command=create_bill,
            bg=BLUE,
            fg=WHITE,
            font=("Arial", 11, "bold"),
            relief="flat",
            pady=10
        ).pack(fill="x", padx=30, pady=15)
# ==================================================
#                   START APPLICATION
# ==================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = HospitalApp(root)
    root.mainloop()