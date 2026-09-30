import mysql.connector as mysql
import bcrypt
from datetime import datetime

DB = {
    "host": "localhost",
    "user": "root",
    "password": "Kamal@2007",
    "database": "bank_management"
}

def get_connection():
    return mysql.connect(**DB)

def setup_database():

    connector = get_connection()
    cursor = connector.cursor()

    # Accounts table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            account_no BIGINT PRIMARY KEY AUTO_INCREMENT,
            customer_name VARCHAR(100) NOT NULL,
            phone VARCHAR(15) UNIQUE NOT NULL,
            email VARCHAR(100),
            account_type ENUM('Savings', 'Current') NOT NULL,
            pin_hash VARCHAR(255) NOT NULL,
            balance DECIMAL(12,2) DEFAULT 0.00,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Transactions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id BIGINT PRIMARY KEY AUTO_INCREMENT,
            account_no BIGINT NOT NULL,
            transaction_type ENUM('Deposit', 'Withdrawal') NOT NULL,
            amount DECIMAL(12,2) NOT NULL,
            balance_after DECIMAL(12,2) NOT NULL,
            transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (account_no)
            REFERENCES accounts(account_no)
            ON DELETE CASCADE
        )
    """)

    connector.commit()

    cursor.close()
    connector.close()

def get_non_empty(prompt):

    while True:

        value = input(prompt).strip()         

        if value:
            return value

        print("This field cannot be empty.")


def get_phone():

    while True:

        phone = input("Enter phone number: ").strip()

        if phone.isdigit() and 10 <= len(phone) <= 15:
            return phone

        print("Enter a valid phone number.")


def get_pin():

    while True:

        pin = input("Create 4-digit PIN: ").strip()

        if pin.isdigit() and len(pin) == 4:
            return pin

        print("PIN must contain exactly 4 digits.")


def get_amount(prompt):

    while True:

        try:

            amount = float(input(prompt))

            if amount <= 0:
                print("Amount must be greater than 0.")
                continue

            return amount

        except ValueError:
            print("Please enter a valid amount.")


def create_account():

    print("\n" + "=" * 50)
    print("           CREATE NEW ACCOUNT")
    print("=" * 50)

    name = get_non_empty("Enter customer name: ")

    phone = get_phone()

    email = input("Enter email: ").strip()

    while True:

        account_type = input(
            "Account type (Savings/Current): "
        ).strip().capitalize()

        if account_type in ["Savings", "Current"]:
            break

        print("Please choose Savings or Current.")

    pin = get_pin()

    confirm_pin = input("Confirm PIN: ").strip()

    if pin != confirm_pin:

        print("PIN confirmation does not match.")
        return

    # Hash PIN before storing it
    pin_hash = bcrypt.hashpw(
        pin.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    try:

        connector = get_connection()
        cursor = connector.cursor()

        query = """
            INSERT INTO accounts
            (customer_name, phone, email, account_type, pin_hash)
            VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (
                name,
                phone,
                email,
                account_type,
                pin_hash
            )
        )

        connector.commit()

        account_no = cursor.lastrowid

        print("\nAccount created successfully!")
        print("Account Number:", account_no)
        print("Customer Name:", name)
        print("Account Type:", account_type)

        cursor.close()
        connector.close()

    except mysql.IntegrityError:

        print("An account with this phone number already exists.")

    except mysql.Error as e:

        print("Database error:", e)


