### Evaluate **Project**
- [ ] Send evaluation request of a **Project** to every faculty
```python
    def Send_eval_req(self):
        all_project = self.get_projects()

        if len(all_project) == 0:
            print("You don't have any projects yet.")
            input('\nPress enter.')
            self.clear_screen()
            return

        while True:

            for index, _project in enumerate(all_project):
                print(f"{index + 1}. {_project.name}")
            print("(Enter 'Q' to quit)")

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

```
- [ ] Each faculty will get to vote (Pass / Not Pass) on a **project**
```python
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
                project.status = 'Declined'
                project.vote_status = ''
```