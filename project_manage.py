# import database module
from database import *
import random
import sys


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

    def advisor_run(self):
        while True:
            pass

    def student_run(self):
        menu_choice = (f"1. Create a project\n"
                       f"2. Invite member to project\n"
                       f"3. Remove member from project\n"
                       f"4. Edit project\n"
                       f"5. Send advisor request\n"
                       f"6. Submit project\n"
                       f"7. Logout\n")
        while True:
            self.Show_Menu(menu_choice)
            response = input()
            if response == '1':
                self.Create_Project()
            elif response == '2':
                self.Invite_member()
            elif response == '3':
                self.Remove_member()



            elif response == '7':
                exit()




    def member_student_run(self):
        pass


    def faculty_run(self):
        pass


    def admin_run(self):
        pass


    def clear_screen(self):
        for _ in range(10):
            print('\n'*5)

    def Create_Project(self):
        project_name = input("Project name: ")
        project_details = input(f"Some details about {project_name}: ")
        project_table = DB.search('project')
        project_table.insert({'project_name':project_name,
                              'lead_student':self.__id,
                              'member1':'',
                              'member2':'',
                              'status':'Declined',
                              'vote_status':'',
                              'project_details':project_details})
        print(f"Project {project_name} has been created.")

    def Invite_member(self):
        project = self.get_projects()

        for index, _project in enumerate(project):
            print(f"{index + 1}. {_project}")

        while True:
            response = int(input("Invite member to which project: ")) - 1
            if 0 <= response < len(project):
                project = project[response]
                break
            else:
                print("Invalid response")

        id = input("Enter member's student id: ")

        if self.check_id(id):
            project = DB.search('project').filter(lambda proj: proj['project_name'] == project).table[0]
            if project['member1'] == '':
                project['member1'] = id
            elif project['member2'] == '':
                project['member2'] = id
            else:
                print('There can only be 3 students in a project.')
                return
            print("Invitation sent successfully")
        else:
            print("Invalid ID.")

    def Remove_member(self):
        project = self.get_projects()

        for index, _project in enumerate(project):
            print(f"{index + 1}. {_project.name}")

        project = project[int(input("Remove member from which project: ")) - 1]
        id = input("Enter member's student id: ")

        if self.check_id(id) and id in DB.search('project').table[project.name].member:
            DB.search('project').table[project.name].remove(id)
            print("Removed member successfully")
        else:
            print("Invalid ID.")

    def get_projects(self):
        project = [_project['project_name'] for _project in DB.search('project').table
                   if _project['lead_student'] == self.__id]
        return project

    def check_id(self,id):
        return any([id == ID['ID'] for ID in DB.search('person').select(['ID']).table])

# start by adding the admin related code






# define a function called initializing
def initializing():
    global DB, application
    # create an object to read an input csv file, persons.csv
    reader = Reader()

    # create a 'persons' table
    person = Table('person', reader.read_csv('persons.csv'))
    login = Table('login', reader.read_csv('login.csv'))
    project = Table('project', reader.read_csv('projects.csv'))
#                [{'project_name':project_name,
#                  'lead_student':id,
#                  'member1':id,
#                  'member2':id,
#                  'status':(Approved / Declined / Waiting),
#                  'vote_status':number starting from 0, then adds up everytime when advisor votes approves,
#                  'project_details':project_details}]

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
    project_writer.writerow(['project','invitation','pending_eval'])
    for dictionary in DB.search('project').table:
        project_writer.writerow(dictionary.values())
    project.close()

    print("Goodbye!")
    sys.exit()


# make calls to the initializing and login functions defined above
initializing()
application.Start_Application()

# once everyhthing is done, make a call to the exit function

