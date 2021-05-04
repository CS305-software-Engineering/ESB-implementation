# ESB-implementation
The project consists of the implementation of an Enterprise Service Bus that facilitates a safe, secure and fast communication between clients and applications.

### Links to important documents:
1. [Software Requirements Specification ](https://github.com/CS305-software-Engineering/ESB-implementation/wiki/SRS-Document)
2. [High-Level Design Document ](https://github.com/CS305-software-Engineering/ESB-implementation/wiki/High-Level-Design-Document)
3. [Low-Level Design Document ](https://github.com/CS305-software-Engineering/ESB-implementation/wiki/Low-Level-Design-Document)
4. [Coding Report](https://github.com/CS305-software-Engineering/ESB-implementation/wiki/Coding-Report)
5. [Testing Plan Document](https://github.com/CS305-software-Engineering/ESB-implementation/wiki/Test-Plan-Document)

### Instrutions to run the project
1. Setting up the database :
    1. Install MySQL on your system.
    2. Setup the root user with a password.
    3. In the MySQL command line, copy the code from init.sql file and paste it there.
    4. Run "show tables;" command to check if all three tables are there.
    5. Use your mysql password in line 44 of app.py 
2. run pip3 install -r requirements.txt
3. run start file (bash file) using "./start"
4. Follow the link(http://127.0.0.1:5000/) printed on the terminal
5. Use signup option to register
6. Click on admin login and login using the following credentials
    username: admin <br>
    password: pass123 <br>
7. Go to pending requests, click on confirm to authorize any pending users. 
8. Users will recieve an email from cs305esb@gmail.com confirming their request status after their request is processed by admin
9. User can now use esb at http://127.0.0.1:5000/

### Deployment:
We tried deploying on heroku, as our TA suggested us to do so after our GCP credits expired, but heroku doesnot allow Inter Process Communication, so we were not able to deploy all the functionalities, however we can use all functionalities if we host on local server.<br>
[click here to use ESB hosted on heroku](https://esb-implementation.herokuapp.com/) <br>
We can still use functionalities like registering,checking logs, accepting pending requests, recieving messages from other clients who are using localserver to run ESB as the database is hosted on heroku <br>
But we cannot get API responses, we cannot send messages to other clients as this needs Inter Process Communication, which is not possible on heroku.
