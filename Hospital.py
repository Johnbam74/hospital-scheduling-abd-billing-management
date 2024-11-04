import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import mysql.connector
import pygame

# Function to connect to MySQL and create database and tables if not exist
def setup_database():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password=""
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS hospital_db")
    cursor.execute("USE hospital_db")
    
    # Create necessary tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL UNIQUE,
            password VARCHAR(50) NOT NULL,
            email VARCHAR(100) NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            age INT NOT NULL,
            email VARCHAR(100) NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INT AUTO_INCREMENT PRIMARY KEY,
            patient_id INT NOT NULL,
            appointment_date DATE NOT NULL,
            FOREIGN KEY (patient_id) REFERENCES patients(id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bills (
            id INT AUTO_INCREMENT PRIMARY KEY,
            patient_id INT NOT NULL,
            amount DECIMAL(10, 2) NOT NULL,
            FOREIGN KEY (patient_id) REFERENCES patients(id)
        )
    """)
    cursor.close()
    conn.close()

class HospitalApp:
    def __init__(self, root):
        setup_database()
        self.root = root
        self.root.title("Hospital Management System")
        self.root.geometry("800x600")
        self.root.resizable(0,0)

        pygame.mixer.init()
        pygame.mixer.music.load("Hospitalaudio.mp3")  # Add your music file
        pygame.mixer.music.play(-1)  # Play music indefinitely

        pygame.mixer.init()
        button_click_sound = pygame.mixer.Sound("buttonclick2.ogg")  # Add your sound file

        # Play sound when button is clicked
        def show_add_patient_page(self):
            button_click_sound.play()  # Play sound effect
            self.clear_screen()
            ...

    


        
        # Load the welcome page
        self.show_welcome_page()

    # Clears all widgets from the screen
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # Function to add floating text
    def create_floating_text(self, text, font=("Arial", 8), fg="black"):
        floating_text = tk.Label(self.root, text=text, font=font, bg="#d0e7f9", fg=fg)  
        floating_text.place(x=10, y=10)
        self.animate_label(floating_text)
        
        
    

    def animate_label(self, label):
        x = 0
        def move():
            nonlocal x
            if x < self.root.winfo_width():
                label.place(x=x, y=50)
                x += 2
                self.root.after(50, move)
            else:
                label.place(x=0, y=50)
                x = 0
                self.root.after(50, move)
        move()

    # Welcome Page
    def show_welcome_page(self):
        self.clear_screen()
        self.set_background_image("Hospital.jpg")  
        tk.Label(self.root, text="Embracing Wellness Together", font=("Arial", 24, "bold"), bg="#d0e7f9").pack(pady=10)
        tk.Button(self.root, text="Click here to Login", command=self.show_login_page).pack(pady=10)
        tk.Button(self.root, text="Not registered? Click here to Sign Up", command=self.show_signup_page).pack(pady=10)

       
        self.create_floating_text("............Committed to Your Health and Wellbeing", font=("Arial", 8), fg="darkblue")

    # Set background image for the current page
    def set_background_image(self, image_path):
        self.background_image = ImageTk.PhotoImage(Image.open(image_path).resize((800, 600), Image.LANCZOS))
        bg_label = tk.Label(self.root, image=self.background_image)
        bg_label.place(x=0, y=0)

    # Login Page
    def show_login_page(self):
        self.clear_screen()
        self.set_background_image("Hospitallogin.jpg")  
        # tk.Label(self.root, text="Login", font=("Arial", 24, "bold"), bg="white").pack(pady=20)

        frame_login = tk.Frame(self.root)
        frame_login.pack(pady=50)
        tk.Label(frame_login, text="Username:", bg="white").grid(row=0, column=0, pady=5)
        self.username_entry = tk.Entry(frame_login)
        self.username_entry.grid(row=0, column=1, pady=5)
        tk.Label(frame_login, text="Password:", bg="white").grid(row=1, column=0, pady=5)
        self.password_entry = tk.Entry(frame_login, show="*")
        self.password_entry.grid(row=1, column=1, pady=5)
        tk.Button(frame_login, text="Login", command=self.verify_login).grid(row=2, columnspan=2, pady=10)
        tk.Button(frame_login, text="Back to Home", command=self.show_welcome_page).grid(row=3, columnspan=2, pady=5)
        # self.create_floating_text("Quality Care, Quality Life.....")
    def verify_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        conn = mysql.connector.connect(host="localhost", user="root", password="", database="hospital_db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        if cursor.fetchone():
            self.show_main_menu()
        else:
            messagebox.showerror("Error", "Invalid username or password")
        cursor.close()
        conn.close()

    def show_signup_page(self):
        self.clear_screen()
        self.set_background_image("Hospitalsignup.jpg")  
        # tk.Label(self.root, text="Sign Up", font=("Arial", 24, "bold"), bg="white").pack(pady=20)

        frame_signup = tk.Frame(self.root)
        frame_signup.pack(pady=50)
        tk.Label(frame_signup, text="Username:", bg="white").grid(row=0, column=0, pady=5)
        self.signup_username_entry = tk.Entry(frame_signup)
        self.signup_username_entry.grid(row=0, column=1, pady=5)
        tk.Label(frame_signup, text="Password:", bg="white").grid(row=1, column=0, pady=5)
        self.signup_password_entry = tk.Entry(frame_signup, show="*")
        self.signup_password_entry.grid(row=1, column=1, pady=5)
        tk.Label(frame_signup, text="Email:", bg="white").grid(row=2, column=0, pady=5)
        self.signup_email_entry = tk.Entry(frame_signup)
        self.signup_email_entry.grid(row=2, column=1, pady=5)
        tk.Button(frame_signup, text="Sign Up", command=self.register_user).grid(row=3, columnspan=2, pady=10)
        tk.Button(frame_signup, text="Back to Home", command=self.show_welcome_page).grid(row=4, columnspan=2, pady=5)

    def register_user(self):
        username = self.signup_username_entry.get()
        password = self.signup_password_entry.get()
        email = self.signup_email_entry.get()
        if username and password and email:
            conn = mysql.connector.connect(host="localhost", user="root", password="", database="hospital_db")
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)", (username, password, email))
                conn.commit()
                messagebox.showinfo("Success", "Registration successful!")
                self.show_login_page()
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error: {err}")
            finally:
                cursor.close()
                conn.close()
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    def show_main_menu(self):
        self.clear_screen()
        self.set_background_image("Hospitalmainmenu.jpg")  
        # tk.Label(self.root, text="Main Menu", font=("Arial", 24, "bold"), bg="white").pack(pady=20)
        tk.Button(self.root, text="Add Patient", command=self.show_add_patient_page, width=20, height=2).pack(pady=10)
        tk.Button(self.root, text="Schedule Appointment", command=self.show_schedule_appointment_page, width=20, height=2).pack(pady=10)
        tk.Button(self.root, text="Generate Bill", command=self.show_generate_bill_page, width=20, height=2).pack(pady=10)
        self.create_floating_text("Quality Care, Quality Life.....")

    # Add Patient Page
    def show_add_patient_page(self):
        self.clear_screen()
        self.set_background_image("Hospitaladdpatient.jpg")  
        tk.Label(self.root, text="Add New Patient", font=("Arial", 18, "bold"), bg="white").pack(pady=20)
        tk.Label(self.root, text="Name", bg="white").pack()
        self.patient_name_entry = tk.Entry(self.root)
        self.patient_name_entry.pack()
        tk.Label(self.root, text="Age", bg="white").pack()
        self.patient_age_entry = tk.Entry(self.root)
        self.patient_age_entry.pack()
        tk.Label(self.root, text="Email", bg="white").pack()
        self.patient_email_entry = tk.Entry(self.root)
        self.patient_email_entry.pack()
        tk.Button(self.root, text="Add Patient", command=self.add_patient).pack(pady=10)
        tk.Button(self.root, text="Back to Main Menu", command=self.show_main_menu).pack()

    def add_patient(self):
        name = self.patient_name_entry.get()
        age = self.patient_age_entry.get()
        email = self.patient_email_entry.get()

        if name and age and email:
            conn = mysql.connector.connect(host="localhost", user="root", password="", database="hospital_db")
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO patients (name, age, email) VALUES (%s, %s, %s)", (name, age, email))
                conn.commit()
                patient_id = cursor.lastrowid  # Get the last inserted ID
                messagebox.showinfo("Success", f"Patient added successfully! Patient ID: {patient_id}")
                self.show_main_menu()
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error: {err}")
            finally:
                cursor.close()
                conn.close()
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    # Schedule Appointment Page
    def show_schedule_appointment_page(self):
        self.clear_screen()
        self.set_background_image("Hospitalschdule.jpg")  
        tk.Label(self.root, text="Schedule Appointment", font=("Arial", 18, "bold"), bg="white").pack(pady=20)
        tk.Label(self.root, text="Patient ID", bg="white").pack()
        self.appointment_patient_id_entry = tk.Entry(self.root)
        self.appointment_patient_id_entry.pack()
        tk.Label(self.root, text="Appointment Date (YYYY-MM-DD)", bg="white").pack()
        self.appointment_date_entry = tk.Entry(self.root)
        self.appointment_date_entry.pack()
        tk.Button(self.root, text="Schedule", command=self.schedule_appointment).pack(pady=10)
        tk.Button(self.root, text="Back to Main Menu", command=self.show_main_menu).pack()

    def schedule_appointment(self):
        patient_id = self.appointment_patient_id_entry.get()
        appointment_date = self.appointment_date_entry.get()

        if patient_id and appointment_date:
            conn = mysql.connector.connect(host="localhost", user="root", password="", database="hospital_db")
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO appointments (patient_id, appointment_date) VALUES (%s, %s)", (patient_id, appointment_date))
                conn.commit()
                messagebox.showinfo("Success", "Appointment scheduled successfully!")
                self.show_main_menu()
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error: {err}")
            finally:
                cursor.close()
                conn.close()
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    # Generate Bill Page
    def show_generate_bill_page(self):
        self.clear_screen()
        self.set_background_image("Hospitalgeneratebill.jpg")  
        tk.Label(self.root, text="Generate Bill", font=("Arial", 18, "bold"), bg="white").pack(pady=20)
        tk.Label(self.root, text="Patient ID", bg="white").pack()
        self.bill_patient_id_entry = tk.Entry(self.root)
        self.bill_patient_id_entry.pack()
        tk.Label(self.root, text="Bill Amount", bg="white").pack()
        self.bill_amount_entry = tk.Entry(self.root)
        self.bill_amount_entry.pack()
        tk.Button(self.root, text="Generate Bill", command=self.generate_bill).pack(pady=10)
        tk.Button(self.root, text="Back to Main Menu", command=self.show_main_menu).pack()

    def generate_bill(self):
        patient_id = self.bill_patient_id_entry.get()
        amount = self.bill_amount_entry.get()

        if patient_id and amount:
            conn = mysql.connector.connect(host="localhost", user="root", password="", database="hospital_db")
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO bills (patient_id, amount) VALUES (%s, %s)", (patient_id, amount))
                conn.commit()
                messagebox.showinfo("Success", "Bill generated successfully!")
                self.show_main_menu()
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error: {err}")
            finally:
                cursor.close()
                conn.close()
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

if __name__ == "__main__":
    root = tk.Tk()
    app = HospitalApp(root)
    root.mainloop()