import csv

class Account:
    def __init__(self, name, balance):
        self.name = name
        self.balance = float(balance)
    
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return True
        return False

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            return True
        return False

    def get_balance(self):
        return self.balance

class Bank:
    def __init__(self):
        self.accounts = {}
        self.log = []
    
    def create_account(self, name, starting_balance):
        if name in self.accounts:
            return False
        self.accounts[name] = Account(name, starting_balance)
        self.log.append(('CREATE', name, starting_balance))
        return True

    def deposit(self, name, amount):
        account = self.accounts.get(name)
        if account and account.deposit(amount):
            self.log.append(('DEPOSIT', name, amount))
            return True
        return False

    def withdraw(self, name, amount):
        account = self.accounts.get(name)
        if account and account.withdraw(amount):
            self.log.append(('WITHDRAW', name, amount))
            return True
        return False

    def transfer(self, from_name, to_name, amount):
        from_acc = self.accounts.get(from_name)
        to_acc = self.accounts.get(to_name)
        if from_acc and to_acc and from_acc.withdraw(amount):
            to_acc.deposit(amount)
            self.log.append(('TRANSFER', from_name, to_name, amount))
            return True
        return False

    def check_balance(self, name):
        account = self.accounts.get(name)
        if account:
            return account.get_balance()
        return None

    def save_log_to_csv(self, filename):
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            for entry in self.log:
                writer.writerow(entry)
    
    def load_log_from_csv(self, filename):
        self.log = []
        with open(filename, 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                self.log.append(tuple(row))

    def save_accounts_to_csv(self, filename):
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['name', 'balance'])
            for name, acc in self.accounts.items():
                writer.writerow([name, acc.get_balance()])

    def load_accounts_from_csv(self, filename):
        self.accounts = {}
        with open(filename, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                name = row['name']
                balance = float(row['balance'])
                self.accounts[name] = Account(name, balance)

    def show_log(self):
        if not self.log:
            print("System log is empty.")
            return
        print("\n--- System Log ---")
        for idx, entry in enumerate(self.log, start=1):
            print(f"{idx}. {entry}")
        print("------------------")

def main():
    bank = Bank()
    while True:
        print("\n1. Create account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transfer")
        print("5. Check balance")
        print("6. Show system log")
        print("7. Save/Load log")
        print("8. Save/Load accounts")
        print("9. Exit")
        choice = input("Choose: ").strip()
        if choice == '1':
            name = input("Name: ")
            bal = float(input("Starting balance: "))
            if bank.create_account(name, bal):
                print("Account created.")
            else:
                print("Account exists.")
        elif choice == '2':
            name = input("Name: ")
            amt = float(input("Amount: "))
            if bank.deposit(name, amt):
                print("Deposited.")
            else:
                print("Deposit failed.")
        elif choice == '3':
            name = input("Name: ")
            amt = float(input("Amount: "))
            if bank.withdraw(name, amt):
                print("Withdrawn.")
            else:
                print("Withdraw failed (insufficient funds?).")
        elif choice == '4':
            from_name = input("From: ")
            to_name = input("To: ")
            amt = float(input("Amount: "))
            if bank.transfer(from_name, to_name, amt):
                print("Transferred.")
            else:
                print("Transfer failed.")
        elif choice == '5':
            name = input("Account name: ")
            balance = bank.check_balance(name)
            if balance is not None:
                print(f"Balance for {name}: {balance}")
            else:
                print("Account not found.")
        elif choice == '6':
            bank.show_log()
        elif choice == '7':
            sub_choice = input("Enter 'save' to save log or 'load' to load log: ").strip().lower()
            fname = "system log"
            if sub_choice == 'save':
                bank.save_log_to_csv(fname)
                print("Log saved.")
            elif sub_choice == 'load':
                bank.load_log_from_csv(fname)
                print("Log loaded.")
            else:
                print("Invalid option.")
        elif choice == '8':
            sub_choice = input("Enter 'save' to save accounts or 'load' to load accounts: ").strip().lower()
            fname = "account state"
            if sub_choice == 'save':
                bank.save_accounts_to_csv(fname)
                print("Accounts saved.")
            elif sub_choice == 'load':
                bank.load_accounts_from_csv(fname)
                print("Accounts loaded.")
            else:
                print("Invalid option.")
        elif choice == '9':
            break

if __name__ == '__main__':
    main()