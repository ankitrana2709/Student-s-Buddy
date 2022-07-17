# Student's Buddy

#### Video Demo: = https://www.youtube.com/watch?v=1WdroM1oXII
#### Website URL = https://yesbuddy.herokuapp.com/

### Description:
#### static folder:
 logo: i created this logo for this application and named it with colour and font name

 favicon: i created this favicon for this application

 styles.css: there is,

     navigation bar styles

     font classes

     button editing

     grid editing for boons

#### templates folder:
 Add_Report.html: used this html for adding new task in my reports

 apology.html: used it to mark an error and provide a hint to the user.

 average.html: Used it for Report Card where average of the user is given.

 boon.html: Used it to provide information for qualities required to be better in your tasks.
                 1. Discipline
                Create specific and realistic goals.
                Create a schedule for yourself
                Place reminders
                Reward yourself when you get something done

                2. Consistency
                Keep going if you make a mistake.
                Take time off to recharge
                Use motivational tools to keep going
                Hold yourself accountable

                3. Alter Thinking
                Give yourself time to see changes
                Set boundaries for your commitments
                Build your willpower
                Eliminate negative thinking

                4. Managing Time
                Meeting deadlines
                Self-awareness
                Stress management and coping
                Strategic planning

 index.html: used as home page and to greet users.

 layout.html: used it as the main html where i defined navigation bars and font families extended it with jinja
              in the head tag we have inserted links of bootstrap files, we have linked with favicon here and we have linked with fontawesome here.
              for connecting with google forms we have connected with google api and brought in font family of Quicksand

              We have marked the title of our home page as Well Wisher.

              Then in body we explain about navigation bar in which we have brought in an icon from fontawesome and using fa- x we changed its size as well.
              ahead of that we typed some functions which are to be executed which are only displayed when login is initiated.in the navigation bar. and at last there is logout button

 login.html: to login for an existing user.

 My_Report.html: used it to provide with table. used jinja for loop to get information out of the database
                every date, hour, minutes, progress and new aim have been brought into this page of a username

 register.html: to register new users and add into database.

 #### app.py: as the main application python file, where all the backend worked.
              we define functions in here
              login with post request it takes user details and with get request it brings in the user details from database. if not matched then renders an apology
                which i generated using memelink
              logout to tell the server that the session is over.
              register to mark a new user. if there is no login credential then register a new user
              average take the data out of the logbook and then count average that is required to perform function
              My_report rendering all the stuff which is happening in html with jinja
              Add_report to add a new report we create this function which posts data into logbook
 #### buddy.db: as a database to collect and retreive all the information provided by the user.
             concerned with two tables
             students: which keeps  records of all the students registered with the app
             logbook: which keeps the record of all the activity of all the users and their progress.
 #### helpers.py: to support our application with apology function and decorator of login required.
           apology: renders a memelink always with a code for technical people and error in simple language as well to make all types of users understand the problem                and correct it
           login required decorator: to not bring some functions which include data of the user without logging in.
 #### Procfile: Used this to deploy this application on Heroku we use gunicorn
 #### test.py: Used to test my intutions. tested some database queries in here and it is always handy.
So,
This is a task manager application which takes in new reports from you everyday
and then deploy it into a table and show in My reports
after collecting all the information required, it calculates the average of your work and returns you with
a conditional remark based on your performance
It also provides you with information about how to manage your tasks and gives your four boons
related to your work.

## Technologies used:
 ### Python
 ### HTML
 ### CSS
 ### JINJA
 ### SQLITE3
 ### HEROKU
