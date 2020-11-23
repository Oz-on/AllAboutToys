class Database:
    """
    It is a mock of database, which will be replaced in the future by real database
    """
    def __init__(self):
        # For a now sales will be stored in json file, because we don't have any database yet
        self.sales = {
            '1': {
                'name': 'Teddy Bear',
                'quantity_sold': 2340,
                'revenue': 1305580,
            },
            '2': {
                'name': 'Lego Fire Station',
                'quantity_sold': 24,
                'revenue': 1305,
            },
        }

        self.users = [('oskar', 'od7794j'), ('ozon', 'zpojf')]

    def get_sales(self):
        return self.sales

    def check_password(self, username, password):
        for user in self.users:
            if username == user[0] and password == user[1]:
                return True


class SaleReport:
    """
    It represents sale report
    """
    def __init__(self):
        db = Database()
        self.data = db.get_sales()

    def export_to_csv(self, file_name):
        # Open given file
        with open(file_name, 'w') as file:
            # Write first line for labeling
            file.write('name;quantity_sold;revenue\n')
            # For every record in database
            for key in self.data:
                name = self.data[key]['name']
                quantity_sold = self.data[key]['quantity_sold']
                revenue = self.data[key]['revenue']
                file.write(f'{name};{quantity_sold};{revenue}\n')


class Authentication:
    def __init__(self):
        self.is_authenticated = False
        self.token = None
        self.db = Database()

    def login(self, username, password):
        # It logs in the user
        is_correct = self.db.check_password(username, password)
        if is_correct:
            print('user is logged in')
        else:
            print('Incorect credentials!')


