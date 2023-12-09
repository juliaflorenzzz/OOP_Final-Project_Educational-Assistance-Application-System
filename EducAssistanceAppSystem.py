import tkinter as tk
from tkinter import filedialog
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
from PIL import Image, ImageTk
import pymysql
from ttkthemes import ThemedStyle

# Function to connect to the database
def connection():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='educass_db',
    )
    return conn


class LoginPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Login Page")
        self.root.geometry("1920x1080")
        self.setup_login_page()

    def setup_login_page(self): 
        # Set background color for the entire window
        self.root.configure(bg="white")  # Adjust the color as needed

        # Create a frame to hold the login widgets
        login_frame = tk.Frame(root, bd=5, relief="sunken", padx=100, pady=100, highlightthickness=5, highlightbackground="maroon")  # Add border and padding
        login_frame.grid(row=0, column=0)

        # Logo or picture (replace 'path_to_logo.png' with the actual path to your image file)
        original_logo = Image.open('logo.png')
        resized_logo = original_logo.resize((220, 200))  # Adjust the size as needed
        tk_logo = ImageTk.PhotoImage(resized_logo)
        self.logo_label = tk.Label(login_frame, image=tk_logo)
        self.logo_label.image = tk_logo  # Keep a reference to the image
        self.logo_label.grid(row=0, column=0, columnspan=2, pady=(0, 0))  # Adjusted height

        # Title label
        title_label = tk.Label(login_frame, text="ADMIN", font=("Arial", 16, "bold"))
        title_label.grid(row=1, column=0, columnspan=2, pady=(10, 10))  # Adjusted height

        # Labels for username and password
        username_label = tk.Label(login_frame, text="Username:", font =("Arial", 12, "bold"))
        password_label = tk.Label(login_frame, text="Password:", font =("Arial", 12, "bold"))

        self.username_entry = tk.Entry(login_frame, width=40)
        self.password_entry = tk.Entry(login_frame, width=40, show='●')
        self.login_button = tk.Button(login_frame, text="Login", font=("Arial", 12), command=self.validate_login, bg="maroon", fg="white")

        # Place the widgets on the frame using grid
        username_label.grid(row=2, column=0, padx=10, pady=(0, 5), sticky="w")  # Adjusted height
        self.username_entry.grid(row=2, column=1, padx=10, pady=(0, 5), sticky="ew")

        password_label.grid(row=3, column=0, padx=10, pady=(0, 5), sticky="w")  # Adjusted height
        self.password_entry.grid(row=3, column=1, padx=10, pady=(0, 5), sticky="ew")

        self.login_button.grid(row=4, column=1, padx=10, pady=(10, 0), sticky="ew")  # Adjusted height

        login_frame.place(relx=0.28, rely=0.05)

    def validate_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Check if the username and password are correct
        if username == "bsuadmin" and password == "bsutneu120":
            messagebox.showinfo("Login Successful", "Welcome, Admin!")
            self.root.destroy()  # Close the login window

            # Initialize the app_instance after a successful login
            self.app_instance = HomePage(tk.Tk())
            print("App instance created")  # Add this print statement
            self.app_instance.run()
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password")


