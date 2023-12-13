# try wrapping the code below that reads a persons.csv file in a class and make it more general such that it can read in any csv file

import csv, os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


# add in code for a Database class
class Database:
    def __init__(self):
        self.__data = {}

    def add(self, table):
        self.__data[table.name] = table

    def search(self, table_name):
        if table_name in self.__data.keys():
            return self.__data[table_name]
        return None

    def __str__(self):
        _str = ''
        for name, data in self.__data.items():
            _str += f"'{name}':{data}\n"
        return _str


# add in code for a Table class
class Table:
    def __init__(self, table_name, data):
        self.name = table_name
        self.table = data

    def insert(self, new_entry: dict):
        self.table += [new_entry]

    def __str__(self):
        _str = ''
        for data in self.table:
            _str += f"{data}\n"
        return _str

    def filter(self, func):
        filtered = []
        for entry in self.table:
            if func(entry):
                filtered += [entry]
        return Table(f"{self.name}_filtered", filtered)

    def select(self, key):
        selected = []
        for entry in self.table:
            new_entry = {}
            for _key in key:
                new_entry[_key] = entry[_key]
            selected += [new_entry]
        return Table(f"{self.name}_selected", selected)


class Reader:
    def read_csv(self, file_name):
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
        data = []
        with open(os.path.join(__location__, file_name)) as f:
            rows = csv.DictReader(f)
            for r in rows:
                data.append(dict(r))
        return data


# modify the code in the Table class so that it supports the insert operation
# where an entry can be added to a list of dictionary

class Project:
    def __init__(self, project_name):
        self.name = project_name
        self.project_details = ''
        self.member = []
        self.vote_status = {}
        self.work_space = {}

    def send_member_request(self, pending_table):
        pending_table.insert([self.name, self])

    def send_advisor_request(self, pending_table):
        pending_table.insert([self.name, self])


# TEST
class TEST:
    def __init__(self):
        reader = Reader()
        self.test_db = Database()
        self.table = Table('person', reader.read_csv('persons.csv'))

    def Test_DB_add(self):
        self.test_db.add(self.table)

    def Test_DB_insert(self):
        self.table.insert({'ID':'6610545481', 'first':'Rattanan', 'last':'Runguthai', 'type':'student'})
        print(self.table)

    def Test_Table_filter(self):
        print(self.table.filter(lambda person: person['type'] == 'faculty'))

    def Test_Table_select(self):
        print(self.table.select(['first', 'last']))

    def Test_Project(self):
        _project = Project('Test')


if __name__ == '__main__':
    Test = TEST()
    Test.Test_DB_add()
    Test.Test_DB_insert()
    Test.Test_Table_filter()
    Test.Test_Table_select()
    Test.Test_Project()
