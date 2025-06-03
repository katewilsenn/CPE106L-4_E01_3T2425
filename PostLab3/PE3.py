"""
File: savingsaccount.py
This module defines the SavingsAccount class.
"""

class SavingsAccount:
    RATE = 0.02

    def __init__(self, name, pin, balance=0.0):
        self.name = name
        self.pin = pin
        self.balance = float(balance)

    def __str__(self):
        result = f"Name:    {self.name}\n"
        result += f"PIN:     {self.pin}\n"
        result += f"Balance: {self.balance:.1f}"
        return result


class Bank:
    def __init__(self, accounts=None):
        self.accounts = accounts if accounts else []

    def addAccount(self, account):
        self.accounts.append(account)

    def __str__(self):
        # Sort accounts by name before printing
        sorted_accounts = sorted(self.accounts, key=lambda a: a.name)
        return "\n\n".join(str(account) for account in sorted_accounts)


def createBank():
    # Hardcoded data to simulate reading from file
    data = [
        ("Ranie", "0824", 500),
        ("Aliyah", "0312", 999),
        ("Kara", "0917", 894)
    ]
    bank = Bank()
    for name, pin, balance in data:
        account = SavingsAccount(name, pin, balance)
        bank.addAccount(account)
    return bank


def main():
    bank = createBank()
    print("Accounts in sorted order:\n")
    print(bank)


if __name__ == "__main__":
    main()