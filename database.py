# try wrapping the code below that reads a persons.csv file in a class and make it more general such that it can read in any csv file

import csv, os, random

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

class Project:
    def __init__(self, project_name, id):
        self.id = str(random.randint(100000,999999))
        self.name = project_name
        self.project_details = ''
        self.lead_student = id
        self.member1 = ''
        self.member2 = ''
        self.advisor = ''
        self.status = 'Declined'
        self.vote_status = ''
        self.invite1 = ''
        self.invite2 = ''
        self.invite_advisor = ''

    def save(self):
        return [self.id, self.name, self.project_details, self.lead_student, self.member1, self.member2,
                self.advisor, self.status, self.vote_status, self.invite1, self.invite2, self.invite_advisor]

    def __fit_text_to_screen(self,txt):
        txt = txt.split()
        new_txt = ''
        while len(txt) != 0:
            if len(txt) < 10:
                new_txt += ' '.join(txt[:len(txt)])
                txt = []
            else:
                new_txt += ' '.join(txt[:10])
                txt = txt[10:]
            new_txt += '\n'
        return new_txt

    def __str__(self):
        vote = [vote.split()[1] for vote in self.vote_status.split(':')[1:]]

        _inv_mem_1_str = ''
        _inv_mem_2_str = ''
        _inv_adv_str = ''

        if self.invite1 != '':
            _inv_mem_1_str = f"{self.invite1.split(':')[0]} ({self.invite1.split(':')[1]})"
        if self.invite2 != '':
            _inv_mem_2_str = f"{self.invite2.split(':')[0]} ({self.invite2.split(':')[1]})"
        if self.invite_advisor != '':
            _inv_adv_str = f"{self.invite_advisor.split(':')[0]} ({self.invite_advisor.split(':')[1]})"

        return (f"Project ID : {self.id}\n"
                f"Project name : {self.name}\n"
                f"Project Details : \n{self.__fit_text_to_screen(self.project_details)}\n"
                f"Lead student : {self.lead_student}\n"
                f"Member 1 : {self.member1}\n"
                f"Member 2 : {self.member2}\n"
                f"Advisor : {self.advisor}\n"
                f"Status : {self.status}\n"
                f"Vote Status : "
                f"{vote.count('1')} Approves, "
                f"{vote.count('0')} Disapproves\n"
                f"\n"
                f"Member 1 invite : {_inv_mem_1_str}\n"
                f"Member 2 invite : {_inv_mem_2_str}\n"
                f"Advisor invite  : {_inv_adv_str}\n")



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

    def get_data(self):
        return self.__data


# add in code for a Table class
class Table:
    def __init__(self, table_name, data):
        self.name = table_name
        self.table = data

    def insert(self, new_entry: dict):
        self.table += [new_entry]

    def __str__(self):
        if isinstance(self.table[0], Project):
            _keys = ['project_id','project_name','project_details',
                     'lead_student','member1','member2','advisor','status','vote_status',
                     'invite1','invite2','invite_advisor']

            padding = [13,15,20,15,10,10,10,11,14,10,10,17]

            for key, pad in zip(['#'] + _keys, [3] + padding):
                print(f"|{key:<{pad}}|", end='')
            print()
            print('-' * (sum(padding) + 5 + 2 * len(_keys)))
            _str = ''

            for index, project in enumerate(self.table):
                project_data = project.save()
                if project.vote_status != '':
                    _vote_str = project_data[8].strip(":").split(':')
                    _vote_str = [vote.split()[1] for vote in _vote_str]
                    _vote_str = ' '.join(_vote_str)
                    project_data[7] = _vote_str

                if project.invite1 != '':
                    _inv_mem_1_str = project.invite1.split(':')[0]
                    project_data[9] = _inv_mem_1_str
                if project.invite2 != '':
                    _inv_mem_2_str = project.invite2.split(':')[0]
                    project_data[10] = _inv_mem_2_str
                if project.invite_advisor != '':
                    _inv_adv_str = project.invite_advisor.split(':')[0]
                    project_data[11] = _inv_adv_str

                _str += f"|{index + 1:<3}|"
                for val, pad in zip(project_data, padding):
                    if len(val) > pad-3:
                        val = val[:pad-3] + '...'
                    _str += f"|{val:<{pad}}|"
                _str += '\n'
            return _str

        table_keys = list(self.table[0].keys())
        padding = [self.aggregate(len, lambda x: max(x) + 2, key) for key in table_keys]
        table_keys.insert(0, '#')

        for key, pad in zip(table_keys, [3] + padding):
            print(f"|{key:<{pad}}|", end='')
        print()
        print('-' * (sum(padding) + 3 + 2*len(table_keys)))
        _str = ''
        for index, entry in enumerate(self.table):
            _str += f"|{index + 1:<3}|"
            for val, pad in zip(entry.values(), padding):
                _str += f"|{val:<{pad}}|"
            _str += '\n'
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

    def aggregate(self, function1, function, aggregation_key):
        temps = []
        for item in self.table:
            temps += [function1(item[aggregation_key])]
        return function(temps)


class Reader:
    def read_csv(self, file_name):
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
        data = []
        with open(os.path.join(__location__, file_name)) as f:
            rows = csv.DictReader(f)
            for r in rows:
                data.append(dict(r))
        f.close()
        return data


# modify the code in the Table class so that it supports the insert operation
# where an entry can be added to a list of dictionary


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

    def Test_Project_table_print(self):
        reader = Reader()
        project_data = reader.read_csv('projects.csv')
        project = []
        for _project in project_data:
            load_project = Project(_project['project_name'], _project['lead_student'])
            load_project.project_details = _project['project_details']
            load_project.member1 = _project['member1']
            load_project.member2 = _project['member2']
            load_project.advisor = _project['advisor']
            load_project.status = _project['status']
            load_project.vote_status = _project['vote_status']
            load_project.invite1 = _project['invite1']
            load_project.invite2 = _project['invite2']
            load_project.invite_advisor = _project['invite_advisor']
            project += [load_project]
        project = Table('project', project)
        print(project)

    def Test_Project_print(self):
        reader = Reader()
        project_data = reader.read_csv('projects.csv')
        _project = project_data[0]
        load_project = Project(_project['project_name'], _project['lead_student'])
        load_project.project_details = _project['project_details']
        load_project.member1 = _project['member1']
        load_project.member2 = _project['member2']
        load_project.advisor = _project['advisor']
        load_project.status = _project['status']
        load_project.vote_status = _project['vote_status']
        load_project.invite1 = _project['invite1']
        load_project.invite2 = _project['invite2']
        load_project.invite_advisor = _project['invite_advisor']
        project = load_project

        print(project)


if __name__ == '__main__':
    Test = TEST()
    Test.Test_DB_add()
    Test.Test_DB_insert()
    Test.Test_Table_filter()
    Test.Test_Table_select()
    Test.Test_Project_table_print()
    Test.Test_Project_print()