def login():

    print("\n" + "=" * 50)
    print("                 LOGIN")
    print("=" * 50)

    try:

        account_no = int(
            input("Enter account number: ")
        )

    except ValueError:

        print("Invalid account number.")
        return None

    pin = input("Enter 4-digit PIN: ").strip()

    try:

        connector = get_connection()
        cursor = connector.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT *
            FROM accounts
            WHERE account_no = %s
            """,
            (account_no,)
        )

        account = cursor.fetchone()

        cursor.close()
        connector.close()

        if not account:

            print("Account not found.")
            return None

        stored_hash = account["pin_hash"]

        if bcrypt.checkpw(
            pin.encode("utf-8"),
            stored_hash.encode("utf-8")
        ):

            print("\nLogin successful!")
            print("Welcome,", account["customer_name"])

            return account_no

        else:

            print("Incorrect PIN.")
            return None

    except mysql.Error as e:

        print("Database error:", e)
        return None

def check_balance(account_no):

    try:

        connector = get_connection()
        cursor = connector.cursor()

        cursor.execute(
            """
            SELECT balance
            FROM accounts
            WHERE account_no = %s
            """,
            (account_no,)
        )

        result = cursor.fetchone()

        cursor.close()
        connector.close()

        if result:

            print("\nCurrent Balance: ₹", result[0])

    except mysql.Error as e:

        print("Database error:", e)

def deposit(account_no):

    print("\n" + "=" * 50)
    print("                  DEPOSIT")
    print("=" * 50)

    amount = get_amount("Enter deposit amount: ₹")

    try:

        connector = get_connection()
        cursor = connector.cursor()

        # Get current balance
        cursor.execute(
            """
            SELECT balance
            FROM accounts
            WHERE account_no = %s
            """,
            (account_no,)
        )

        result = cursor.fetchone()

        if not result:

            print("Account not found.")
            return

        current_balance = float(result[0])

        new_balance = current_balance + amount

        # Update balance
        cursor.execute(
            """
            UPDATE accounts
            SET balance = %s
            WHERE account_no = %s
            """,
            (new_balance, account_no)
        )

        # Record transaction
        cursor.execute(
            """
            INSERT INTO transactions
            (
                account_no,
                transaction_type,
                amount,
                balance_after
            )
            VALUES (%s, 'Deposit', %s, %s)
            """,
            (
                account_no,
                amount,
                new_balance
            )
        )

        connector.commit()

        print("\nDeposit successful!")
        print("Deposited: ₹", amount)
        print("New Balance: ₹", new_balance)

        cursor.close()
        connector.close()

    except mysql.Error as e:

        connector.rollback()
        print("Transaction failed:", e)


def withdraw(account_no):

    print("\n" + "=" * 50)
    print("                WITHDRAW")
    print("=" * 50)

    amount = get_amount("Enter withdrawal amount: ₹")

    try:

        connector = get_connection()
        cursor = connector.cursor()

        # Lock the account row during transaction
        cursor.execute(
            """
            SELECT balance
            FROM accounts
            WHERE account_no = %s
            FOR UPDATE
            """,
            (account_no,)
        )

        result = cursor.fetchone()

        if not result:

            print("Account not found.")
            connector.rollback()
            return

        current_balance = float(result[0])

        # Important safeguard
        if amount > current_balance:

            print("\nInsufficient balance.")
            print("Available Balance: ₹", current_balance)

            connector.rollback()
            cursor.close()
            connector.close()

            return

        new_balance = current_balance - amount

        # Update account balance
        cursor.execute(
            """
            UPDATE accounts
            SET balance = %s
            WHERE account_no = %s
            """,
            (
                new_balance,
                account_no
            )
        )

        # Record transaction
        cursor.execute(
            """
            INSERT INTO transactions
            (
                account_no,
                transaction_type,
                amount,
                balance_after
            )
            VALUES (%s, 'Withdrawal', %s, %s)
            """,
            (
                account_no,
                amount,
                new_balance
            )
        )

        connector.commit()

        print("\nWithdrawal successful!")
        print("Withdrawn: ₹", amount)
        print("Remaining Balance: ₹", new_balance)

        cursor.close()
        connector.close()

    except mysql.Error as e:

        connector.rollback()
        print("Transaction failed:", e)

def account_details(account_no):

    try:

        connector = get_connection()
        cursor = connector.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                account_no,
                customer_name,
                phone,
                email,
                account_type,
                balance,
                created_at
            FROM accounts
            WHERE account_no = %s
            """,
            (account_no,)
        )

        account = cursor.fetchone()

        cursor.close()
        connector.close()

        if not account:

            print("Account not found.")
            return

        print("\n" + "=" * 50)
        print("              ACCOUNT DETAILS")
        print("=" * 50)

        print("Account Number :", account["account_no"])
        print("Customer Name  :", account["customer_name"])
        print("Phone          :", account["phone"])
        print("Email          :", account["email"])
        print("Account Type   :", account["account_type"])
        print("Balance        : ₹", account["balance"])
        print("Created At     :", account["created_at"])

    except mysql.Error as e:

        print("Database error:", e)



def statement(account_no):

    try:

        connector = get_connection()
        cursor = connector.cursor()

        cursor.execute(
            """
            SELECT
                transaction_id,
                transaction_type,
                amount,
                balance_after,
                transaction_date
            FROM transactions
            WHERE account_no = %s
            ORDER BY transaction_date ASC
            """,
            (account_no,)
        )

        transactions = cursor.fetchall()

        cursor.close()
        connector.close()

        print("\n" + "=" * 80)
        print("                         BANK STATEMENT")
        print("=" * 80)

        if not transactions:

            print("No transactions found.")
            return

        print(
            f"{'ID':<8}"
            f"{'TYPE':<15}"
            f"{'AMOUNT':<15}"
            f"{'BALANCE':<15}"
            f"{'DATE':<22}"
        )

        print("-" * 80)

        for transaction in transactions:

            print(
                f"{transaction[0]:<8}"
                f"{transaction[1]:<15}"
                f"₹{float(transaction[2]):<14.2f}"
                f"₹{float(transaction[3]):<14.2f}"
                f"{str(transaction[4]):<22}"
            )

    except mysql.Error as e:

        print("Database error:", e)

def banking_dashboard(account_no):

    while True:

        print("\n")
        print("=" * 50)
        print("             BANKING DASHBOARD")
        print("=" * 50)

        print("1. Check Balance")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Account Details")
        print("5. Transaction Statement")
        print("6. Logout")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":

            check_balance(account_no)

        elif choice == "2":

            deposit(account_no)

        elif choice == "3":

            withdraw(account_no)

        elif choice == "4":

            account_details(account_no)

        elif choice == "5":

            statement(account_no)

        elif choice == "6":

            print("\nLogged out successfully.")
            break

        else:

            print("Invalid choice. Please try again.")


def main():

    print("\n")
    print("=" * 60)
    print("           AUTOMATED BANK MANAGEMENT SYSTEM")
    print("=" * 60)

    try:

        setup_database()

    except mysql.Error as e:

        print("\nUnable to connect to MySQL.")
        print("Check your MySQL username, password and server.")
        print("Error:", e)
        return

    while True:

        print("\n")
        print("=" * 50)
        print("                  MAIN MENU")
        print("=" * 50)

        print("1. Create Account")
        print("2. Login")
        print("3. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":

            create_account()

        elif choice == "2":

            account_no = login()

            if account_no:

                banking_dashboard(account_no)

        elif choice == "3":

            print("\nThank you for using the Bank Management System.")
            break

        else:

            print("Invalid choice. Please select 1, 2 or 3.")

if __name__ == "__main__":
    main()