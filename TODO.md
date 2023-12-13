### **Admin** 
- [ ] Manage database
  - Insert new entry to **Table** in **Database**
  - Remove entry from **Table** in **Database**
---
### **Lead Student**
- [ ] Create a project
  - _class_ **Project** :
    - _project name_
    - _member list_ `['lead_std_id', 'member_id']`
    - _status : (Approved / Declined / Waiting)_
    - _vote_status = Dictionary of voters_id and True / False depending on if the voter approves or not_
    - _project details_
    - _work space_ : Dictionary {work_name : strings}
      - e.g.```{ 'Python' : 'print(Hello world)', 'JS' : 'console.log(Hello_world)' }```
  
- [ ] Find _members_
  - Send invitation message to **Member's student** id

- [ ] Add _members_ to **Project**
  - (Add / Remove) _members_ from **Project**

- [ ] See and Modify _project details_
  - edit _project details_

- [ ] Send request to Advisors
  - Send request message to **advisors**

- [ ] Submit final project report
  - Submit final report to **advisor**
---
### **Member Student**
- [ ] See _invitational message_ from **Lead Student**
  - (Accept / Deny) _invitation_
- [ ] See and Modify _project details_
  - edit _project details_
---
### **Normal faculty who is not an advisor**
- [ ] See details of all the **Project**
  - Have access to all **Project** object
- [ ] Evaluate **Project**s
  - Vote (Pass / Not Pass) to **Project** object
---
### **Advising faculty**
- [ ] See request to be **advisor**
  - Send (Accept / Deny) response
- [ ] See details of all the **Project**
  - Have access to all **Project** object
- [ ] Evaluate **Project**s
  - Vote (Pass / Not Pass) to **Project** object
- [ ] Approve **Project**
---
