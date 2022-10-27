class Category:

    def __init__(self, category):
        self.ledger = list()
        self.withdraw_amount = 0
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
            self.withdraw_amount += amount
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
    total_spend = 0
    chart = 'Percentage spent by category\n'
    max_cat_len = 0

    for c in categories:
        total_spend += c.withdraw_amount
        if len(c.category) > max_cat_len:
            max_cat_len = len(c.category)

    for i in range (10, -1, -1):
        chart += f'{i*10:>3}|'
        for c in categories:
            if int(format(c.withdraw_amount / total_spend, '.2f')[2]) >= i:
                chart += ' o '
            else:
                chart += '   ' 
        chart += ' \n'
    
    chart += f"    {'-'*(len(categories)*3+1)}\n"
    
    for i in range(max_cat_len):
        chart += '    ' 
        for c in categories:
            try:
                chart += f' {c.category[i]} '
            except:
                chart += '   '
        chart += ' \n' if i != max_cat_len - 1 else ' '
    return chart


food = Category('Food')
entertainment = Category('Entertainment')
business = Category('Business')
food.deposit(900, "deposit")
entertainment.deposit(900, "deposit")
business.deposit(900, "deposit")
food.withdraw(105.55)
entertainment.withdraw(33.40)
business.withdraw(10.99)


print(create_spend_chart([business, food, entertainment]))

