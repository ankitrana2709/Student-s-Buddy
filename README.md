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
 
 index.html: used as home page and to greet users.

 layout.html: used it as the main html where i defined navigation bars and font families extended it with jinja
 
 login.html: to login for an existing user.
 
 My_Report.html: used it to provide with table. used jinja for loop to get information out of the database
 
 register.html: to register new users and add into database.
 
 #### app.py: as the main application python file, where all the backend worked.
 #### buddy.db: as a database to collect and retreive all the information provided by the user.
 #### helpers.py: to support our application with apology function and decorator of login required.
 #### Procfile: Used this to deploy this application
 #### test.py: Used to test my intutions.
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
