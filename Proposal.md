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
def Evaluate_project(project_name):
    for project in _Database.search('project').table:
        if project.name == project_name and user['person_id'] not in project.vote_status:
            print(project.project_details)
            print("(Approve / Deny)")
            _response = '1' if input() == 'Approve' else '0'
            project.vote_status += _response
            return
    print('Project not found in request box')

```