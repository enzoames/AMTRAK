# AMTRAK PROJECT
## Optimizing the AMTRAK rail road system

## RUNNING SERVER - MIGRATIONS - SQL COMMANDS - ADMIN PAGE 
## - READY TO WORK? - RAW SQL COMMANDS WITH DJANGO

**NOTE! please read the following first and make no changes to the code yet.** 
**Once done reading and implementing go to READY TO WORK?**

### RUNNING SERVER (locally)

Once you clone the repo, the first thing you will do is navigate to the folder where the file 
manage.py file is saved. Once there run this command:

    python manage.py runserver 0:8000

This command will run the server locally in your web browser. Open any browser and type:

    localhost:8000/

This should display the site where we will implement the GUI. Go back to your terminal/command 
prompt and you will see the server running. you can close it by hitting { control c }


### ADMIN PAGE

The admin page is very important bc where we will populate the database tables with information. 
In order for you to access the admin page:

   **NOTE!** if you shut down the server you must run it again for this to show
    
    localhost:8000/admin
  
    username: admin
    password: csc336project

Inside the admin page you can see the tables and populate them with data if needed. 
Very handy tool that Django offers you


### MIGRATIONS

Inside amtrakmain/migrations folder you can see there is a 0001_initial.py file, if you open it 
you can see what was created inside the database. I (Enzo) created a table in our database and 
Django kept a log of the changes. Any changes in models.py indicates that we need to tell 
DJANGO to start a 'migration' then we will see the changes in our admin page.

As we move forward we will create more tables and make more changes. In order for you tell django 
that the changes you made to models.py need to be added to our database, you do:

   **NOTE!** Run these commands inside manage.py file is located. The first time you do this it
   will say that there are no migrations detected. Once you start working on your branch, and 
   want to check you work you will use these commands

    python manage.py makemigrations

    python manage.py migrate

After these two commands you will see that Django created the tables or changes in the database. 
But ! If there are any errors in your code, Django will show you what they are.


### SQL COMMANDS

Django is going to run the sql commands that will be needed in order to add tables, make changes, 
etc. In other words you are not required to type any sql commands, Django will simply do that for you.

Now, for the purpose of the class there is a way to see what type of sql commands django is 
doing every time you are making changes to the database (amtrackmain/models.py) and migrate 
those changes. Run the commands:

    python manage.py sqlmigrate amtrakmain 0001

   **NOTE!** 0001 is the number of the migration that was implemented. This doesn't affect the 
   database in any way, just shows you what is being done


### RAW SEQUEL COMMANDS WITH DJANGO

Soon. . .