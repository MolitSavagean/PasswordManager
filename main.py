from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [(random.choice(letters)) for _ in range(nr_letters)]
    password_symbols = [(random.choice(symbols)) for _ in range(nr_symbols)]
    password_numbers = [(random.choice(numbers)) for _ in range(nr_numbers)]

    password_list = password_letters + password_symbols + password_numbers
    random.shuffle(password_list)

    gen_password = "".join(password_list)
    password_entry.delete(0, END)
    password_entry.insert(END, f"{gen_password}")
    pyperclip.copy(gen_password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = web_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Error", message="Please don't leave any fields empty")
    else:
        try:
            with open("data.json", "r") as data:
                data_file = json.load(data)
        except FileNotFoundError:
            with open("data.json", "w") as data:
                json.dump(new_data, data, indent=4)
        else:
            data_file.update(new_data)
            with open("data.json", "w") as data:
                json.dump(data_file, data, indent=4)
        finally:
            web_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- SEARCH ------------------------------- #

def search():
    website = web_entry.get()
    try:
        with open("data.json", "r") as data:
            data_file = json.load(data)
    except FileNotFoundError:
        messagebox.showinfo(title="ERROR", message="No data file found")
    else:
        if website in data_file:
            email = data_file[website]['email']
            password = data_file[website]['password']
            messagebox.showinfo(title=f"{website}", message=f"Email: {email}\nPassword: {password}")
            pyperclip.copy(password)
        else:
            messagebox.showinfo(title="ERROR", message="No details for the website exists")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_image)
canvas.grid(column=1, row=0)

web_label = Label(text="Website:")
web_label.grid(column=0, row=1)
email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)
password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

web_entry = Entry(width=30)
web_entry.grid(column=1, row=1, sticky="EW")
web_entry.focus()
email_entry = Entry(width=35)
email_entry.insert(END, "mohitsajeevan2001@gmail.com")
email_entry.grid(column=1, row=2, columnspan=2, sticky="EW")
password_entry = Entry(width=30)
password_entry.grid(column=1, row=3, sticky="EW")

password_button = Button(text="Generate Password", command=generate_password)
password_button.grid(column=2, row=3, sticky="E")
add_button = Button(text="Add", width=36, command=save)
add_button.grid(column=1, row=4, columnspan=2, sticky="EW")
search_button = Button(text="Search", command=search)
search_button.grid(column=2, row=1, sticky="EW")

window.mainloop()
