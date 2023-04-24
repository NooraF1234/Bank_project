import mysql.connector
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import random

# Connect to the MySQL database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Hendrickson12!",
  database="bank_program"
)

# Create a cursor object to execute SQL queries
mycursor = mydb.cursor()

# Create the GUI window
root = tk.Tk()
root.title("Banking System")

# Create the labels and entry boxes
account_label = tk.Label(root, text="Account Number:")
account_label.grid(row=0, column=0, padx=10, pady=10)
account_entry = tk.Entry(root)
account_entry.grid(row=0, column=1, padx=10, pady=10)



pin_label = tk.Label(root, text="PIN:")
pin_label.grid(row=1, column=0, padx=10, pady=10)
pin_entry = tk.Entry(root, show="*")
pin_entry.grid(row=1, column=1, padx=10, pady=10)

# new_account_button = tk.Button(text="New Account")
# new_account_button.grid(padx=10, pady=10)

# Create the login button
def login():
    account_num = account_entry.get()
    pin = pin_entry.get()
    
    # Check if the account number and PIN are valid
    mycursor.execute("SELECT * FROM bank_program.bank WHERE account_num = %s AND pin = %s", (account_num, pin))
    account = mycursor.fetchone()
    

    
    if account:
        messagebox.showinfo("Login Success", "Welcome " + account[2] + "!")
        show_options()
    else:
        messagebox.showerror("Login Failed", "Invalid Account Number or PIN")

login_button = tk.Button(root, text="Login", command=login)
login_button.grid(row=2, column=1, padx=10, pady=10)

# Create the main options frame
options_frame = tk.Frame(root)

def show_options():

    new_account_button.grid_forget()
    options_frame.grid(row=3, column=0, columnspan=2)
    
    
    deposit_button = tk.Button(options_frame, text="Deposit", command=deposit)
    deposit_button.pack(padx=10, pady=10)
    
    withdraw_button = tk.Button(options_frame, text="Withdraw", command=withdraw)
    withdraw_button.pack(padx=10, pady=10)

    



def new_account():
    account_num = random.randint(100000, 999999)
    pin = tk.simpledialog.askinteger("New Account", "Choose a 4-digit PIN:")
    name = tk.simpledialog.askstring("New Account", "Enter your name:")
    balance = tk.simpledialog.askfloat("New Account", "Enter your initial deposit:")
    birthdate = tk.simpledialog.askstring("New Account", "Birthdate: ")

    if not (name and balance and pin and birthdate and account_num):
        return
    
    # Insert the new account into the database
    sql = "INSERT INTO bank_program.bank (account_num, pin, name, balance, birthdate) VALUES (%s, %s, %s, %s, %s)"
    val = (account_num, pin, name, balance, birthdate)
    mycursor.execute(sql, val)
    mydb.commit()
    
    messagebox.showinfo("New Account", "Account created successfully!")
    messagebox.showinfo("Account number", f"Your account number is {account_num}")
    messagebox.showinfo("Pin", f"Your pin is {pin}")
    messagebox.showinfo("Balance", f"Your balance is {balance}")

new_account_button = tk.Button(text="New Account", command=new_account)
new_account_button.grid(padx=10, pady=10)




# Define the function to check the balance

def check_balance():
    account_num = account_entry.get()
    pin = pin_entry.get()

    # Check if the account number and PIN are valid
    mycursor.execute("SELECT * FROM bank_program.bank WHERE account_num = %s AND pin = %s", (account_num, pin))
    account = mycursor.fetchone()

    # If the account is valid, retrieve the balance
    if account:
        mycursor.execute("SELECT balance FROM bank_program.bank WHERE account_num = %s AND pin = %s", (account_num, pin))
        balance = mycursor.fetchone()[0]
        messagebox.showinfo("Balance", "Your balance is $" + str(balance))
    else:
        messagebox.showerror("Error", "Invalid Account Number or PIN")
balance_button = tk.Button(options_frame, text="Check Balance", command=check_balance)
balance_button.pack(padx=10, pady=10)



