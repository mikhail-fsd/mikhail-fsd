class Category:

    def __init__(self, category):
        self.ledger = list()
        self.balance = 0
        self.category = category

    def __str__(self):
        bill = f'{self.category:*^30}\n'
        for record in self.ledger:
            bill += f"{record['description'][:23]:<24}{format(float(record['amount']), '.2f')}\n"
        bill += f'Total: {self.balance}' 
        
        return bill 

        
    def deposit(self, amount, discription=''):
        self.ledger.append({'amount': amount, 'description':discription})
        self.balance += amount

    def withdraw(self, amount, discription=''):
        if self.balance > amount:
            self.ledger.append({'amount': -amount, 'description':discription})
            self.balance -= amount
            return True
        else:
            return False

    def get_balance(self):
        return self.balance

    def transfer(self, transfer_amount, destionation_category):
        if self.balance > transfer_amount:
            transfer_description_withdraw= f'Transfer to {destionation_category.category}'
            self.withdraw(transfer_amount, transfer_description_withdraw)

            transfer_description_deposit = f'Transfer from {self.category}'
            destionation_category.deposit(transfer_amount, transfer_description_deposit)
            return True
        return False

    def check_funds(self, amount):
        if self.balance >= amount:
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

print()
print(food)
#self.assertEqual(actual, expected, 'Expected balance to be 854.33')

