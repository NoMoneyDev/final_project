# import database module
from database import *
from datetime import date
import random
import sys


__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

class Application:
    def __init__(self):
        '''
        initialize
        '''
        self.__username = ''
        self.__id = ''

    def Start_Application(self):
        '''
        Start the program
        :return: Nothing
        '''
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
        '''
        Show menu for the user
        :param menu_choice: string to use as menu
        :return: Nothing
        '''
        self.clear_screen()
        print(f"Hello, {self.__username}!")
        print(menu_choice)

    def Login(self,val):
        '''
        Login
        :param val: resulting tuple from Login_Prompt() function
        :return: Nothing
        '''
        if val[1] == 'student':
            self.student_run()
        elif val[1] == 'faculty':
            self.faculty_run()
        elif val[1] == 'admin':
            self.admin_run()

    # start by adding the admin related code
    def admin_run(self):
        '''
        If user is admin, run this.
        :return: Nothing
        '''
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
        '''
        If user is student run this.
        :return: Nothing
        '''
        menu_choice = (f"1. Create a project\n"
                       f"2. See project detail\n"
                       f"3. Invite member to project\n"
                       f"4. Remove member from project\n"
                       f"5. Edit project\n"
                       f"6. Send advisor request\n"
                       f"7. Submit project\n"
                       f"8. Accept project invitation\n"
                       f"Q. Logout\n")
        while True:
            self.Show_Menu(menu_choice)
            response = input()
            if response == '1':
                self.Create_Project()
            elif response == '2':
                self.See_project_detail()
            elif response == '3':
                self.Invite_member()
            elif response == '4':
                self.Remove_member()
            elif response == '5':
                self.Edit_project()
            elif response == '6':
                self.Send_advisor_req()
            elif response == '7':
                self.Send_eval_req()
            elif response == '8':
                self.Accept_invitation()
            elif response == 'Q':
                exit()
            else:
                print("Invalid response")


    def faculty_run(self):
        '''
        If user is faculty, run this.
        :return: Nothing
        '''
        menu_choice = (f"1. See all project's detail\n"
                       f"2. Accept project advising invitation\n"
                       f"3. Evaluate project\n"
                       f"Q. Logout\n")
        while True:
            self.Show_Menu(menu_choice)
            response = input()
            if response == '1':
                self.See_all_project_detail()
            elif response == '2':
                self.Accept_advisor()
            elif response =='3':
                self.Evaluate_project()
            elif response == 'Q':
                exit()
            else:
                print("Invalid response")


    def admin_insert(self):
        '''
        Let admin insert an entry to a table
        :return: Nothing
        '''
        all_table = DB.get_data()
        print("Which table do you want to add entry to?")
        for index,table in enumerate(all_table):
            print(f"{index+1}. {table}")
        print("(Enter 'Q' to quit)")

        response = input()
        if response == 'Q':
            return
        else:
            check = lambda x: int(x) - 1 in range(len(all_table))
            if check(response):
                response = int(response) - 1

        table = list(all_table.values())[response]
        if table.name == 'project':
            table_keys = ['project_name','project_details','lead_student','member1','member2',
                             'advisor','status','vote_status','invite1','invite2','invite_advisor']
        else:
            table_keys = DB.search(list(all_table.keys())[response]).table[0].keys()
        while True:
            self.clear_screen()
            print(f"Adding entry to {list(all_table.keys())[response]}")
            new_entry_input = input(f"Keys     : {list(table_keys)}\n"
                                    f"New entry: ")
            entry = {}
            if new_entry_input == 'Q':
                return
            if len(new_entry_input.split(',')) != len(table_keys):
                print("Invalid entry")
                input('\nPress enter.')
                continue
            else:
                print("Your new entry is: ")
                new_entry_str = "{"
                for key,val in zip(table_keys, new_entry_input.split(',')):
                    new_entry_str += f"{key.strip()} : {val.strip()}, "
                    entry[key] = val.strip()
                new_entry_str = new_entry_str[:-1] + "}"
                print(new_entry_str)

                confirm = self.take_input("Confirm? (Y/N): ",lambda x: x in ['Y','N'])
                if confirm == 'Y':
                    if table.name == 'project':
                        load_project = Project(entry['project_name'], entry['lead_student'])
                        load_project.project_details = entry['project_details']
                        load_project.member1 = entry['member1']
                        load_project.project_details = entry['member2']
                        load_project.advisor = entry['advisor']
                        load_project.status = entry['status']
                        load_project.vote_status = entry['vote_status']
                        load_project.invite1 = entry['invite1']
                        load_project.invite2 = entry['invite2']
                        load_project.invite_advisor = entry['invite_advisor']
                        table.insert(load_project)
                    else:
                        table.insert(entry)
                    input('\nPress enter.')
                    self.clear_screen()
                    return
                elif confirm == 'N':
                    continue

    def admin_remove(self):
        '''
        Let admin remove an entry from a table
        :return: Nothing
        '''
        all_table = DB.get_data()
        print("Which table do you want to remove entry from?")
        for index, table in enumerate(all_table):
            print(f"{index + 1}. {table}")
        print("(Enter 'Q' to quit)")
        response = input()
        if response =='Q':
            return
        else:
            check = lambda x: int(x) - 1 in range(len(all_table))
            if check(response):
                response = int(response)-1

        print(f"Removing entry from {list(all_table.keys())[response]}")
        table = list(all_table.values())[response]
        print(table)

        check = lambda x: int(x) - 1 in range(len(table.table))
        while True:
            remove = input("Which entry do you want to remove (Enter 'Q' to quit): ")
            if remove == 'Q':
                return
            elif check(remove):
                remove = int(remove)-1
                break
            else:
                print("Invalid input")

        table.table.pop(remove)
        print("Removed entry succesfully.")
        input('\nPress enter.')
        self.clear_screen()

    def clear_screen(self):
        '''
        Create some blank space for a little more cleanliness
        :return: Nothing
        '''
        print('\n'*5)

    def Create_Project(self):
        '''
        Let student create their projectw
        :return: Nothing
        '''
        while True:
            project_name = input("Project name (Enter 'Q' to quit): ")
            if project_name == 'Q':
                return
            if project_name in [proj.name for proj in DB.search('project').table]:
                print('There already is a project with this name.\n'
                      'Please use another name')
                input('\nPress enter.')
                self.clear_screen()
                continue
            break

        project_details = input(f"Some details about {project_name}: ")
        project_table = DB.search('project')
        project = Project(project_name, self.__id)
        project.project_details = project_details
        project_table.insert(project)
        print(f"Project {project_name} has been created.")
        input('\nPress enter.')
        self.clear_screen()

    def Invite_member(self):
        '''
        Let student invite other student using their id to their project
        :return: Nothing
        '''
        all_project = self.get_projects()

        if len(all_project) == 0:
            print("You don't have any projects yet.")
            input('\nPress enter.')
            self.clear_screen()
            return

        for index, _project in enumerate(all_project):
            print(f"{index + 1}. {_project.name}")


        response = int(self.take_input("Invite member to which project: ",
                                       lambda x : int(x)-1 in range(len(all_project)))) - 1
        project = all_project[response]

        while True:
            id = input("Enter member's student id: ")
            if self.check_id(id) and self.isStudent(id) and id != self.__id:
                break
            else:
                print("Invalid ID\n")

        inv_str = f"{id}:{str(date.today())}"

        if project.invite1 == '':
            project.invite1 = inv_str
        elif project.invite2 == '':
            project.invite2 = inv_str
        else:
            print('You can only invite 2 students at a time.')
            response = self.take_input('Do you want to replace this student with another? (Y/N): ',
                                       lambda x: x in ['Y','N'])
            if response == 'Y':
                print(f"1. {project.invite1.split(':')[0]}\n"
                      f"2. {project.invite2.split(':')[0]}\n")
                response = self.take_input('Which student would you like the new student to replace with: ',
                                lambda x: int(x) in [1,2])
                if response == 1:
                    project.invite1 = inv_str
                elif response == 2:
                    project.invite2 = inv_str
            elif response == 'N':
                print("No invitation sent")
                input('\nPress enter.')
                self.clear_screen()
                return
        print("Invitation sent successfully")
        input('\nPress enter.')
        self.clear_screen()
        return

    def Accept_invitation(self):
        '''
        Let student accept invitation to join another project
        :return: Nothing
        '''
        project_invite = [project for project in DB.search('project').table
                          if project.invite1.split(':')[0] == self.__id or project.invite2.split(':')[0] == self.__id]

        if len(project_invite) == 0:
            print("You don't have any invitations yet.")
            input('\nPress enter.')
            self.clear_screen()
            return

        for index,project in enumerate(project_invite):
            print(f"{index+1}. {project.name}")
        print("Q. Do not accept")

        while True:
            response = input("Which project invitation do you want to accept? : ")
            if response == 'Q':
                return

            check = lambda x: int(x) - 1 in range(len(project_invite))
            if not check(response):
                print("Invalid response")
                print()
                continue


            response = int(response) - 1
            project = project_invite[response]


            if project.member1 == '':
                project.member1 = self.__id
                if project.invite1 == self.__id:
                    project.invite1 = ''
                elif project.invite2 == self.__id:
                    project.invite2 = ''
                break
            elif project.member2 == '':
                project.member2 == self.__id
                if project.invite1 == self.__id:
                    project.invite1 = ''
                elif project.invite2 == self.__id:
                    project.invite2 = ''
                break
            else:
                print("Project is already full.")
                input('\nPress enter.')
                project.invite1 = ''
                project.invite2 = ''
                return

        print("Invitation accepted")
        input('\nPress enter.')
        self.clear_screen()
        return

    def Remove_member(self):
        '''
        Let user remove the member of the project
        :return: Nothing
        '''
        all_project = self.get_projects()

        if len(all_project) == 0:
            print("You don't have any projects yet.")
            input('\nPress enter.')
            self.clear_screen()
            return

        for index, _project in enumerate(all_project):
            print(f"{index + 1}. {_project.name}")

        response = int(self.take_input("Remove member from which project: ",
                                   lambda x: int(x)-1 in range(len(all_project))))-1
        project = all_project[response]

        if all([i=='' for i in [project.member1, project.member2]]):
            print("There is no member in this project.")
            input('\nPress enter.')
            self.clear_screen()
            return

        self.clear_screen()
        member = [project.member1, project.member2]
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
        input('\nPress enter.')
        self.clear_screen()

    def Edit_project(self):
        '''
        Lets user edit project that they are a part of. (Being a member or a lead student)
        :return: Nothing
        '''
        all_project = self.get_projects() + [project for project in DB.search('project').table
                                         if project.member1 == self.__id or project.member2 == self.__id]

        if len(all_project) == 0:
            print("You are not a member of any projects yet.")
            input('\nPress enter.')
            self.clear_screen()
            return

        for index, _project in enumerate(all_project):
            print(f"{index + 1}. {_project.name}")

        while True:
            response = input("Edit which project? : ")
            if response == 'Q':
                return
            check = lambda x: int(x) - 1 in range(len(all_project))
            if check(response):
                response = int(response) - 1
                break
            else:
                print("Invalid input.")
                input('\nPress enter.')
                self.clear_screen()

        project = all_project[response]

        while True:
            print("Project detail:")
            print(self.fit_text_to_screen(project.project_details))
            new_project_detail = input("\nNew project detail:\n")
            self.clear_screen()
            print("New project detail:")
            print(self.fit_text_to_screen(new_project_detail))

            while True:
                confirm = input('Do you want to replace this as the new project detail? '
                                '(Y/N) (Enter "Q" to cancel): ')

                if confirm == 'Y':
                    project.project_details = new_project_detail
                    return
                elif confirm == 'N':
                    return
                elif confirm == 'Q':
                    return

    def get_projects(self):
        '''
        Give all the project that the student owns
        :return: list of Project objects
        '''
        project = [_project for _project in DB.search('project').table
                   if _project.lead_student == self.__id]
        return project

    def check_id(self,id):
        '''
        Check if the id is valid
        :param id: id to check
        :return: True if it is in persons.csv else False
        '''
        return any([id == ID['ID'] for ID in DB.search('person').select(['ID']).table])

    def take_input(self,text, valid):
        '''
        This is so badly written
        :param text: text to ask user for input
        :param valid: function to check if the input is valid
        :return: valid input
        '''
        while True:
            response = input(text)
            if valid(response):
                return response
            else:
                print("Invalid response")

    def fit_text_to_screen(self,txt):
        '''
        turn word spaghetti into string that cut to new line every 10 word
        :param txt: txt to convert
        :return: string that cut to new line every 10 word
        '''
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

    def See_all_project_detail(self):
        '''
        Self explainatory
        :return: Nothing
        '''
        all_project = DB.search('project')
        print(all_project)
        _continue = input('Press enter :')

    def Send_advisor_req(self):
        '''
        Send out request to an advisor using their id
        :return: Nothing
        '''
        all_project = self.get_projects()

        if len(all_project) == 0:
            print("You don't have any projects yet.")
            input('\nPress enter.')
            self.clear_screen()
            return

        for index,project in enumerate(all_project):
            print(f"{index+1}. {project.name}")

        while True:
            response = input("Which project do you want to send advisor request from (Enter 'Q' to quit) : ")
            if response == 'Q':
                return
            check = lambda x: int(x) - 1 in range(len(all_project))
            if check(response):
                response = int(response) - 1
                break
            else:
                print("Invalid input.")
                input('\nPress enter.')
                self.clear_screen()

        project = all_project[response]

        project = all_project[response]
        if project.advisor != '':
            print("You already have an advisor.")
            input('\nPress enter.')
            self.clear_screen()
            return
        if project.invite_advisor != '':
            response = self.take_input("Do you want to overwrite the previous invite? (Y/N): ",
                                       lambda x: x in ['Y','N'])
            if response == 'Y':
                True
            elif response == 'N':
                return

        id = self.take_input("Advisor's ID : ", self.check_advisor_id)

        inv_str = f"{id}:{str(date.today())}"

        project.invite_advisor = inv_str

        print("\nAdvisor invite sent successfully.")
        input('\nPress enter.')
        self.clear_screen()



    def Accept_advisor(self):
        '''
        Let advisor accept advisor request that student's sent out
        :return: Nothing
        '''
        all_project = DB.search('project').table
        all_project = [project for project in all_project if project.invite_advisor == self.__id]

        if len(all_project) == 0:
            print("You don't have any advisor request at the moment.")
            input('\nPress enter.')
            self.clear_screen()
            return

        for index,project in enumerate(all_project):
            print(f"{index+1}. {project.name}")

        response = int(self.take_input("Which project do you want to be an advisor for? : ",
                                       lambda x: int(x) - 1 in range(len(all_project)))) - 1
        project = all_project[response]
        project.advisor = self.__id
        project.invite_advisor = ''
        print(f"You are now the advisor for {project.name}")
        input('\nPress enter.')
        self.clear_screen()

    def isStudent(self,id):
        '''
        Check if the id given is a student id from 'persons.csv'
        :param id: id that you want to user
        :return: True if the id is a student id else False
        '''
        all_person = DB.search('person').table
        for person in all_person:
            if person['ID'] == id:
                return person['type'] == 'student'

    def Send_eval_req(self):
        '''
        Ask user which project to send for evaluation, then change the projects status to "Waiting".
        :return: Nothing
        '''
        all_project = self.get_projects()

        if len(all_project) == 0:
            print("You don't have any projects yet.")
            input('\nPress enter.')
            self.clear_screen()
            return

        for index, _project in enumerate(all_project):
            print(f"{index + 1}. {_project.name}")
        print("(Enter 'Q' to quit)")

        while True:
            response = input("Send evaluation request from which project? : ")
            if response == 'Q':
                return

            check = lambda x: int(x) - 1 in range(len(all_project))
            if check(response):
                response = int(response) - 1
                break
            else:
                print("Invalid input.")
                input('\nPress enter.')
                self.clear_screen()

        project = all_project[response]

        if project.status == 'Waiting':
            print("Already in evaluation process.")
            input('\nPress enter.')
            self.clear_screen()
            return

        project.status = 'Waiting'
        print("Evaluation request sent successfully.")
        input('\nPress enter.')
        self.clear_screen()
        return

    def Evaluate_project(self):
        '''
        Ask user which project they want to evaluate then let them vote
        :return: Nothing
        '''
        all_project = [project for project in DB.search('project').table if project.status == 'Waiting']

        if len(all_project) == 0:
            print("No project to evaluate yet.")
            input('\nPress enter.')
            self.clear_screen()
            return

        for index,project in enumerate(all_project):
            print(f"{index+1}. {project.name}")
        print("(Enter 'Q' to quit)")

        while True:
            response = input("Which project would you like to evaluate? : ")
            if response == 'Q':
                return

            check = lambda x: int(x) - 1 in range(len(all_project))
            if check(response):
                response = int(response) - 1
                break
            else:
                print("Invalid input.")
                input('\nPress enter.')
                self.clear_screen()
        self.clear_screen()

        project = all_project[response]

        if self.check_voted(project):
            return

        print(project)

        while True:
            vote = input("Approves/Not approves (Y/N) : ")
            if vote not in ['Y','N']:
                print("Invalid input.")
                input('\nPress enter.')
                self.clear_screen()
                continue

            if vote == 'Y':
                project.vote_status += f':{self.__id} 1 '
                self.check_project_eval(project)
                return
            elif vote == 'N':
                project.vote_status += f':{self.__id} 0 '
                self.check_project_eval(project)
                return

    def check_project_eval(self, project):
        '''
        Check if project has already been voted by every faculty and approves the project if so.
        :param project: Project object to check
        :return: Nothing
        '''
        all_faculty_num = len([fac for fac in DB.search('person').table if fac['type'] == 'faculty'])
        vote = [vote.split()[1] for vote in project.vote_status.split(':')[1:]]

        if len(project.vote_status.split(':')[1:]) != all_faculty_num:
            return
        elif vote.count('1') > vote.count('0'):
            project.status = 'Approved'
        else:
            project.status = 'Declined'
            project.vote_status = ''

    def check_voted(self, project):
        '''
        Check if the user has evaluated this project yet
        :param project: Project to check if the user has evaluated this project yet or no
        :return: True if user already evaluated the project else False
        '''
        if project.vote_status == '': return False
        _all_vote = project.vote_status.split(':')
        for vote in _all_vote[1:]:
            if self.__id == vote.split()[0]:
                print("You already evaluated this project.")
                input('\nPress enter.')
                self.clear_screen()
                return True
        return False

    def check_advisor_id(self, id):
        all_person = DB.search('person').table
        for person in all_person:
            if person['ID'] == id:
                return person['type'] == 'faculty'
        return False

    def See_project_detail(self):
        all_project = self.get_projects() + [project for project in DB.search('project').table
                                         if project.member1 == self.__id or project.member2 == self.__id]

        if len(all_project) == 0:
            print("You don't have any projects yet.")
            input('\nPress enter.')
            self.clear_screen()
            return

        for index, _project in enumerate(all_project):
            print(f"{index + 1}. {_project.name}")
        print("(Enter 'Q' to quit)")

        while True:
            response = input("See which project's details? (Enter 'Q' to quit) : ")
            if response == 'Q':
                return

            self.clear_screen()

            check = lambda x: int(x) - 1 in range(len(all_project))
            if check(response):
                response = int(response) - 1
                break
            else:
                print("Invalid input.")
                input('\nPress enter.')
                self.clear_screen()

        project = all_project[response]

        print(project)
        input('\nPress enter.')


# define a function called initializing
def initializing():
    '''
    Program setup
    :return:
    '''
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
        load_project.id = _project['project_id']
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
    person_writer.writerow(['ID','first','last','type'])
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
    project_writer.writerow(['project_id','project_name','project_details','lead_student','member1','member2',
                             'advisor','status','vote_status','invite1','invite2','invite_advisor'])
    for _project in DB.search('project').table:
        project_writer.writerow(_project.save())
    project.close()

    print("Goodbye!")
    sys.exit()


# make calls to the initializing and login functions defined above
initializing()
application.Start_Application()

# once everyhthing is done, make a call to the exit function

