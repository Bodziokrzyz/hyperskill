import random
import sqlite3

random.seed()

conn = sqlite3.connect("card.s3db")
cur = conn.cursor()
conn.commit()


def generate_account_number():
    global account_number, card_pin
    bank_id = "400000"
    account_id = str(random.randint(99999999, 1000000000))
    calc_checksum = bank_id + account_id
    calc_checksum = [int(i) for i in calc_checksum]
    for i in range(0, 15, 2):
        calc_checksum[i] *= 2
    for i in range(15):
        if calc_checksum[i] > 9:
            calc_checksum[i] -= 9
    checksum = str(sum(calc_checksum * 9))
    checksum = str(int(checksum[len(checksum) - 1]))
    account_number = bank_id + account_id + checksum
    card_pin = format(random.randint(0000, 9999), '04d')
    cur.execute("INSERT INTO card (number, pin, balance) VALUES (?,?,?)", (account_number, card_pin, 0))
    conn.commit()
    print(f"\nYour card have been created\nYour card number:\n{account_number}\nYour card PIN:\n{card_pin}")


def log_into_account():
    global account_number, card_pin
    c_number = input("Enter your card number:")
    pin_number = input("Enter your PIN:")
    card_db = str(cur.execute("SELECT number FROM card").fetchall())
    pin_db = str(cur.execute(f'SELECT pin FROM card WHERE number = {c_number}').fetchall())
    if c_number in card_db:
        if pin_number in pin_db:
            account_number = c_number
            card_pin = pin_number
            print("You have successfully logged in!")
            logged_in_menu()
        else:
            print('Wrong card number or PIN!')
    else:
        print('Wrong card number or PIN!')


def ext():
    print("Bye!")
    exit()


def close_account():
    cur.execute(f'DELETE FROM card WHERE number = {account_number}')
    conn.commit()
    print('The account has been closed!')
    logged_in_menu()


def add_income():
    income_to_add = input("Enter income:")
    cur.execute("UPDATE card SET balance = balance + ? WHERE number = ?", (income_to_add, account_number))
    conn.commit()
    print("Income was added!")
    logged_in_menu()


def balance():
    x = cur.execute(f"SELECT balance FROM card WHERE number = {account_number}")
    conn.commit()
    print(f"Balance: {x}")
    logged_in_menu()


def log_out():
    print("You have successfully logged out!")
    first_menu()


def luhn_transfer_check(x):
    checking_card = list(x)
    last = checking_card[-1]
    del checking_card[-1]
    for i in range(0, len(checking_card)):
        checking_card[i] = int(checking_card[i])
    for i in range(0, len(checking_card), 2):
        checking_card[i] *= 2
    for i in range(0, len(checking_card)):
        if checking_card[i] > 9:
            checking_card[i] -= 9
    digits_sum = sum(checking_card) + int(last)
    if digits_sum % 10 == 0:
        return True


def if_in_db(num):
    cur.execute("SELECT number FROM card")
    res = cur.fetchall()
    if (num,) in res:
        return True
    else:
        return False


def transfer():
    print("""
Transfer
Enter card number:""")
    t_number = input()
    if t_number == account_number:
        print("You can't transfer money to the same account!")
        logged_in_menu()
    elif luhn_transfer_check(t_number) is True:
        if if_in_db(t_number) is True:
            money_to_transfer = int(input("Enter how much money you want to transfer:"))
            account_balance = cur.execute(f"SELECT balance FROM card WHERE number = {account_number}").fetchone()
            conn.commit()
            if (money_to_transfer,) > account_balance:
                print("Not enough money!")
                logged_in_menu()
            elif (money_to_transfer,) < account_balance:
                cur.execute(f"UPDATE card SET balance = balance - {money_to_transfer} WHERE number = {account_number}")
                cur.execute(f"UPDATE card SET balance = balance + {money_to_transfer} WHERE number = {t_number}")
                conn.commit()
                print("Success!")
                logged_in_menu()
        elif if_in_db(t_number) is False:
            print("Such a card does not exist.")
            logged_in_menu()
    else:
        print("Probably you made mistake in the card number.\nPlease try again!")
        logged_in_menu()


def first_menu():
    print("""
1. Create an account
2. Log into account
0. Exit""")
    cur.execute('''
        CREATE TABLE IF NOT EXISTS card (
        id INTEGER PRIMARY KEY,
        number TEXT,
        pin TEXT,
        balance INTEGER DEFAULT 0
        );
        ''')
    conn.commit()
    user_input = int(input())
    if user_input == 1:
        generate_account_number()
    elif user_input == 2:
        log_into_account()
    elif user_input == 0:
        print("Bye!")
        ext()


def logged_in_menu():
    print("""
1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit""")
    logged_in_input = int(input())
    if logged_in_input == 1:
        balance()
    elif logged_in_input == 2:
        add_income()
    elif logged_in_input == 3:
        transfer()
    elif logged_in_input == 4:
        close_account()
    elif logged_in_input == 5:
        log_out()
    elif logged_in_input == 0:
        print("Bye!")
        ext()


while True:
    first_menu()
