# Rail Road Poject - Optimizing the AMTRAK rail road system

### | PROFESSOR INSTRUCTIONS | RUNNING SERVER | MIGRATIONS |

### | SQL COMMANDS | ADMIN PAGE | READY TO WORK? |

### | RAW SQL COMMANDS WITH DJANGO | BOOTSTRAP |


**NOTE! please read the following first and make no changes to the code yet.** 
**Once done reading and implementing go to READY TO WORK? section**

**NOTE! These commands can be different on windows, be careful**


## ER Diagram for Rail Road System

![ER-Amtrak](https://github.com/enzoames/AMTRAK/blob/master/src/amtrak/ER_AMTRAK.png?raw=true)
    by: Enzo Ames

## Flowchart for RailRoad System
![Flowchart](https://github.com/enzoames/AMTRAK/blob/master/src/amtrak/Flowchart.jpg?raw=true)
    by: Tasnim Imani

### PROFESSOR INSTRUCTIONS

The URL of our projet: https://oceanic-gecko-166900.appspot.com/ [**Work In Progress**]

* The src folder is where our entire project lives
    * Inside amtrak you will find our different django applications
        * amtrak folder (again) - In this folder you will see different python files that are essential
            to deploy Django and our database. Most of the code is already presented to you when you start
            a Django project.
            
        * amtrakmain folder - This is the application where the 'Searching Avaiable Train' feature lives
            * management folder - This is where we initially populate our database
                * populate_db.py - This file contains all the code that populates our database with
                    initial inputs for the tables Train, StopsAt, Station, SeatsFree, and Segment.
                    **CURRENT WORK IN PROGRESS** Since we have our server running on the google cloud
                    platform we need to recreate the tables that once existed in our inital sqlite3 database
                    to the Mysql database provided to us by google. For example, Seatsfree table is very 
                    extensive therefore the code in this file will take care of inputting every row.
            * migrations folder - This folder keeps track of all our migrations. Any change we make to
                an attribute of table will be recorded here. Django takes care of keeping this folder
                updated. Refer to MIGRATIONS section for more information 
            * templates folder - This folder contains html files that will be render to the main page
                depending on the user input. If the user tries to search for an unavailable train, we will
                display the corresponding html file.
            * models.py - This is the most important python file in our project. This is where we instantiate
                all our database tables. Here we set the values of each attribute and the relation from one
                table to another.
            * forms.py - The user is presented with a form in which he will have to fill out in order for us
                to proccess his request. This file is where the structure of the form is created. The form
                follows grabs information from models.py.
            * views.py - In this file we do most of our computation. When a user fill out the form, this takes
                care of processing the request and displaying the right information. Nothing is save to
                database since this feature only allows for the user for search if train is available.
            * init.py, admin.py, app.py, tests.py, urls.py - little or some work was done in these files.
                not too important in the bigger picture.  

        * homepage folder - Contains similar files to amtrakmain but are not populated with much code
            * templates/homepage folder - Is where our base.html lives. This file contains our boostrap content
                * base.html - This file contains the basic structure and apperance of our site. You will
                    notice that other html files accross our application __extend__ this file, bc we want
                    maintain the structure/look constant, hence the name __base__

        * purchase folder - This is where the 'Book Ticket' feature lives
            * views.py - This file takes care of dealing with the request coming from the user when it 
                wants to book a ticket. This is where we check for free seats, compute fare, compute train,
                arrival dates, and save to database. Once user has checked the availability of train, it will
                proceed to this form and fill out the required information to purchase ticket
            * remaining python file have little or no importance. 

        * static/css - where some other css files created by me live, nothing much to see here. 

    * static_cdn - this is where the html, css, javascript for the Django admin lives. This was provided by
        the framework at the moment of creation


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
DJANGO to start a **migration** then we will see the changes in our admin page.

As we move forward we will create more tables and make more changes. In order for you tell django 
that the changes you made to **models.py** need to be added to our database, you do:

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
doing every time you are making changes to the database **(amtrackmain/models.py)** and migrate 
those changes. Run the commands:

    python manage.py sqlmigrate amtrakmain 0001

   **NOTE!** 0001 is the number of the migration that was implemented. This doesn't affect the 
   database in any way, just shows you what has been done


### READY TO WORK

Once you finished going over the above, and you think youre ready to work on the 
project. **create a branch**. If you're not sure how to do so following these commands:

    git pull 

    note - output should say 'up to date' or download the most recent code for you

    git branch

    note - your ouput should be: * master
    then,

    git branch [name initals here]-work

    example:

    git branch ea-work

    then again,

    git branch

    output should be: [your initials here]-work  * master

    then,

    git checkout ea-work

    should say you switched to your branch. Double check by doing 'git branch' 
    should highlight you branch

At this point now you can do work and start writing some code. **if any of the above** 
**didn't work, google the error -- how to create a branch in git**. When you're finish with your work 
and it **compiles**:

    git status

    this shows all the modified files

    git add -A

    git commit -m 'some meaninful message of what you worked on'

    git checkout master

    should say switch to master branch. to double check do: 'git branch' and shows the branch you're on

    git pull 

    git merge [initials here]-work

    note - the name of your branch of course.

    git push

Thats it ! git push sends your code to gihub, once done you can delete your branch if needed.
Now, whenever you want to work again repeat the same proccess. **work on your branch, not MASTER**

If you have any problems catch me before or after class


### RAW SEQUEL COMMANDS WITH DJANGO

To enter the shell

    python manage.py shell

    from amtrakmain.models import <name_of_table_here>

You can also create tables here, ex: Train.objects.create()

Follow the django documentation to see all availble commands

### BOOTSTRAP

Bootstrap is a front-end framework to make building web applications a lot easier and faster.
It provides you with the necessary files to configure the front end

