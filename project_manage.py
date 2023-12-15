# import database module
from database import *
import random
import sys

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

class Application:
    def __init__(self):
        self.__username = ''
        self.__id = ''

    def Start_Application(self):
        while True:
            user = self.Login_Prompt()
            self.Login(user)

    # define a function called login
    def Login_Prompt(self):
        '''here are things to do in this function:
            add code that performs a login task
            ask a user for a username and password
            returns [ID, role] if valid, otherwise returning None'''
        _username = input("Enter Username: ")
        _password = input("Enter Password: ")
        Login = DB.search('login').table
        for credentials in Login:
            if _username == credentials['username'] and _password == credentials['password']:
                self.__username = _username
                self.__id = credentials['ID']
                return [credentials['ID'], credentials['role']]
        return None

    def Show_Menu(self, menu_choice):
        self.clear_screen()
        print(f"Hello, {self.__username}!")
        print(menu_choice)

    def Login(self,val):
        if val[1] == 'advisor':
            self.advisor_run()
        elif val[1] == 'student':
            self.student_run()
        elif val[1] == 'faculty':
            self.faculty_run()
        elif val[1] == 'admin':
            self.admin_run()

    def admin_run(self):
        menu_choice = (f"1. Insert a new entry\n"
                       f"2. Remove an entry\n"
                       f"Q. Logout")
        while True:
            self.Show_Menu(menu_choice)
            response = input()
            if response == '1':
                self.admin_insert()
            elif response == '2':
                self.admin_remove()
            elif response == 'Q':
                exit()
            else:
                print("Invalid response")


    def student_run(self):
        menu_choice = (f"1. Create a project\n"
                       f"2. Invite member to project\n"
                       f"3. Remove member from project\n"
                       f"4. Edit project\n"
                       f"5. Send advisor request\n"
                       f"6. Submit project\n"
                       f"7. Accept project invitation\n"
                       f"Q. Logout\n")
        while True:
            self.Show_Menu(menu_choice)
            response = input()
            if response == '1':
                self.Create_Project()
            elif response == '2':
                self.Invite_member()
            elif response == '3':
                self.Remove_member()
            elif response =='4':
                self.Edit_project()



            elif response == 'Q':
                exit()
            else:
                print("Invalid response")

    def member_student_run(self):
        pass


    def advisor_run(self):
        while True:
            pass


    def faculty_run(self):
        pass


    def admin_insert(self):
        all_table = DB.get_data()
        print("Which table do you want to add entry to?")
        for index,table in enumerate(all_table):
            print(f"{index+1}. {table}")
        response = int(self.take_input('', lambda x: int(x)-1 in range(len(all_table)))) - 1
        print(f"Adding entry to {list(all_table.keys())[response]}")
        table_keys = DB.search(list(all_table.keys())[response]).table[0].keys()
        while True:
            self.clear_screen()
            new_entry_input = input(f"Keys     : {list(table_keys)}\n"
                              f"New entry: ")
            entry = {}
            if len(new_entry_input.split(',')) != len(table_keys):
                print("Invalid entry")
            else:
                print("Your new entry is: ")
                new_entry_str = "{"
                for key,val in zip(table_keys, new_entry_input.split(',')):
                    new_entry_str += f"{key.strip()} : {val.strip()}, "
                    entry[key] = val
                new_entry_str = new_entry_str[:-1] + "}"
                print(new_entry_str)

                confirm = self.take_input("Confirm? (Y/N): ",lambda x: x in ['Y','N'])
                if confirm == 'Y':
                    list(all_table.values())[response].insert(entry)
                    return
                elif confirm == 'N':
                    continue

    def admin_remove(self):
        all_table = DB.get_data()
        print("Which table do you want to remove entry from?")
        for index, table in enumerate(all_table):
            print(f"{index + 1}. {table}")
        response = int(self.take_input('', lambda x: int(x)-1 in range(len(all_table)))) - 1
        print(f"Removing entry from {list(all_table.keys())[response]}")
        table = list(all_table.values())[response]
        table_keys = list(DB.search(list(all_table.keys())[response]).table[0].keys())
        padding = [table.aggregate(len, lambda x: max(x)+2, key) for key in table_keys]
        table_keys.insert(0, '#')

        for key,pad in zip(table_keys,[3]+padding):
            print(f"|{key:<{pad}}|",end='')
        print()
        print('-'*(sum(padding)+13))
        for index,entry in enumerate(table.table):
            entry_str = f"|{index+1:<3}|"
            for val,pad in zip(entry.values(), padding):
                entry_str += f"|{val:<{pad}}|"
            print(entry_str)

        remove = int(self.take_input("Which entry do you want to remove: ",
                                 lambda x: int(x)-1 in range(len(table.table))))-1
        table.table.pop(remove)
        print("Removed entry succesfully.")

    def clear_screen(self):
        print('\n'*5)

    def Create_Project(self):
        project_name = input("Project name: ")
        project_details = input(f"Some details about {project_name}: ")
        project_table = DB.search('project')
        project_table.insert(Project(project_name, self.__id))
        print(f"Project {project_name} has been created.")

    def Invite_member(self):
        project = self.get_projects()

        for index, _project in enumerate(project):
            print(f"{index + 1}. {_project}")


        response = int(self.take_input("Invite member to which project: ",
                                       lambda x : int(x)-1 in range(len(project)))) - 1
        project = project[response]

        id = self.take_input("Enter member's student id: ", self.check_id)

        project = DB.search('project').filter(lambda proj: proj == project).table[0]
        if project.invite1 == '':
            project.invite1 = id
        elif project.invite2 == '':
            project.invite2 = id
        else:
            print('You can only invite 2 students at a time.')
            response = self.take_input('Do you want to replace this student with another? (Y/N): ',
                                       lambda x: x in ['Y','N'])
            if response == 'Y':
                print(f"1. {project.invite1}\n"
                      f"2. {project.invite2}")
                response = self.take_input('Which student would you like the new student to replace with: ',
                                lambda x: int(x) in [1,2])
                if response == 1:
                    project.invite1 = id
                elif response == 2:
                    project.invite2 = id
            elif response == 'N':
                print("No invitation sent")
        print("Invitation sent successfully")

    def Remove_member(self):
        project = self.get_projects()

        for index, _project in enumerate(project):
            print(f"{index + 1}. {_project.name}")

        project = project[int(input("Remove member from which project: ")) - 1]
        project = DB.search('project').table[project]
        self.clear_screen()

        print("Member list: ")
        print(f"1. {project.member1}")
        print(f"2. {project.member2}")
        student = self.take_input("Which student do you want to remove? : ",
                                  lambda x: int(x) in [1,2])
        if student == '1':
            project.member1 = ''
        elif student == '2':
            project.member2 = ''

        print("Removed member successfully")

    def Edit_project(self):
        project = self.get_projects()

        for index, _project in enumerate(project):
            print(f"{index + 1}. {_project.name}")

        project = project[int(input("Edit which project: ")) - 1]

        while True:
            print("Project detail:")
            print(project.project_details)
            new_project_detail = input("New project detail:\n")
            self.clear_screen()
            print("New project detail:")
            print(self.fit_text_to_screen(new_project_detail))

            confirm = self.take_input('Do you want to replace this as the new project detail? (Y/N): ',
                                       lambda x: x in ['Y','N'])
            if confirm == 'Y':
                project.project_details = new_project_detail
                return
            elif confirm =='N':
                continue

    def get_projects(self):
        project = [_project for _project in DB.search('project').table
                   if _project.lead_student == self.__id]
        return project

    def check_id(self,id):
        return any([id == ID['ID'] for ID in DB.search('person').select(['ID']).table])

    def take_input(self,text, valid):
        while True:
            response = input(text)
            if valid(response):
                return response
            else:
                print("Invalid response")

    def fit_text_to_screen(self,txt):
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



