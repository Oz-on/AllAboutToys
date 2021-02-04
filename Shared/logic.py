# This file contains all classes used in many features
# If you add sth to this file feel free to add yourselves as authors
# Authors: Oskar Domingos, Marceli Skorupski
import json
import sqlite3
from SalesFeature.Discounts.models import DiscountScheme


class DB:
    """
    This class has all methods related to Database handling.
    For now, there is no database, so all operations are performed on json file
    """
    def __init__(self):
        self._db_name = 'Database.db'

        # Sales list holds every data related to sales
        self._sales = []

        self.__fetch_sales()

    @staticmethod
    def initialize_db(db_name):
        """
        It creates tables that are necessary to ensure that app will be working correctly
        :return:
        """
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Create table for sales
        # cursor.execute('''CREATE TABLE IF NOT EXISTS sale(
        #     id INTEGER PRIMARY KEY AUTOINCREMENT,
        #     product_id INTEGER NOT NULL,
        #     category_id INTEGER NOT NULL,
        #     quantity INTEGER NOT NULL,
        #     receipt_id INTEGER NOT NULL,
        #     receipt_date TEXT
        # )''')
        #
        # # Create table for requests
        # cursor.execute('''CREATE TABLE IF NOT EXISTS request(
        #     id INTEGER PRIMARY KEY AUTOINCREMENT,
        #     replied_on INTEGER,
        #     request_type TEXT,
        #     user_id INTEGER,
        #     content TEXT)
        # ''')
        #
        # # Create table for replies
        # cursor.execute('''CREATE TABLE IF NOT EXISTS request_reply(
        #     id INTEGER PRIMARY KEY AUTOINCREMENT,
        #     request_id INTEGER,
        #     user_id INTEGER,
        #     content TEXT)
        # ''')
        #
        # # Create table for discounts schemes
        # cursor.execute('''
        #     CREATE TABLE IF NOT EXISTS discount_scheme(
        #         id INTEGER PRIMARY KEY,
        #         details TEXT,
        #         discount_percentage REAL)
        # ''')

        # Insert some data
        # Create users
        # cursor.execute('''INSERT INTO user(firstname, lastname, username, password) VALUES("John", "Doe", "johndoe", "johndoe1");''')
        # cursor.execute('''INSERT INTO user(firstname, lastname, username, password) VALUES("Alberto", "Rahim", "albi", "zaqtyui");''')
        # Create requests
        cursor.execute('''INSERT INTO request(request_type, user_id, content, replied_on) VALUES("review", 1, "This product is a crap", 0);''')
        cursor.execute('''INSERT INTO request(request_type, user_id, content, replied_on) VALUES("query", 2, "Can I have a refund?", 0);''')

        conn.commit()
        conn.close()

    def __fetch_sales(self):
        """
        Author: Oskar Domingos
        It takes sales from file and wrap in appropriate data structure
        :return:
        """

        with open('./Shared/sales.json', 'r') as file:
            self._sales = json.load(file)
            self._sales = self._sales['orders']
            print(self._sales)
            # Map sales list to have appropriate fields
            for i in range(len(self._sales)):
                sale = self._sales[i]
                category = {
                    "id": sale['category_id'],
                    "name": sale['category_name'],
                }
                product = {
                    "id": sale['product_id'],
                    "name": sale['product_name'],
                    "cost": sale['product_cost'],
                    "category": category,
                }
                self._sales[i]['product'] = product
                self._sales[i]['category'] = category

                del self._sales[i]['product_id']
                del self._sales[i]['product_name']
                del self._sales[i]['product_cost']
                del self._sales[i]['category_id']
                del self._sales[i]['category_name']

    def fetch_requests(self):
        """
        Author: Oskar Domingos
        It takes requests from database and wrap in appropriate data structure
        :return list of requests which are dictionaries:
        """
        conn = sqlite3.connect(self._db_name)
        cursor = conn.cursor()

        requests = []
        for row in cursor.execute('''SELECT request.id, request.request_type, Users.username, Users.ID_number, request.content FROM request INNER JOIN 
        Users ON request.user_id=Users.ID_number WHERE request.replied_on=0'''):
            request = {
                'id': row[0],
                'request_type': row[1],
                'username': row[2],
                'user_id': row[3],
                'content': row[4],
            }
            requests.append(request)

        conn.close()

        return requests

    def add_request_reply(self, request, content):
        """
        Author: Oskar Domingos
        It adds reply to a request
        :return:
        """
        conn = sqlite3.connect(self._db_name)
        cursor = conn.cursor()

        cursor.execute(
            '''INSERT INTO request_reply(request_id, user_id, content) VALUES(?, ?, ?)''',
            (request.request_id, request.author.user_id, content,)
        )
        cursor.execute(
            '''UPDATE request SET replied_on=1 WHERE id=?''',
            (request.request_id,)
        )

        conn.commit()
        conn.close()

        return request.request_id

    def fetch_discounts_schemes(self):
        """
        Author: Oskar Domingos
        It takes discount schemes from database and wrap in appropriate data structure
        :return list of discount schemes:
        """
        conn = sqlite3.connect(self._db_name)
        cursor = conn.cursor()

        discounts_schemes = []
        for row in cursor.execute('''SELECT discount_scheme.id, discount_scheme.details, discount_scheme.discount_percentage FROM discount_scheme'''):
            discounts_schemes.append(DiscountScheme(
                discount_scheme_id=row[0],
                details=row[1],
                discount_percentage=row[2],
            ))

        conn.close()
        return discounts_schemes

    def edit_discount_scheme(self, discount_scheme):
        """
        Author: Oskar Domingos
        It edits discount scheme
        :param discount_scheme:
        :return:
        """
        conn = sqlite3.connect(self._db_name)
        cursor = conn.cursor()

        cursor.execute(
            '''UPDATE discount_scheme SET details=?, discount_percentage=? WHERE id=?''',
            (discount_scheme.details, discount_scheme.discount_percentage, discount_scheme.discount_scheme_id)
        )

        conn.commit()
        conn.close()

    def add_discount_scheme(self, discount_scheme):
        """
        Author: Oskar Domingos
        :param discount_scheme:
        :return:
        """
        conn = sqlite3.connect(self._db_name)
        cursor = conn.cursor()

        # Check if record with that id already exists
        cursor.execute('''SELECT id FROM discount_scheme WHERE id=?''', (discount_scheme.discount_scheme_id,))
        result = cursor.fetchone()
        print(result)

        if result is not None:
            return False
        else:
            cursor.execute(
                '''INSERT INTO discount_scheme(id, details, discount_percentage) VALUES(?,?,?)''',
                (discount_scheme.discount_scheme_id, discount_scheme.details, discount_scheme.discount_percentage)
            )
            conn.commit()
            conn.close()
            return True

    def remove_discount_scheme(self, discount_scheme):
        """
        Author: Oskar Domingos
        IT removes discount scheme from database
        :param discount_scheme:
        :return:
        """

        conn = sqlite3.connect(self._db_name)
        cursor = conn.cursor()

        cursor.execute(
            '''DELETE FROM discount_scheme WHERE id=?''',
            (discount_scheme.discount_scheme_id,)
        )

        conn.commit()
        conn.close()

    def SetMaxPos(self, tbl):
        conn = self.create_connection()
        cur = conn.cursor()
        maxpos = 0
        if tbl == 'Products':
            cur.execute('SELECT * FROM Products ')
            res = cur.fetchall()
            # print(res)
            for rec in res:
                maxpos = maxpos + 1

            self.close_connection(conn)
            return maxpos



        elif tbl == 'Categories':
            cur.execute('SELECT * FROM Categories')
            res = cur.fetchall()
            # print(res)
            for rec in res:
                maxpos = maxpos + 1

            self.close_connection(conn)
            return maxpos

    def FetchData(self, pos, tbl):
        conn = self.create_connection()
        cur = conn.cursor()
        if tbl == 'Products':
            cur.execute("SELECT rowid, * FROM Products WHERE rowid = '%s' " % pos)
            todisplay = cur.fetchall()
            self.close_connection(conn)
            return (todisplay[0])[1:]

        elif tbl == 'Categories':
            cur.execute("SELECT rowid, * FROM Categories WHERE rowid = '%s' " % pos)
            todisplay = cur.fetchall()
            self.close_connection(conn)
            return (todisplay[0])[1:]

    def del_record(self, position, tbl):
        conn = self.create_connection()
        cur = conn.cursor()

        if tbl == 'Products':
            cur.execute(' Delete from Products WHERE Product_code = (?) ', position)
            cur.execute("CREATE TABLE Products_Temp AS SELECT * FROM Products")
            cur.execute("DELETE FROM Products")
            cur.execute("DELETE FROM sqlite_sequence WHERE name='Products.'")
            cur.execute("INSERT INTO Products SELECT * FROM Products_Temp")
            cur.execute("DROP TABLE Products_Temp")
            self.close_connection(conn)
        elif tbl == 'Categories':
            cur.execute('Delete from Categories WHERE Cat_Code = (?) ', position)
            cur.execute("CREATE TABLE Categories_Temp AS SELECT * FROM Categories")
            cur.execute("DELETE FROM Categories")
            cur.execute("DELETE FROM sqlite_sequence WHERE name='Categories'")
            cur.execute(" INSERT INTO Categories (name) SELECT name FROM Categories_Temp")
            cur.execute("DROP TABLE Categories_Temp")
            self.close_connection(conn)

    def login_check(self, username, password):
        UNPS = [(username, password)]
        conn = self.create_connection()
        cur = conn.cursor()
        cur.execute('SELECT username, password FROM Users ')
        result = cur.fetchall()
        # print(result)
        for row in result:
            # print(row)
            if row == UNPS[0]:
                final = True
            else:
                final = False

        self.close_connection(conn)

        return final

    def fetchvaluesCatName(self):
        conn = self.create_connection()
        cur = conn.cursor()
        values = []
        cur.execute('SELECT name FROM Categories')
        result = cur.fetchall()
        for row in result:
            # print(row)
            for item in row:
                # print(item)
                values.append(item)
        # print(values)
        self.close_connection(conn)
        return values

    def save(self, table, newid, newname, newdesc, newcatcode, newqty):
        conn = self.create_connection()
        cur = conn.cursor()
        cur.execute(""" INSERT OR REPLACE INTO Products VALUES (? , ? , ? , ? , ?)""",
                    (newid, newname, newdesc, newcatcode, newqty))
        cur.execute("CREATE TABLE Products_Temp AS SELECT * FROM Products")
        cur.execute("DELETE FROM Products")
        cur.execute("DELETE FROM sqlite_sequence WHERE name='Products'")
        cur.execute("INSERT INTO Products SELECT * FROM Products_Temp")
        cur.execute("DROP TABLE Products_Temp")
        self.close_connection(conn)

    def saveCat(self, table, newid, newname):
        conn = self.create_connection()
        cur = conn.cursor()
        cur.execute(""" INSERT OR REPLACE INTO Categories VALUES (? , ? )""", (newid, newname,))
        cur.execute("CREATE TABLE Categories_Temp AS SELECT * FROM Categories")
        cur.execute("DELETE FROM Categories")
        cur.execute("DELETE FROM sqlite_sequence WHERE name='Categories'")
        cur.execute(" INSERT INTO Categories (name) SELECT name FROM Categories_Temp")
        # cur.execute("INSERT INTO Categories SELECT * FROM Categories_Temp")
        cur.execute("DROP TABLE Categories_Temp")
        self.close_connection(conn)

    def set_rec_pos(self, recid, table):
        conn = self.create_connection()
        cur = conn.cursor()
        if table == 'Categories':
            cur.execute("SELECT rowid, * FROM Categories WHERE Cat_Code = {0} ".format(recid))
            newpos_ = cur.fetchall()
            self.close_connection(conn)
        elif table == 'Products':
            cur.execute("SELECT rowid, * FROM Products WHERE Product_Code = {0} ".format(recid))
            newpos_ = cur.fetchall()
            self.close_connection(conn)

        return ((newpos_[0])[0])

    def setSRdata(self):
        conn = self.create_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM Products ')
        SRdict = cur.fetchall()
        # print(SRdict)
        return SRdict

    def setLSData(self):
        conn = self.create_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Products WHERE Qty <= 5 ")
        LSDict = cur.fetchall()
        return LSDict

    def LoworNot(self):
        conn = self.create_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Products WHERE Qty <= 5 ")
        LSDict = cur.fetchall()
        if LSDict == []:
            return False
        else:
            return True

    # Connect
    def create_connection(self,):
        conn = sqlite3.connect('Database.db')
        return conn

    def close_connection(self, conn):
        conn.commit()
        conn.close()

    @property
    def sales(self):
        return self._sales


class Authentication:
    def __init__(self):
        self.is_authenticated = False
        self.token = None
        self.db = DB()

    def login(self, username, password):
        # It logs in the user
        is_correct = self.db.check_password(username, password)
        if is_correct:
            print('user is logged in')
        else:
            print('Incorect credentials!')