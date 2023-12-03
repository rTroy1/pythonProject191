from tkinter import *
from tkinter import messagebox
import datetime
import smtplib




class App:
    def __init__(self):
        self.window = Tk()
        self.window.title("Website Blocker")
        self.window.config(padx=200, pady=50, bg="#79AC78")
        self.window.geometry("1600x1000")


        self.canvas = Canvas(self.window, width=854, height=500)
        self.image_1 = PhotoImage(file="Screenshot 2023-10-23 185541.png")
        self.canvas.create_image(427, 275, image=self.image_1)

        button = Button(text="Next", width=7, command=self.action)
        button.grid(row=1, column=1)

        self.canvas.grid(row=0, column=1, pady=10)

        self.website_list_entry = None  # Initialize as None
        self.duration_entry = None  # Initialize as None

        self.current_user_email = None  # Track the current user's email

        self.window.mainloop()

    def action(self):
        window_1 = Toplevel()
        window_1.title("Three Canvases in a Row")
        window_1.config(padx=20, pady=0, bg="#79AC78")
        window_1.geometry("1600x1000")

        self.image_2 = PhotoImage(file="Screenshot 2023-10-24 131043 (1).png")
        self.image_3 = PhotoImage(file="parent.png")
        self.image_4 = PhotoImage(file="299105_lock_icon (1).png")

        canvas0 = Canvas(window_1, width=600, height=100, bg="#79AC78")
        canvas0.create_text(300, 50, fill="white", text="Who's using ?", font=("Courier", 35, "bold"))
        canvas0.config(highlightthickness=0)
        canvas0.grid(row=0, column=0, columnspan=2, pady=50)

        def website_block():
            websites = [site.strip() for site in self.website_list_entry.get("1.0", "end-1c").split('\n') if site.strip()]

            # Get blocking duration, handle empty entry
            blocking_duration_str = self.duration_entry.get()
            if blocking_duration_str:
                blocking_duration = int(blocking_duration_str)
            else:
                # Handle the case when the entry is empty
                print("Blocking duration is empty. Please enter a valid duration.")
                return

            end_time = datetime.datetime.now() + datetime.timedelta(days=blocking_duration)
            host_path = "C:/Windows/System32/drivers/etc/hosts"
            redirect = "127.0.0.1"

            if datetime.datetime.now() < end_time:
                with open(host_path, "r+") as host_file:
                    content = host_file.read()
                    for website in websites:
                        if  website not in content:
                            host_file.write(redirect + " " + website + "\n")
                        else:
                            pass

            # If time is greater than end_time
            else:
                with open(host_path, "r+") as host_file:
                    content = host_file.readlines()
                    host_file.seek(0)
                    for lines in content:
                        if not any(website in lines for website in websites):
                            host_file.write(lines)
                    host_file.truncate()

            my_email = "221030109@juitsolan.in"
            password = "zuwmrqnvptaiiajd"



            connection = smtplib.SMTP("smtp.gmail.com", port=587)
            connection.starttls()

            connection.login(user=my_email, password=password)
            connection.sendmail(from_addr=my_email, to_addrs=email_entry_login.get(),
                                msg=f"Websites {websites} have been blocked successfully for {blocking_duration} days")
            connection.close()

            print("Email sent!")



        def unblock_websites():
            websites = [site.strip() for site in self.website_list_entry.get("1.0", "end-1c").split('\n') if site.strip()]
            host_path = "C:/Windows/System32/drivers/etc/hosts"

            with open(host_path, "r+") as host_file:
                content = host_file.readlines()
                host_file.seek(0)
                for line in content:
                    if not any(website in line for website in websites):
                        host_file.write(line)
                host_file.truncate()

        def signup():
            password = password_entry_login.get()
            email = email_entry_login.get()
            is_ok = messagebox.askokcancel(title="Website",
                                           message=f"These are the details entered:\nEmail: {email}"
                                                   f"\nPassword: {password}\nIs it ok to save?")
            if is_ok:
                # Create a file with the user's email as the filename
                filename = f"{email}.txt"
                with open(filename, 'w') as user_file:
                    user_file.write(f"Email: {email}\nPassword: {password}\n")

                # Add the user to the passwords.txt file
                with open("passwords.txt", 'a') as data_file:
                    data_file.write(f"{email}|{password}\n")

                email_entry_login.delete(0, END)
                password_entry_login.delete(0, END)

                # Show a message box with successful signup message
                messagebox.showinfo("Signup Successful", "Signup successful! Now please login.")

                login_page()  # Open the login page after signup

        def login():
            user_email = email_entry_login.get()
            with open("email_login","w") as newfile:
                newfile.write(email_entry_login.get())
            user_password = password_entry_login.get()

            try:
                with open("passwords.txt", 'r') as data_file:
                    for line in data_file:
                        saved_email, saved_password = line.strip().split('|')
                        if user_email == saved_email and user_password == saved_password:

                            self.current_user_email = user_email
                            window_3 = Toplevel()
                            window_3.title("Main Page")
                            window_3.config(padx=50, pady=50)

                            url_label = Label(window_3, text="ENTER URLs (one per line)", bg="#79AC78")
                            url_label.grid(row=1, column=0)

                            self.website_list_entry = Text(window_3, width=35, height=5)
                            self.website_list_entry.grid(row=1, column=1)

                            duration_label = Label(window_3, text="Blocking Duration (days):", bg="#79AC78")
                            duration_label.grid(row=2, column=0)

                            self.duration_entry = Entry(window_3, width=35)
                            self.duration_entry.grid(row=2, column=1)

                            submit_button_1 = Button(window_3, text="Start Blocking", command=website_block)
                            submit_button_1.grid(row=3, column=0)

                            unblock_button = Button(window_3, text="Unblock Websites", command=unblock_websites)
                            unblock_button.grid(row=3, column=1)

                            return
            except FileNotFoundError:
                pass  # Ignore the error if the file doesn't exist

            # Login failed
            messagebox.showerror("Login Failed", "Invalid email or password")

        def login_page():
            window_2 = Toplevel()
            window_2.title("Login Page")
            window_2.config(padx=50, pady=50)

            email_label_login = Label(window_2, text="ENTER EMAIL", bg="#79AC78")
            email_label_login.grid(row=1, column=0)

            global email_entry_login
            email_entry_login = Entry(window_2, width=35)
            email_entry_login.grid(row=1, column=1)

            global password_entry_login
            password_label_login = Label(window_2, text="ENTER PASSWORD", bg="#79AC78")
            password_label_login.grid(row=2, column=0)


            password_entry_login = Entry(window_2, width=35, show="*")
            password_entry_login.grid(row=2, column=1)

            login_button = Button(window_2, text="LOGIN", command=login)
            login_button.grid(row=4, column=0)


            signup_button = Button(window_2, text="SIGN UP", command=signup)
            signup_button.grid(row=4, column=1)

            window_2.mainloop()

        canvas1 = Canvas(window_1, width=300, height=299)
        canvas1.create_image(150, 149, image=self.image_2)
        canvas1.config(bg="white", highlightthickness=0)


        button_1 = Button(window_1, image=self.image_2, command=login_page)
        button_1.grid(row=1, column=0, padx=50)


        canvas2 = Canvas(window_1, width=300, height=300)
        canvas2.create_image(150, 150, image=self.image_3)
        canvas2.config(bg="white", highlightthickness=0)


        button2 = Button(window_1, image=self.image_3, command=login_page)
        button2.grid(row=1, column=2, padx=50)

        window_1.mainloop()


if __name__ == "__main__":
    app = App()