# start by adding the admin related code






# define a function called initializing
def initializing():
    global DB, application
    # create an object to read an input csv file, persons.csv
    reader = Reader()

    # create a 'persons' table
    person = Table('person', reader.read_csv('persons.csv'))
    login = Table('login', reader.read_csv('login.csv'))
    project_data = reader.read_csv('projects.csv')
#                [{'project_name':project_name,
#                  'project_details': project_details,
#                  'lead_student':id,
#                  'member1':id,
#                  'member2':id,
#                  'advisor':'faculty',
#                  'status':(Approved / Declined / Waiting),
#                  'vote_status':number starting from 0, then adds up everytime when advisor votes approves
#                  'invite1':id,
#                  'invite2':id}]

    project = []
    for _project in project_data:
        load_project = Project(_project['project_name'], _project['lead_student'])
        if _project['project_details'] != '':
            load_project.project_details = _project['project_details']
        if _project['member1'] != '':
            load_project.member1 = _project['member1']
        if _project['member2'] != '':
            load_project.project_details = _project['member2']
        if _project['advisor'] != '':
            load_project.advisor = _project['advisor']
        if _project['status'] != '':
            load_project.status = _project['status']
        if _project['vote_status'] != '':
            load_project.vote_status = _project['vote_status']
        if _project['invite1'] != '':
            load_project.invite1 = _project['invite1']
        if _project['invite2'] != '':
            load_project.invite2 = _project['invite2']

        project += [load_project]

    project = Table('project', project)
    # add the 'persons' table into the database
    DB = Database()

    DB.add(person)
    DB.add(login)
    DB.add(project)

    # add code that performs a login task; asking a user for a username and password;
    # returning [person_id, role] if valid, otherwise returning None
    application = Application()

# define a function called exit
def exit():
    # here are things to do in this function:
    # write out all the tables that have been modified to the corresponding csv files
    # By now, you know how to read in a csv file and transform it into a list of dictionaries. For this project, you also need to know how to do the reverse, i.e., writing out to a csv file given a list of dictionaries. See the link below for a tutorial on how to do this:

    # https://www.pythonforbeginners.com/basics/list-of-dictionaries-to-csv-in-python
    person = open('persons.csv', 'w')
    person_writer = csv.writer(person)
    person_writer.writerow(['ID','fist','last','type'])
    for dictionary in DB.search('person').table:
        person_writer.writerow(dictionary.values())
    person.close()

    login = open('login.csv', 'w')
    login_writer = csv.writer(login)
    login_writer.writerow(['ID','username','password','role'])
    for dictionary in DB.search('login').table:
        login_writer.writerow(dictionary.values())
    login.close()

    project = open('projects.csv', 'w')
    project_writer = csv.writer(project)
    project_writer.writerow(['project_name','project_details',
                             'lead_student','member1','member2','advisor','status','vote_status','invite1','invite2'])
    for _project in DB.search('project').table:
        project_writer.writerow(_project.save())
    project.close()

    print("Goodbye!")
    sys.exit()


# make calls to the initializing and login functions defined above
initializing()
application.Start_Application()

# once everyhthing is done, make a call to the exit function

