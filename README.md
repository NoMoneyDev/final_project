# Final project for 2023's 219114/115 Programming I

persons.csv : the file that contains everyone's id, names, and their types
- id (ID number of the person)
- first (First name of the person)
- last (Last name of the person)
- type (Role of the person)
  
login.csv : the file that contains all the login credentials
- ID (id number of the person)
- username (username the person uses to login)
- password (password the person uses to login)
- role (role of the person)

projects.csv : the file that contains all the student's project
- (class Project : Is created when students create projects, or during initializing() when the program load data from files into Table and Projects)
- project_id (id of the project)
- project_name (name of the project)
- project_details (this is what students will edit in the program)
- lead_student (id of the student who created the project)
- member1 (id of a member)
- member2 (id of a member)
- advisor (id of the project's advisor)
- status (Approves : project has been evaluated and passed, Waiting : project in evaluation process, Declined : default status of a project, or if a project has been evaluated and failed)
- vote_status (dictionary of voter and votes seperated by ' ' and each pairs is then seperated by ':')
- invite1 (id and date of invitation of the student that gets invited, a dictionary that key and values are seperated by ':')
- invite2 (id and date of invitation of the student that gets invited, a dictionary that key and values are seperated by ':')
- invite_advisor (id and date of invitation of the advisor that gets invited, a dictionary that key and values are seperated by ':')

database.py : the file that contains almost all the class
- Project : The class that each object will contain information of each entry in the projects.csv
- Table : The class the each object will represent a csv file (either persons.csv or login.csv)
- Database : The class that each object will contain any number of tables


# How to compile and run project
1. Clone this repository in to your local repository
2. Change the persons.csv and login.csv to your data pool
3. Thats it! (Optional: if you have data for your student's projects too, then you can put them in projects.csv file)


  
# Role and Actions

| Role    | Action                     | Method               | Class                    | Completion Percentage | Missing features/ Bugs|
|---------|----------------------------|----------------------|--------------------------|-----------------------|-----------------------|
| Admin   | Insert a new entry         | admin_insert()       | Table, Database          | 80% | No type check for any table|
|         | Remove an entry            | admin_remove()       | Table, Database          | 100% | |
| Student | Create a project           | Create_Project()     | Project, Table           | 90% | You can create projects with blank names, There are no checks for projects with same id |
|         | See project detail         | See_project_detail() | Project, Table, Database | 100% | |
|         | Invite member to project   | Invite_member(), get_projects()  | Project, Table, Database | 100% | |
|         | Remove member from project | Remove_member(), get_projects()      | Project, Table, Database | 100% | |
|         | Edit project               | Edit_project(), get_projects(), fit_text_to_screen()      | Project, Table, Database | 100% | |
|         | Send advisor request       | Send_advisor_req(), get_projects()   | Project, Table, Database | 100% | |
|         | Submit project             | Send_eval_req(), get_projects()      | Project, Table, Database | 100% | |
|         | Accept project invitation  | Accept_invitation()  | Project, Table, Database | 100% | |
| Facilty | See all project's detail           | See_all_project_detail() | Project, Table, Database | 100% | |
|         | Accept project advising invitation | Accept_advisor()         | Project, Table, Database | 100% | |
|         | Evaluate project                   | Evaluate_project()       | Project, Table, Database | 100% | |
| _main_  | Initialize                         | initializing()           | Project, Table, Database | 100% | |
|         | Exit                               | exit()       | Project, Table, Database | 100% | |


# Missing features and bugs
- Almost no type checks at all
- Students are able to create projects with empty name (empty project detail at creation is intended)