class HomePage:
    def __init__(self, root):
        self.root = root
        self.root.title("Educational Assistance Application System")
        self.root.geometry("1920x1080")
        
        # Establish a database connection and create a cursor
        self.db_connection = connection()
        self.db_cursor = self.db_connection.cursor(pymysql.cursors.DictCursor)
        
        self.style = ThemedStyle(self.root)
        self.style.set_theme("arc")

        # Load background image
        self.background_image = Image.open("header.png")
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        self.canvas = tk.Canvas(self.root, width=1200, height=213)
        self.canvas.pack(side=tk.TOP, pady=0, ipadx=0, ipady=0, fill=tk.X)

        # Set background image
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_photo)
        self.root.configure(bg='white')

        self.sidebar_frame = ttk.Frame(root, padding=(30, 100, 30, 0), style='Sidebar.TFrame')
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.home_button = ttk.Button(self.sidebar_frame, text="Home", command=self.display_home, style='Sidebar.TButton')
        self.home_button.pack(pady=10, ipady=5, fill=tk.X)

        self.info_button = ttk.Button(self.sidebar_frame, text="System Information", command=self.display_info, style='Sidebar.TButton')
        self.info_button.pack(pady=10, ipady=5, fill=tk.X)

        self.form_button = ttk.Button(self.sidebar_frame, text="Application Form", command=self.display_application_form, style='Sidebar.TButton')
        self.form_button.pack(pady=10, ipady=5, fill=tk.X)

        self.dashboard_button = ttk.Button(self.sidebar_frame, text="Student Records", command=self.open_student_records, style='Sidebar.TButton')
        self.dashboard_button.pack(pady=10, ipady=5, fill=tk.X)
        
        self.logout_button = ttk.Button(self.sidebar_frame, text="Logout", command=self.logout, style='Sidebar.TButton')
        self.logout_button.pack(pady=10, ipady=5, fill=tk.X)

        self.content_frame = ttk.Frame(root, padding=(50, 50, 50, 70), style='Content.TFrame')
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.applicants = []

        self.root.style = ttk.Style()

        self.root.style.configure('Sidebar.TButton', background='Black', foreground='Black', font=('Arial', 10, 'bold'), borderwidth=0)
        self.root.style.configure('Sidebar.TFrame', background='Maroon')
        self.root.style.configure('Content.TFrame', background='White')
        self.root.style.configure('Content.TLabel', background='White', borderwidth=0, relief='solid', padding=(5, 5), foreground='Black')
        self.root.style.configure('Content.TButton', background='Black', foreground='Maroon', font=('Arial', 10, 'bold'), borderwidth=10)
        
        self.display_home()
        
    def logout(self):
        # Display a confirmation message before logging out
        confirm_logout = messagebox.askyesno("Logout", "Are you sure you want to log out?")
        
        if confirm_logout:
            # Destroy the content within the content frame
            for widget in self.content_frame.winfo_children():
                widget.destroy()
                
            self.root.destroy()
        else:
            # Handle the case when the user clicks "No"
            pass
        
    def open_student_records(self):
        # para ma-open yung students records class
        student_records_display = StudentRecordsDisplay(self.content_frame, self.db_cursor, root)
        student_records_display.student_records()
        
    def populate_table(self):
        # Check if the Treeview widget exists
        if not hasattr(self, 'my_tree'):
            return

        # Clear existing content in the Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Fetch all applicants from the database
        self.db_cursor.execute("SELECT id, name, sr_code, gender, birthday, age, address, contact_number, school_university, program, gwa, family_income FROM applicants")
        applicants = self.db_cursor.fetchall()

        # Insert data into the Treeview
        for applicant in applicants:
            self.tree.insert(parent='', index='end', iid=applicant['id'], values=(
                applicant['id'],
                applicant['name'],
                applicant['sr_code'],
                applicant['gender'],
                applicant['birthday'],
                applicant['age'],
                applicant['address'],
                applicant['contact_number'],
                applicant['school_university'],
                applicant['program'],
                applicant['gwa'],
                applicant['family_income']
            ))

    def clear_content_frame(self):

        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def display_home(self):
        self.clear_content_frame()

        # Load and resize the PNG image
        image_path = "home.png"  # Replace with the actual path to your PNG image
        original_image = Image.open(image_path)

        # Resize the image to your desired dimensions
        resized_image = original_image.resize((1000, 300))  # Replace width and height with your desired dimensions

        photo = ImageTk.PhotoImage(resized_image)

        image_label = ttk.Label(self.content_frame, image=photo)
        image_label.image = photo  # Keep a reference to the image to prevent garbage collection
        image_label.pack()
        
        # Add text below the image
        info_text = """
        Empowering Minds, Enabling Futures: Your Educational Success, Our Priority.
        """
        info_label = ttk.Label(self.content_frame, text=info_text, font=('Arial', 14, 'italic'), style='Content.TLabel', justify = 'center')
        info_label.pack()

    def display_info(self):
        self.clear_content_frame()

        # Load and resize the PNG image
        image_path = "systeminfo.png"  # Replace with the actual path to your PNG image
        original_image = Image.open(image_path)

        # Resize the image to your desired dimensions
        resized_image = original_image.resize((1000, 300))  # Replace width and height with your desired dimensions

        photo = ImageTk.PhotoImage(resized_image)

        image_label = ttk.Label(self.content_frame, image=photo)
        image_label.image = photo  # Keep a reference to the image to prevent garbage collection
        image_label.pack()

        # Add text below the image
        info_text = """
        Unlock boundless opportunities for your education by seamlessly applying through our assistance system -
        a gateway to academic support tailored for your success, where enrollment, excellent grades, and certification of indigency pave the way to a brighter future.
        """
        info_label = ttk.Label(self.content_frame, text=info_text, font=('times', 12), style='Content.TLabel', justify = 'center')
        info_label.pack()
        
    def display_application_form(self):

        self.clear_content_frame()
        
        # Create a canvas to place the application form and a vertical scrollbar
        canvas = tk.Canvas(self.content_frame)
        
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        # Create a frame to hold the application form entries
        form_frame = ttk.Frame(canvas)

        canvas.create_window((10, 10), window=form_frame, anchor="nw")

        # Display application form
        form_label = ttk.Label(form_frame, text="APPLICATION FORM", font=('Arial', 16, 'bold'), style='Content.TLabel')
        form_label.pack(side=tk.TOP, pady=5, ipadx=400, ipady=10, fill=tk.X)  # Align the label to the left

        # Create labels and entry widgets for the form fields
        form_fields = [

            "Name (LN, FN, MI)", "Sr Code", "Gender", "Birthday", "Age", "Address",
            "Contact Number", "School/University", "Program", "GWA", "Family Income"
        ]

        self.form_entries = {}

        for field in form_fields:

            label = ttk.Label(form_frame, text=field, style='Content.TLabel')
            label.pack(side=tk.TOP, pady=5, ipadx=350, ipady=1, fill=tk.X)  # Align the label to the left

            if field == "Birthday":

                # Use tkcalendar DateEntry for the birthday input
                entry = DateEntry(form_frame, width=12, background='Maroon', foreground='white', borderwidth=2)
            elif field == "Gender":

                # Use ttk.Combobox for the gender input
                entry = ttk.Combobox(form_frame, values=["Male", "Female"], state="readonly")

            else:

                entry = ttk.Entry(form_frame, width=30)
            entry.pack(fill=tk.X)  # Allow the entry widget to expand horizontally
            self.form_entries[field] = entry

        # Submit button
        submit_button = ttk.Button(form_frame, text="Submit", command=self.submit_application, style='Content.TButton')
        submit_button.pack(side=tk.TOP, pady=5, ipadx=300, ipady=5, fill=tk.X)
        reset_button = ttk.Button(form_frame, text="Reset Form", command=self.reset_form, style='Content.TButton')
        reset_button.pack(side=tk.TOP, pady=5, ipadx=300, ipady=5, fill=tk.X)

        # Configure the canvas to scroll with the scrollbar
        form_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        # Pack the canvas into the content_frame
        canvas.pack(side="left", fill="both", expand=True)
    
    def submit_application(self):
        # Get data from the form entries
        applicant_data = {
            'name': self.form_entries['Name (LN, FN, MI)'].get(),
            'sr_code': self.form_entries['Sr Code'].get(),
            'gender': self.form_entries['Gender'].get(),
            'birthday': self.format_date(self.form_entries['Birthday'].get()),
            'age': int(self.form_entries['Age'].get()) if self.form_entries['Age'].get() else 0,
            'address': self.form_entries['Address'].get(),
            'contact_number': self.form_entries['Contact Number'].get(),
            'school_university': self.form_entries['School/University'].get(),
            'program': self.form_entries['Program'].get(),
            'gwa': float(self.form_entries['GWA'].get()) if self.form_entries['GWA'].get() else 0.0,
            'family_income': float(self.form_entries['Family Income'].get()) if self.form_entries['Family Income'].get() else 0.0
        }

        # Validate if all fields are filled
        if all(applicant_data.values()):
            # Insert data into the database
            insert_query = """
            INSERT INTO applicants 
            (name, sr_code, gender, birthday, age, address, contact_number, school_university, program, gwa, family_income) 
            VALUES (%(name)s, %(sr_code)s, %(gender)s, %(birthday)s, %(age)s, %(address)s, %(contact_number)s, %(school_university)s, %(program)s, %(gwa)s, %(family_income)s)
            """
            try:
                self.db_cursor.execute(insert_query, applicant_data)
                self.db_connection.commit()
                messagebox.showinfo("Success", "Application submitted successfully!")

                # Update the Treeview to display the new applicant
                self.populate_table()

                # Clear the form entries
                self.reset_form()
            except Exception as e:
                messagebox.showerror("Database Error", f"Error submitting application: {e}")
        else:
            messagebox.showwarning("Incomplete Form", "Please fill out all fields.")

    def format_date(self, date_str):
        # Convert the date from the DateEntry format to 'yyyy-mm-dd' format
        try:
            # Parse the date from the DateEntry format
            parsed_date = datetime.strptime(date_str, "%m/%d/%y")
            # Format the date to 'yyyy-mm-dd'
            formatted_date = parsed_date.strftime("%Y-%m-%d")
            return formatted_date
        except ValueError:
            return None
        
    def reset_form(self):
        for entry in self.form_entries.values():
            if isinstance(entry, ttk.Entry):
                entry.delete(0, tk.END)
            elif isinstance(entry, DateEntry):
                entry.set_date(None)
            elif isinstance(entry, ttk.Combobox):
                entry.set("")
                
    def run(self):
        self.root.mainloop()
        
                
