### Evaluate **Project**
- [ ] Send evaluation request of a **Project** to every faculty
```python
class Project:
    def __init__(self):
        ...
        self.vote_status = {advisor : True/False}
    
    def send_evaluation_request(self):
        pending = _Database.search('pending evaluate').table
        pending.insert(_Project.name, self)
```
- [ ] Each faculty will get to vote (Pass / Not Pass) on a **project**
```python
def evalute_project(project_name):
    for project in _Database.search('pending_evaluate').table:
        if project.name == project_name and user['person_id'] not in project.vote_status:
            print(project.project_details)
            print("(Approve / Deny)")
            _response = True if input() == 'Approve' else False
            project.vote_status += [{user['person_id'] : _response}]
            return
    print('Project not found in request box')

user = Login_Prompt()
Login(user)
evalute_project(project_name)
```