def deposit():
    # Get the account number, PIN, and deposit amount from the user
    account_num = account_entry.get()
    pin = pin_entry.get()
    amount = simpledialog.askfloat("Deposit", "Enter the amount to deposit:")

    # Check if the account number and PIN are valid
    mycursor.execute("SELECT * FROM bank_program.bank WHERE account_num = %s AND pin = %s", (account_num, pin))
    account = mycursor.fetchone()

    # If the account is valid, update the balance by adding the deposit amount to the current balance
    if account:
        balance = account[3] + amount
        # Update the balance in the database
        mycursor.execute("UPDATE bank_program.bank SET balance = %s WHERE account_num = %s", (balance, account_num))
        mydb.commit()
        messagebox.showinfo("Deposit Success", "Deposit of $" + str(amount) + " was successful. New balance is $" + str(balance))
    else:
        messagebox.showerror("Error", "Invalid Account Number or PIN")




def withdraw():
    # Get the account number, PIN, and withdrawal amount from the user
    account_num = account_entry.get()
    pin = pin_entry.get()
    amount = simpledialog.askfloat("Withdraw", "Enter the amount to withdraw:")

    # Check if the account number and PIN are valid
    mycursor.execute("SELECT * FROM bank_program.bank WHERE account_num = %s AND pin = %s", (account_num, pin))
    account = mycursor.fetchone()

    # If the account is valid and the balance is sufficient, update the balance and display a success message
    if account:
        balance = account[3]
        if balance >= amount:
            new_balance = balance - amount
            mycursor.execute("UPDATE bank_program.bank SET balance = %s WHERE account_num = %s", (new_balance, account_num))
            mydb.commit()
            messagebox.showinfo("Withdraw", "Withdrawal successful. Your new balance is $" + str(new_balance))
        else:
            messagebox.showerror("Withdraw", "Insufficient funds.")
    else:
        messagebox.showerror("Error", "Invalid Account Number or PIN")

def close_account():
    account_num = account_entry.get()
    pin = pin_entry.get()

    # Check if the account number and PIN are valid
    mycursor.execute("SELECT * FROM bank_program.bank WHERE account_num = %s AND pin = %s", (account_num, pin))
    account = mycursor.fetchone()

    # If the account is valid, delete it from the database
    if account:
        mycursor.execute("DELETE FROM bank_program.bank WHERE account_num = %s", (account_num,))
        mydb.commit()
        messagebox.showinfo("Close Account", "Account closed successfully!")
        root.destroy()
    else:
        messagebox.showerror("Error", "Invalid Account Number or PIN")
close_account_button = tk.Button(options_frame, text="Close Account", command=close_account)
close_account_button.pack(padx=10, pady=10)



def modify_account():
    account_num = account_entry.get()
    pin = pin_entry.get()

    # Check if the account number and PIN are valid
    mycursor.execute("SELECT * FROM bank_program.bank WHERE account_num = %s AND pin = %s", (account_num, pin))
    account = mycursor.fetchone()

    # If the account is valid, prompt the user to choose what to modify and enter a new value
    if account:
        choice = simpledialog.askstring("Modify Account", "What would you like to modify? (name/pin/birthdate)")
        new_value = None
        
        if choice == "name":
            new_value = simpledialog.askstring("Modify Account", "Enter your new name:")
        elif choice == "pin":
            new_value = simpledialog.askinteger("Modify Account", "Enter your new 4-digit PIN:")
        elif choice == "birthdate":
            new_value = simpledialog.askstring("Modify Account", "Enter your new birthdate:")
        
        if new_value:
            # Update the account with the new value
            sql = f"UPDATE bank_program.bank SET {choice} = %s WHERE account_num = %s AND pin = %s"
            val = (new_value, account_num, pin)
            mycursor.execute(sql, val)
            mydb.commit()

            messagebox.showinfo("Modify Account", "Account updated successfully!")
    else:
        messagebox.showerror("Error", "Invalid Account Number or PIN")
modify_account_button = tk.Button(options_frame, text="Modify Account", command=modify_account)
modify_account_button.pack(padx=10, pady=10)





root.mainloop()