class StudentRecordsDisplay(HomePage):
    def __init__(self, content_frame, db_cursor, root):
        self.db_connection = connection()
        self.content_frame = content_frame
        self.db_cursor = db_cursor
        self.db_connection = connection()
        self.db_cursor = self.db_connection.cursor(pymysql.cursors.DictCursor)
        self.root = root
        self.form_entries = {}  # Initialize form_entries here or within another method
        self.update_applicant_window = None
        
    def student_records(self):
        self.clear_content_frame()
        # Create a frame for the Treeview
        # Fetch all applicants from the database
        self.db_cursor.execute("SELECT * FROM applicants")
        applicants = self.db_cursor.fetchall()
        
        self.clear_content_frame()
        
        # Create a label for the table title
        title_label = tk.Label(self.content_frame, text="LIST OF ALL APPLICANTS", font=("Arial", 12, 'bold'))
        title_label.pack(pady=0)

        # Create a Treeview widget for the table in the __init__ method
        # Create a Treeview widget for the table
        columns = ("ID", "Name", "Sr Code", "Gender", "Birthday", "Age", "Address", "Contact Number", "School/University", "Program", "GWA", "Family Income")
        
        self.tree = ttk.Treeview(self.content_frame, columns=columns, show="headings")

        # center
        for col in columns:
            self.tree.heading(col, text=col, anchor=tk.CENTER)

        # column widths
        self.tree.column("ID", width=20)  
        self.tree.column("Name", width=150)  
        self.tree.column("Sr Code", width=45)  
        self.tree.column("Gender", width=40)
        self.tree.column("Birthday", width=55)
        self.tree.column("Age", width=30)
        self.tree.column("Address", width=155)  
        self.tree.column("Contact Number", width=85)
        self.tree.column("School/University", width=140)
        self.tree.column("Program", width=60)
        self.tree.column("GWA", width=30)
        self.tree.column("Family Income", width=70)
        
        for col in columns:
            self.tree.heading(col, text=col)

        # Insert data into the Treeview
        for applicant in applicants:
            self.tree.insert(parent='', index='end', iid=applicant['id'], values=(
                applicant['id'],
                applicant['name'],
                applicant['sr_code'],
                applicant['gender'],
                applicant['birthday'],
                applicant['age'],
                applicant['address'],
                applicant['contact_number'],
                applicant['school_university'],
                applicant['program'],
                applicant['gwa'],
                applicant['family_income']
            ))
            
        self.tree.pack(fill=tk.BOTH, expand=True, padx=0, pady=10)

        # Create a frame for the dashboard buttons
        dashboard_frame = ttk.Frame(self.content_frame, padding=(215, 0, 0, 0), style='Content.TFrame')
        dashboard_frame.pack(fill=tk.X)

        # Dashboard buttons
        qualified_button = ttk.Button(dashboard_frame, text="Qualified Applicants", command=self.show_qualified_applicants, style='Content.TButton')
        qualified_button.pack(side=tk.LEFT, padx=5)

        unqualified_button = ttk.Button(dashboard_frame, text="Unqualified Applicants", command=self.show_unqualified_applicants, style='Content.TButton')
        unqualified_button.pack(side=tk.LEFT, padx=5)
        
        update_button = ttk.Button(dashboard_frame, text="Update Applicant", command=self.update_applicant, style='Content.TButton')
        update_button.pack(side=tk.LEFT, padx=5)

        remove_button = ttk.Button(dashboard_frame, text="Remove Applicant", command=self.remove_applicant, style='Content.TButton')
        remove_button.pack(side=tk.LEFT, padx=5)
        
        # DISPLAY
    def display_all_applicants(self):
        # Fetch all applicants from the database
        self.db_cursor.execute("SELECT * FROM applicants")
        applicants = self.db_cursor.fetchall()
        
        self.clear_content_frame()
        
        # Create a label for the table title
        title_label = tk.Label(self.content_frame, text="LIST OF ALL APPLICANTS", font=("Arial", 12, 'bold'))
        title_label.pack(pady=0)

        # Create a Treeview widget for the table in the __init__ method
        # Create a Treeview widget for the table
        columns = ("ID", "Name", "Sr Code", "Gender", "Birthday", "Age", "Address", "Contact Number", "School/University", "Program", "GWA", "Family Income")
        self.tree = ttk.Treeview(self.content_frame, columns=columns, show="headings")

        # center
        for col in columns:
            self.tree.heading(col, text=col, anchor=tk.CENTER)

        # column widths
        self.tree.column("ID", width=20)  
        self.tree.column("Name", width=150)  
        self.tree.column("Sr Code", width=45)  
        self.tree.column("Gender", width=40)
        self.tree.column("Birthday", width=55)
        self.tree.column("Age", width=30)
        self.tree.column("Address", width=155)  
        self.tree.column("Contact Number", width=85)
        self.tree.column("School/University", width=140)
        self.tree.column("Program", width=60)
        self.tree.column("GWA", width=30)
        self.tree.column("Family Income", width=70)
        
        for col in columns:
            self.tree.heading(col, text=col)

        # Insert data into the Treeview
        for applicant in applicants:
            self.tree.insert(parent='', index='end', iid=applicant['id'], values=(
                applicant['id'],
                applicant['name'],
                applicant['sr_code'],
                applicant['gender'],
                applicant['birthday'],
                applicant['age'],
                applicant['address'],
                applicant['contact_number'],
                applicant['school_university'],
                applicant['program'],
                applicant['gwa'],
                applicant['family_income']
            ))
            
        self.tree.pack(fill=tk.BOTH, expand=True, padx=0, pady=10)
            
        # Create a frame for the dashboard buttons
        dashboard_frame = ttk.Frame(self.content_frame, padding=(215, 0, 0, 0), style='Content.TFrame')
        dashboard_frame.pack(fill=tk.X)

        # Dashboard buttons
        qualified_button = ttk.Button(dashboard_frame, text="Qualified Applicants", command=self.show_qualified_applicants, style='Content.TButton')
        qualified_button.pack(side=tk.LEFT, padx=5)

        unqualified_button = ttk.Button(dashboard_frame, text="Unqualified Applicants", command=self.show_unqualified_applicants, style='Content.TButton')
        unqualified_button.pack(side=tk.LEFT, padx=5)
        
        update_button = ttk.Button(dashboard_frame, text="Update Applicant", command=self.update_applicant, style='Content.TButton')
        update_button.pack(side=tk.LEFT, padx=5)

        remove_button = ttk.Button(dashboard_frame, text="Remove Applicant", command=self.remove_applicant, style='Content.TButton')
        remove_button.pack(side=tk.LEFT, padx=5)

        # QUALIFIED
    def show_qualified_applicants(self):
        self.db_cursor.execute("SELECT * FROM applicants WHERE gwa <= 2.00 AND family_income <= 15000.00;")
        applicants = self.db_cursor.fetchall()
        
        # Clear existing content in the content frame
        self.clear_content_frame()
        
        # Create a label for the table title
        title_label = tk.Label(self.content_frame, text="LIST OF ALL QUALIFIED APPLICANTS", font=("Arial", 12, 'bold'))
        title_label.pack(pady=0)
        
        if applicants:
            # Create a Treeview widget for the table
            columns = ("ID", "Name", "Sr Code", "Gender", "Birthday", "Age", "Address", "Contact Number", "School/University", "Program", "GWA", "Family Income")
            self.tree = ttk.Treeview(self.content_frame, columns=columns, show="headings")

            # Center column headings
            for col in columns:
                self.tree.heading(col, text=col, anchor=tk.CENTER)

            # Set column widths
            column_widths = [20, 150, 45, 40, 55, 30, 155, 85, 140, 60, 30, 70]
            for col, width in zip(columns, column_widths):
                self.tree.column(col, width=width)

            # Insert data into the Treeview for qualified applicants
            for applicant in applicants:
                self.tree.insert(parent='', index='end', iid=applicant['id'], values=(
                    applicant['id'],
                    applicant['name'],
                    applicant['sr_code'],
                    applicant['gender'],
                    applicant['birthday'],
                    applicant['age'],
                    applicant['address'],
                    applicant['contact_number'],
                    applicant['school_university'],
                    applicant['program'],
                    applicant['gwa'],
                    applicant['family_income']
                ))

                # Pack Treeview to content frame
                self.tree.pack(fill=tk.BOTH, expand=True, padx=0, pady=10)

        else:
            # Display a message if no qualified applicants are found
            label = ttk.Label(self.content_frame, text="No qualified applicants.", style='Content.TLabel')
            label.pack(anchor='w')  # Align the label to the left

        # Create a frame for the dashboard buttons
        dashboard_frame = ttk.Frame(self.content_frame, padding=(160, 0, 0, 0), style='Content.TFrame')
        dashboard_frame.pack(fill=tk.X)

        # Dashboard buttons
        all_applicants_button = ttk.Button(dashboard_frame, text="All Applicants", command=self.display_all_applicants, style='Content.TButton')
        all_applicants_button.pack(side=tk.LEFT, padx=5)

        unqualified_button = ttk.Button(dashboard_frame, text="Unqualified Applicants", command=self.show_unqualified_applicants, style='Content.TButton')
        unqualified_button.pack(side=tk.LEFT, padx=5)

        update_button = ttk.Button(dashboard_frame, text="Update Applicant", command=self.update_applicant, style='Content.TButton')
        update_button.pack(side=tk.LEFT, padx=5)
        
        remove_button = ttk.Button(dashboard_frame, text="Remove Applicant", command=self.remove_applicant, style='Content.TButton')
        remove_button.pack(side=tk.LEFT, padx=5)
        
        # Add a new button for downloading as PDF
        download_pdf_button = ttk.Button(dashboard_frame, text="Download as PDF", command=self.download_as_pdf, style='Content.TButton')
        download_pdf_button.pack(side=tk.LEFT, padx=5)

        #UNQUALIFIED
    def show_unqualified_applicants(self):
        self.db_cursor.execute("SELECT * FROM applicants WHERE gwa >= 2.01 or family_income >= 15001.00;")
        applicants = self.db_cursor.fetchall()
        
        # Clear existing content in the content frame
        self.clear_content_frame()
        
        # Create a label for the table title
        title_label = tk.Label(self.content_frame, text="LIST OF ALL UNQUALIFIED APPLICANTS", font=("Arial", 12, 'bold'))
        title_label.pack(pady=0)
        
        if applicants:
            # Create a Treeview widget for the table
            columns = ("ID", "Name", "Sr Code", "Gender", "Birthday", "Age", "Address", "Contact Number", "School/University", "Program", "GWA", "Family Income")
            self.tree = ttk.Treeview(self.content_frame, columns=columns, show="headings")

            # Center column headings
            for col in columns:
                self.tree.heading(col, text=col, anchor=tk.CENTER)

            # Set column widths
            column_widths = [20, 150, 45, 40, 55, 30, 155, 85, 140, 60, 30, 70]
            for col, width in zip(columns, column_widths):
                self.tree.column(col, width=width)

            # Insert data into the Treeview for unqualified applicants
            for applicant in applicants:
                self.tree.insert(parent='', index='end', iid=applicant['id'], values=(
                    applicant['id'],
                    applicant['name'],
                    applicant['sr_code'],
                    applicant['gender'],
                    applicant['birthday'],
                    applicant['age'],
                    applicant['address'],
                    applicant['contact_number'],
                    applicant['school_university'],
                    applicant['program'],
                    applicant['gwa'],
                    applicant['family_income']
                ))
                
                # Pack Treeview to content frame
                self.tree.pack(fill=tk.BOTH, expand=True, padx=0, pady=10)

        else:
            # Display a message if no unqualified applicants are found
            label = ttk.Label(self.content_frame, text="No unqualified applicants.", style='Content.TLabel')
            label.pack(anchor='w')  # Align the label to the left
            
        # Create a frame for the dashboard buttons
        dashboard_frame = ttk.Frame(self.content_frame, padding=(240, 0, 0, 0), style='Content.TFrame')
        dashboard_frame.pack(fill=tk.X)

        # Dashboard buttons
        all_applicants_button = ttk.Button(dashboard_frame, text="All Applicants", command=self.display_all_applicants, style='Content.TButton')
        all_applicants_button.pack(side=tk.LEFT, padx=5)

        qualified_button = ttk.Button(dashboard_frame, text="Qualified Applicants", command=self.show_qualified_applicants, style='Content.TButton')
        qualified_button.pack(side=tk.LEFT, padx=5)
        
        update_button = ttk.Button(dashboard_frame, text="Update Applicant", command=self.update_applicant, style='Content.TButton')
        update_button.pack(side=tk.LEFT, padx=5)

        remove_button = ttk.Button(dashboard_frame, text="Remove Applicant", command=self.remove_applicant, style='Content.TButton')
        remove_button.pack(side=tk.LEFT, padx=5)
        
        # UPDATE
    def update_applicant(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select an applicant to update.")
            return

        applicant_info = self.tree.item(selected_item, 'values')
        applicant_id = applicant_info[0]

        # Open a new window to update applicant info
        self.update_applicant_window = tk.Toplevel(self.content_frame)
        self.update_applicant_window.title("Update Applicant")

        # Entry fields for updating applicants
        name_entry = tk.Entry(self.update_applicant_window)
        sr_code_entry = tk.Entry(self.update_applicant_window)
        gender_combobox = ttk.Combobox(self.update_applicant_window, values=["Male", "Female"])
        gender_combobox.configure(state='readonly')
        birthday_entry = DateEntry(self.update_applicant_window, width=12, background='Maroon', foreground='white', borderwidth=2)
        age_entry = tk.Entry(self.update_applicant_window)
        address_entry = tk.Entry(self.update_applicant_window)
        contact_number_entry = tk.Entry(self.update_applicant_window)
        school_university_entry = tk.Entry(self.update_applicant_window)
        program_entry = tk.Entry(self.update_applicant_window)
        gwa_entry = tk.Entry(self.update_applicant_window)
        family_income_entry = tk.Entry(self.update_applicant_window)

        # Labels for entry fields
        tk.Label(self.update_applicant_window, text="Name:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        tk.Label(self.update_applicant_window, text="Sr Code:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        tk.Label(self.update_applicant_window, text="Gender:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        tk.Label(self.update_applicant_window, text="Birthday:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        tk.Label(self.update_applicant_window, text="Age:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
        tk.Label(self.update_applicant_window, text="Address:").grid(row=5, column=0, padx=10, pady=5, sticky="e")
        tk.Label(self.update_applicant_window, text="Contact Number:").grid(row=6, column=0, padx=10, pady=5, sticky="e")
        tk.Label(self.update_applicant_window, text="School/University:").grid(row=7, column=0, padx=10, pady=5, sticky="e")
        tk.Label(self.update_applicant_window, text="Program:").grid(row=8, column=0, padx=10, pady=5, sticky="e")
        tk.Label(self.update_applicant_window, text="GWA:").grid(row=9, column=0, padx=10, pady=5, sticky="e")
        tk.Label(self.update_applicant_window, text="Family Income:").grid(row=10, column=0, padx=10, pady=5, sticky="e")
        
        # Entry fields placement
        name_entry.grid(row=0, column=1, padx=30, pady=5)
        sr_code_entry.grid(row=1, column=1, padx=30, pady=5)
        gender_combobox.grid(row=2, column=1, padx=30, pady=5)
        birthday_entry.grid(row=3, column=1, padx=30, pady=5)
        age_entry.grid(row=4, column=1, padx=30, pady=5)
        address_entry.grid(row=5, column=1, padx=30, pady=5)
        contact_number_entry.grid(row=6, column=1, padx=30, pady=5)
        school_university_entry.grid(row=7, column=1, padx=30, pady=5)
        program_entry.grid(row=8, column=1, padx=30, pady=5)
        gwa_entry.grid(row=9, column=1, padx=30, pady=5)
        family_income_entry.grid(row=10, column=1, padx=30, pady=5)

        # Set the default values to the selected applicant's information
        name_entry.insert(0, applicant_info[1])
        sr_code_entry.insert(0, applicant_info[2])
        gender_combobox.set(applicant_info[3])

        # Convert the date to the 'MM-DD-YYYY' format
        old_date_format = "%Y-%m-%d"  
        new_date_format = "%m/%d/%y"  # change format

        # Parse the date from the existing format to a datetime object
        parsed_date = datetime.strptime(applicant_info[4], old_date_format)

        # Convert the datetime object to the desired format as a string
        formatted_date = parsed_date.strftime(new_date_format)

        # Set the formatted date as the default value for birthday
        birthday_entry.set_date(formatted_date)
        age_entry.insert(0, applicant_info[5])
        address_entry.insert(0, applicant_info[6])
        contact_number_entry.insert(0, applicant_info[7])
        school_university_entry.insert(0, applicant_info[8])
        program_entry.insert(0, applicant_info[9])
        gwa_entry.insert(0, applicant_info[10])
        family_income_entry.insert(0, applicant_info[11])

        # Button to save updated applicant information
        save_button = tk.Button(self.update_applicant_window, text="Save Changes", command=lambda: self.save_updated_applicant_info(
        applicant_id, name_entry.get(), sr_code_entry.get(),  gender_combobox.get(), birthday_entry.get(), age_entry.get(), address_entry.get(),
        contact_number_entry.get(), school_university_entry.get(), program_entry.get(), gwa_entry.get(), family_income_entry.get()))
        save_button.grid(row=12, columnspan=2, pady=10)

        def clear_fields():
            name_entry.delete(0, 'end')
            sr_code_entry.delete(0, 'end')
            gender_combobox.set('')
            birthday_entry.set_date(None)
            age_entry.delete(0, 'end')
            address_entry.delete(0, 'end')
            contact_number_entry.delete(0, 'end')
            school_university_entry.delete(0, 'end')
            program_entry.delete(0, 'end')
            gwa_entry.delete(0, 'end')
            family_income_entry.delete(0, 'end')

        clear_button = tk.Button(self.update_applicant_window, text="Clear Fields", command=clear_fields)
        clear_button.grid(row=13, columnspan=2, pady=10)

        # SAVE UPDATED INFO
    def save_updated_applicant_info(self, applicant_id, name, sr_code, gender, birthday, age, address, contact_number, school_university, program, gwa, family_income):
        try:
            # Convert the date format from 'mm/dd-yy' to 'yyyy-mm-dd'
            old_date_format = "%m/%d/%y"
            new_date_format = "%Y-%m-%d"

            # Parse the date from the 'mm/dd-yy' format to a datetime object
            parsed_date = datetime.strptime(birthday, old_date_format)

            # Convert the datetime object to the desired 'yyyy-mm-dd' format as a string
            formatted_date = parsed_date.strftime(new_date_format)

            cursor = self.db_connection.cursor()
            query = "UPDATE applicants SET name=%s, sr_code=%s, gender=%s, birthday=%s, age=%s, address=%s, contact_number=%s, school_university=%s, program=%s, gwa=%s, family_income=%s WHERE id=%s"
            values = (name, sr_code, gender, formatted_date, age, address, contact_number, school_university, program, gwa, family_income, applicant_id)
            cursor.execute(query, values)

            self.db_connection.commit()
            messagebox.showinfo("Success", "Applicant information updated successfully!")

            # Update the table with the updated applicant information
            self.populate_table()
            self.update_applicant_window.destroy()

        except Exception as e:
            print(f"Error: {e}")
            messagebox.showerror("Error", "Error updating applicant information.")

        finally:
            if cursor:
                cursor.close()
    
        # REMOVE
    def remove_applicant(self):
        selected_item = self.tree.selection()
        
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select an applicant to delete.")
            return
        
        id = self.tree.item(selected_item)['values'][0]
        confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to delete this applicant?")
        
        if confirmation:
            delete_query="""DELETE FROM applicants WHERE id = %s"""
            try:
                self.db_cursor.execute(delete_query, id)
                self.db_connection.commit()
                print("Deletion Successful")  
                messagebox.showinfo("Success", "Applicant deleted successfully!")
                self.student_records()
                
            except Exception as e:
                print(f"Deletion Failed: {e}") 
                messagebox.showerror("Error", f"Failed to delete applicant: {e}")

        # DOWNLOAD PDF FILE
    def download_as_pdf(self):
        # Check if an applicant is selected in the Treeview
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Applicant Selected", "Please select an applicant.")
            return

        # Get the selected applicant's ID
        selected_id = selected_item[0]

        # Fetch the details of the selected applicant from the database
        self.db_cursor.execute("SELECT * FROM applicants WHERE id = %s", (selected_id,))
        selected_applicant = self.db_cursor.fetchone()

        # Ask the user to choose a file location for saving the PDF
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])

        # Check if a valid file path has been selected
        if file_path and file_path.endswith('.pdf'):
            # Create a PDF document
            pdf_canvas = canvas.Canvas(file_path, pagesize=letter)

            # Set font and size
            pdf_canvas.setFont("Times-Roman", 12)
            
            # Add an image at the top (adjust coordinates as needed)
            image_path = "logoo.png"
            pdf_canvas.drawInlineImage(image_path, 420, 640, width=100, height=90)
            image_path = "logobsu.png"
            pdf_canvas.drawInlineImage(image_path, 340, 650, width=80, height=70)
            
            # Add additional text at the top
            pdf_canvas.setFont("Times-Roman", 14)
            pdf_canvas.drawString(100, 800, "")  # Adjusted y-coordinate
            pdf_canvas.setFont("Times-Roman", 12)
            pdf_canvas.setFont("Times-Bold", 14)  # Set font to bold
            pdf_canvas.drawString(100, 700, "BATANGAS STATE UNIVERSITY")  # Adjusted y-coordinate
            pdf_canvas.drawString(100, 680, "The National Engineering University")  # Adjusted y-coordinate
            pdf_canvas.drawString(100, 660, "Alangilan Campus")  # Adjusted y-coordinate
            
            pdf_canvas.setFont("Times-Bold", 14)
            pdf_canvas.setFillColorRGB(0.5, 0, 0)  # RGB values for maroon 
            pdf_canvas.drawString(100, 625, "EDUCATIONAL ASSISTANCE APPLICATION SYSTEM")  # Adjusted y-coordinate
            
            pdf_canvas.setFont("Times-Bold", 14)  # Set font to bold
            pdf_canvas.setFillColorRGB(0, 0, 0)
            pdf_canvas.drawString(100, 600, "Confirmation of Qualification for Educational Assistance")  # Adjusted y-coordinate
            
            pdf_canvas.setFont("Times-Roman", 12)
            pdf_canvas.drawString(100, 580, "We are pleased to inform you that, after careful review and consideration of your")
            pdf_canvas.drawString(100, 560, "application for educational assistance, you have been found eligible and qualified")  # Adjusted y-coordinate
            pdf_canvas.drawString(100, 540, "for the Educational Assistance Program at BSU - Alangilan Campus.")  # Adjusted y-coordinate
            
            pdf_canvas.setFont("Times-Italic", 12)  # Set font to italic
            pdf_canvas.drawString(100, 510, "Details of your qualification are as follows:")  # Adjusted y-coordinate
            
            pdf_canvas.setFont("Times-Roman", 12)
            pdf_canvas.drawString(100, 180, "Your dedication to academic excellence and commitment to your studies have been")  # Adjusted y-coordinate
            pdf_canvas.drawString(100, 160, "recognized, and we are confident that the support provided through the Educational")  # Adjusted y-coordinate
            pdf_canvas.drawString(100, 140, "Assistance Program will contribute to your continued success in your academic")  # Adjusted y-coordinate
            pdf_canvas.drawString(100, 120, "journey.")  # Adjusted y-coordinate
            
            pdf_canvas.setFont("Times-Bold", 11)  # Set font to bold
            pdf_canvas.drawString(100, 90, "Congratulations once again on qualifying for the educational assistance application!")  # Adjusted y-coordinate
            
            pdf_canvas.setFont("Times-Italic", 12)
            pdf_canvas.drawString(100, 70, "We look forward in supporting you in your educational endeavors.")  # Adjusted y-coordinate
        
           
            # Add design elements
            pdf_canvas.setStrokeColorRGB(0, 0, 0)  # Set border color to black
            pdf_canvas.rect(100, 220, 400, 265)  # Add a border around the applicant information

            # Write the selected applicant's information to the PDF
            pdf_canvas.setFont("Times-Roman", 12)
            pdf_canvas.drawString(120, 460, f"Applicant ID: {selected_applicant['id']}")
            pdf_canvas.drawString(120, 440, f"Name: {selected_applicant['name']}")
            pdf_canvas.drawString(120, 420, f"Sr Code: {selected_applicant['sr_code']}")
            pdf_canvas.drawString(120, 400, f"Gender: {selected_applicant['gender']}")
            pdf_canvas.drawString(120, 380, f"Birthday: {selected_applicant['birthday']}")
            pdf_canvas.drawString(120, 360, f"Age: {selected_applicant['age']}")
            pdf_canvas.drawString(120, 340, f"Address: {selected_applicant['address']}")
            pdf_canvas.drawString(120, 320, f"Contact Number: {selected_applicant['contact_number']}")
            pdf_canvas.drawString(120, 300, f"School/University: {selected_applicant['school_university']}")
            pdf_canvas.drawString(120, 280, f"Program: {selected_applicant['program']}")
            
            pdf_canvas.setFont("Times-Bold", 12)  # Set font to bold
            pdf_canvas.drawString(120, 260, f"GWA: {selected_applicant['gwa']}")
            pdf_canvas.drawString(120, 240, f"Family Income: {selected_applicant['family_income']}")
        

            # Save the PDF
            pdf_canvas.save()

            # Inform the user that the PDF has been generated
            messagebox.showinfo("PDF Downloaded", f"The PDF file has been saved at:\n{file_path}")
        else:
            # Inform the user that no valid file path was selected
            messagebox.showwarning("Invalid File Path", "Please select a valid file path for saving the PDF.")


if __name__ == "__main__":
    root = tk.Tk()
    login_page = LoginPage(root)
    root.mainloop()