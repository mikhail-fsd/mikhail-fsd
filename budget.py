class Category:

    def __init__(self, category):
        self.ledger = list()
        self.balance = 0
        self.category = category


    def deposit(self, amount, discription=''):
        dep = {'amount': amount, 'description':discription}
        self.ledger.append(dep)

    def withdraw(self, amount, discription=''):
        if self.get_balance() > amount:
            dep = {'amount': -amount, 'description':discription}
            self.ledger.append(dep)
            return True
        else:
            return False

    def get_balance(self):
        balance = 0
        for record in self.ledger:
            balance += record['amount']
        self.balance = balance
        return self.balance

    def transfer(self, transfer_amount, destionation_category):
        if self.get_balance() > transfer_amount:
            transfer_description_withdraw= f'Transfer to {destionation_category.category}'
            self.withdraw(transfer_amount, transfer_description_withdraw)

            transfer_description_deposit = f'Transfer from {self.category}'
            destionation_category.deposit(transfer_amount, transfer_description_deposit)
            return True
        return False

    def check_funds(self, amount):
        if self.get_balance() >= amount:
            return True
        else:
            return False
        


def create_spend_chart(categories):
        pass


food = Category('Food')
food.deposit(900, "deposit")
print(food.ledger)
print()
food.withdraw(45.67, "milk, cereal, eggs, bacon, bread")
print(food.ledger)
print()

print(food.get_balance())
print(food.ledger)

#self.assertEqual(actual, expected, 'Expected balance to be 854.33')

