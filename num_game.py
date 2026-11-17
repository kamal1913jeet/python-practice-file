import tkinter as tk
from tkinter import messagebox
import random
# Global variables
random_number = random.randint(1, 100)
attempts = 0
username = ""
# Start Game Function
def start_game():
    global username, random_number, attempts

    username = name_entry.get().strip()

    if username == "":
        messagebox.showwarning("Name Required", "Please enter your name")
        return
    # Hide name section
    name_label.place_forget()
    name_entry.place_forget()
    start_button.place_forget()

    # Generate a new number
    random_number = random.randint(1, 100)
    attempts = 0

    # Show guessing section
    guess_label.place(x=75, y=40)
    guess_entry.place(x=130, y=85)
    submit_button.place(x=175, y=130)
    feedback_label.place(x=50, y=180)

    feedback_label.config(text=f"Good luck, {username}!")
# Check Guess Function
def check_guess():
    global attempts

    guess = guess_entry.get().strip()

    if not guess.isdigit():
        messagebox.showinfo("Invalid Input", "Enter a valid number")
        return
    guess = int(guess)

    if guess < 1 or guess > 100:
        messagebox.showwarning("Invalid Number", "Enter a number between 1 and 100")
        return

    attempts += 1

    if guess < random_number:
        feedback_label.config(text="Too low! Try again.")

    elif guess > random_number:
        feedback_label.config(text="Too high! Try again.")

    else:
        feedback_label.config(
            text=f"Correct! You guessed it in {attempts} attempts."
        )

        save_results(username, attempts)
        submit_button.config(state="disabled")
# Save Result Function
def save_results(name, num_attempts):
    messagebox.showinfo(
        "Result Saved",
        f"Good job, {name}!\nYour score is saved.\nAttempts: {num_attempts}"
    )
# Main Window
root = tk.Tk()
root.title("Number Guessing Game")
root.geometry("400x270")
root.resizable(False, False)
root.config(background="blue")
# Name Section
name_label = tk.Label(
    root,
    text="Enter Your Name:",
    font=("High Tower Text", 18),
    bg="yellow"
)
name_label.place(x=115, y=50)

name_entry = tk.Entry(root, font=("Arial", 18), width=10)
name_entry.place(x=130, y=100)

start_button = tk.Button(
    root,
    text="START",
    command=start_game,
    bg="#F51BC9",
    fg="white",
    relief="raised",
    borderwidth=5
)
start_button.place(x=175, y=200)


# Guessing Section
guess_label = tk.Label(
    root,
    text="Guess a Number (1-100)",
    font=("High Tower Text", 18),
    bg="lightblue"
)

guess_entry = tk.Entry(root, font=("Arial", 20), width=10)

submit_button = tk.Button(
    root,
    text="Check",
    command=check_guess,
    bg="#F51BC9",
    fg="white",
    relief="raised",
    borderwidth=5
)

feedback_label = tk.Label(
    root,
    text=" ",
    font=("High Tower Text", 13),
    bg="lightblue"
)

root.mainloop()
