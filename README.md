# Silva Permaculture

The idea behind the project is that of creating a space for the users who are looking for  useful information about plants
and trees that can restore and improve the life of the soil and enhance the environment. <br/>

The users can help improve the database, by registering to the website, and then start adding plants and useful information about them.

## User Experience

I created the site as a tool for anyone, from professional gardeners, permaculture designers or any professional, semi-professionals, hobbyists or casual gardeners that want to be able to find plants and trees that can restore, improve and enhance degraded or baren soils and created lush environments rich in life.

My goal in mind when starting the building of the app was that it has to be simple to interact with, but at the same time offering functionalities to be able to search, register, add and edit plants and trees.

The app had to be user friendly and colorful, and the information needed to be displayed in eye-friendly mode, so that if the user wanted to read more about something in particular, they could press a button and the whole text of that area would be displayed. 

**User stories**

In general, as a user interested in plants and trees that is searching for information, they will want to know what this site is about and what they can learn from it.<br/>
They will expect to be able to view and find information about  plants or trees, or even search for a plant in a free form manner.

**Professional/Semi-Professional User**

Besides the general information, they will also want to know the properties of a particular plant or tree, find out about specific habitats, and most important, the nutrients
that a plant can gather from the soil and/or if that plant/tree can support the growth of other plants/trees. 
Also, they will want to be able to search for plants based on specific nutrients.

They will also be able to register and add or edit their own plants and trees, thus sharing valuable information with the community.
They will have access to their account page, where they can change their registration username and update their profile picture.

**Hobbyst User**

They will share a passion for gardening and they will want to find more about how specific plants can improve the soil and environment of their gardens.
They will expect to be able to search for information and also will want to register to be able to add or edit their own plants and trees.

They will have access to their account page, where they can change their registration username and update their profile picture.

**Casual User**

They will browse the website to find what it is about and if they will find some useful information, they will apply it into their own gardens.
They may register on the site to share some information.

**Administrator**

I wanted the functionality to edit a plant or remove it from the database to be possible for the user that registered to the site and added that plant or tree.

## Features

**Existing Features**

1. Basic Registration(Username and Password) - Allows users to register to the site by filling the registration form.
  -Registration form - When submitting the form, the users will be prompted if the username is taken and to choose another one and if the passwords match; A flash message will prompt the user that registration was successful and they can login.
   
2. Login - Allows users to login to the site and have access to the account page, add plant page by going to the login page and fill the form with their username and password. The form will warn the user if their credentials mismatch or forgot to fill a field and also prompt with successful message if the login was correct. 

3. Search - Allows users, regardless if they are registered or not, to search for a plant or tree by typing a common name or scientific name. The search allows users to also find plants based on medicinal uses, habitats or other information, by typing into the main search field.

4. Filtered search - Allows users to find plants based on filters by selecting a nutrient and nitrogen fixator/nurse plant.

5. Account page - Allows users to change their registered username and also update a new profile picture.
6. Add plant - Allows users to add a plant to the database by filling the add new plant form. The form will be guiding the user will useful information and warn him when something is missing or a successful message when the plant was added to the database.

7. Edit their plant(s) - Allows users to edit a plant they have added. This feature is available if the user navigates to the plant that they have added. They have the option to go back to the plant if they don't want to edit it or if they edited it, they will be prompted with a successful message and return to that plant page.

8. Delete their plant(s) - Allows the user to delete a plant by navigating to a plant they have added and pressing a Delete button. To make sure the user doesn't delete by accident a plant, a modal window will appear that will ask the user if they are sure they want to delete that plant or not.

9. View plants page - Allows user to browse for the already published plants in an easy to read manner.

10. View individual plant - Allows user to find more information about a specific plant by clicking the button **Read More** which will take them to that particular plant.

11. Find more information about a topic - The plants added can have lots of information, but just a small portion of the content can be read for good UX. If they want to find more, they will have to click the **Read More** button. A modal will show the whole information regarding that topic.


**Features left to implement**

1. Registration by email - This will allow users to be registered by email.

2. Forgot password? - If feature 1 is implemented, this will allow users to request a new password to login again to the site.

3. Security check - If feature 1 is implemented, this will allow to check for the validity of the email address, by sending to that registered email address a confirmation link.

4. Plants cards can show the user that added that plant and when exactly.

5. Order the plants by date added or nutrients

## Technologies Used

##### Front End

* Bootstrap [Bootstrap 4](https://getbootstrap.com/)

    Bootstrap is used in the project to create the User Interface and for better User Experience.
    The fluid grid and CSS Bootstrap classes, allows elements to be display in a harmonious way on different devices.

* CSS3
    
    I used CSS3 to add a personal styling touch to different elements and to better represent elements.
    
* Bootstrap Select [Bootstrap-select](https://developer.snapappointments.com/bootstrap-select/)
    
    For a better design and functionality for the multiple-select elements.

* Flask - A Python micro-framework [Flask](http://flask.pocoo.org/) and [Python](https://www.python.org/)

    Flask and Python were used to create the logic and functions for the web app.
    
* [SQLite](https://sqlite.org/index.html) and [SQLAlchemy](https://www.sqlalchemy.org/)

    SQLAlchemy was used to for its object-relational mapping together with SQLite for creating the tables(objects)
    into a more Pythonic way, to represent the User, Plants, Nutrients and the relationship between them.
    SQLite was used for development.
*[Heroku PostgreSQL](https://www.heroku.com/postgres)
    Switched from file based SQLite to production database PostgreSQL to also avoid heroku erasing the SQLite file db.

    
* [Elasticsearch](https://www.elastic.co/)

     Used for creating a full-text search. 

* [Google Fonts](https://fonts.google.com/)

     To represent the text in a more beautiful way.
     
* [FontAwesome](https://fontawesome.com/)

     To add flavour to different parts of the project and to better represent ideas.
      
* [LogoMakr](https://logomakr.com/)
        
     To create the logo for the site.     
     
## Database schema

1. User
     ````   
      CREATE TABLE user ( id INTEGER NOT NULL, 
      username VARCHAR(20) NOT NULL, 
      password VARCHAR(60) NOT NULL, 
      image_file VARCHAR(20) NOT NULL,
      PRIMARY KEY (id), 
      UNIQUE (username) )  

2. Plants
    ````
        CREATE TABLE plants ( id INTEGER NOT NULL, 
        common_name VARCHAR(40) NOT NULL, 
        botanical_name VARCHAR(80) NOT NULL,
        short_description TEXT NOT NULL,
        medicinal TEXT NOT NULL, other_uses TEXT NOT NULL, 
        habitats TEXT NOT NULL,
        region TEXT NOT NULL, 
        image_file VARCHAR(20), 
        date_added DATETIME NOT NULL,
        user_id INTEGER NOT NULL, 
        PRIMARY KEY (id),
        UNIQUE (botanical_name), 
        FOREIGN KEY(user_id) REFERENCES user (id) )
        
3. Dynamic Nutrients Accumulators
    ````
        CREATE TABLE "DNA" ( id INTEGER NOT NULL,
         element VARCHAR(15),
         PRIMARY KEY (id) )

4. Nitrogen Fixator/Nurse
    ````
        CREATE TABLE "NFN" ( id INTEGER NOT NULL,
         plant_extra VARCHAR(40),
         PRIMARY KEY (id) )
         
5. Many to Many relationship table Plants and Nutrients
    ````
        CREATE TABLE plants_dna ( plants_id INTEGER NOT NULL,
         dna_id INTEGER NOT NULL,
         UNIQUE (plants_id, dna_id),
         FOREIGN KEY(plants_id) REFERENCES plants (id),
         FOREIGN KEY(dna_id) REFERENCES "DNA" (id) )  

6. Many to Many relationship table Plants and Nitrogen Fixator/Nurse
    ````
        CREATE TABLE plants_nfn ( plants_id INTEGER NOT NULL,
        nfn_id INTEGER NOT NULL,
        UNIQUE (plants_id, nfn_id), FOREIGN KEY(plants_id) REFERENCES plants (id), 
   
   
##### Example of a plant model

    ````
    >>> from silvapermaculture import *
    >>> from silvapermaculture.models import *
    >>> plant = Plants.query.get(1)
    >>> plant
    Plants('Comfrey', 'Symphytum officinale', 'A member of the borage family, comfrey - Symphytum spp. is native to Europe and Asia and there are 40 recorded species throughout that region. The plant most commonly referred to and used in gardens is Russian comfrey - Symphytum x uplandicum, a naturally occurring hybrid of two wild species: common comfrey - Symphytum officinale and prickly comfrey - Symphytum asperum.
    
    A few centuries back, the hybrid Symphytum x uplandicum came to the attention of Henry Doubleday (1810-1902) and he widely promoted the plant as a food and forage crop. Years later, and after two world wars, Lawrence D Hills (1911-1991) would continue Henry Doubleday's Comfrey crusade.
    
    In the 1950s, Hills developed a comfrey research program in the village of Bocking, near Braintree in the UK. The original trial site is on the plot of land now occupied by the Doubleday Gardens housing development. Lawrence Hills lived at 20 Convent Lane just around the corner of the trial site. At this site, Hills trialed at least 21 comfrey 'strains', each one named after the village Bocking. Strain 14 was identified as being the most nutrient rich, non-seeding strain and 'Bocking 14' began its journey into gardens far and wide across the world. ', ' Comfrey has been cultivated, as a healing herb since at least 400BC. The Greeks and Romans commonly used comfrey to stop heavy bleeding, treat bronchial problems and heal wounds and broken bones.
    Poultices were made for external wounds and tea was consumed for internal ailments. Comfrey has been reported to promote healthy skin with its mucilage content that moisturizes and soothes and promotes cell proliferation.
    This plant is my first port of call if ever I need to dress a wound. Simply take a few leaves brush them together to remove the hairs and wrap them around the wound and apply light pressure. It's incredibly effective at stopping the bleeding, reducing the pain and healing the wound.', '[Nitrogen, Potassium, Calcium, Magnesium, Iron, Silicon]', '[Nitrogen Fixator]' )
    >>> plant.author
    User('Samuel', 'b09c46c970d0c348.jpg')
    >>> plant.dna
    [Nitrogen, Potassium, Calcium, Magnesium, Iron, Silicon]
    >>> plant.nfn
    [Nitrogen Fixator]
    >>> plant.medicinal
    " Comfrey has been cultivated, as a healing herb since at least 400BC. The Greeks and Romans commonly used comfrey to stop heavy bleeding, treat bronchial problems and heal wounds and broken bones.\r\nPoultices were made for external wounds and tea was consumed for internal ailments. Comfrey has been reported to promote healthy skin with its mucilage content that moisturizes and soothes and promotes cell proliferation.\r\nThis plant is my first port of call if ever I need to dress a wound. Simply take a few leaves brush them together to remove the hairs and wrap them around the wound and apply light pressure. It's incredibly effective at stopping the bleeding, reducing the pain and healing the wound."
    >>> plant.common_name
    'Comfrey'
    >>> plant.botanical_name
    'Symphytum officinale'
    >>>exit()

## Testing

##### 1.Routes testing

    i. Testing the routes links from menu(home, plants, add plant, account).
    ii. Accessing  different routes from the current page(for example from plants to account) and verify that it access the desired route.

##### 2.Database  

    i. Tested in terminal the User model and trying to access them.
         
            >>>from silvapermaculture import db
            >>>db.create_all()
            >>>from silvapermaculture import User
            >>>user_1 = User(username="John Doe", password="Password")
            >>>db.session.add(user_1)
            >>>db.session.commit()
            >>>find_user = User.query.first()
            User('John Doe', 'b09c46c970d0c348.jpg')
            >>>exit()
            
    ii. Testing in terminal the Plants models and accessing them
            
            >>>from silvapermaculture import db
            >>>from silvapermaculture import *
            >>>plant_1 = Plants(common_name="Test 1", botanical_name="Test 1 Latin", short_description="Lorem ipsum", medicinal_use="LoremLoremIpsum", other_uses="Second lorem", habitats="Testiing", region="Europe", user_id=1)
            >>>db.session.add(plant_1)
            >>>db.session.commit()
            >>>find_plant = Plants.query.first()
            >>>find_plant
            [Plants('Test 1', 'Test 1 Latin', 'Lorem ipsum', 'LoremLoremIpsum', 'Second lorem', 'Testiing', 'Europe')]
            >>>exit()
    
    iii. Adding and testing in terminal the Dynamic Nutrients Accumulator and Nurse/Nitrogen Fixator plant models.
    
##### 3. Register form
    
    i. Go to "Register" page from the menu or go from the link "register" from the home page.
    ii. Try to submit the empty register form and verify that an error message from Flask forms appears with the required input.
    iii. Try to submit the register form with different passwords and verify that a relevant warning message appears.
    iv. Try to submit the register form with the same username as one already existing in the database and verify that a relevant warning message prompts the user to choose another one.
    v. Try to submit the register form with all inputs valid and verify that a successful registered message appears.
   
##### 4. Login form

    i. Go to "Login" page from the menu.
    ii. Try to submit the empty login form and verify that an error message from Flask forms appears with the required input.
    iii. Try to submit the login form only with the user name and verify that a relevant warning message appears.
    iv.  Try to submit the login form only with the password and verify that a relevant warning message appears.
    v. Try to submit the login form with all inputs valid and verify that a successful logged in message appears that redirects to the home page.
    
##### 5. Add a new plant form
    
    i. Go to "Login" page and login with credentials.
    ii. Go to "Add a plant" page.
    iii. Try to submit the empty form and verify that an error message from Flask forms appears with the required input.
    iv.  Try to submit the form only with one valid of the required inputs (the first 4) and verify that a relevant warning message appears.
    v.  Try to submit the form only with one valid of the required inputs (the first 4) and verify that a relevant warning message appears.
    vi. Try to submit the form only with two valid of the required inputs(the first 4) and verify that a relevant warning message appears.
    vii. Try to submit the form only with three valid of the required inputs(the first 4) and verify that a relevant warning message appears.
    viii. Try to submit the form with all the required inputs valid and with a .txt file upload for the plant's image and verify that a relevant warning message appears.(Applicaton only allows extensions jpg and png)
    ix. Try to submit the new plant form with all inputs valid and verify that a successful added plant message appears and redirects the user to the Plants page.
    
##### 6. Edit a plant form
    
    i. Go to "Login" page and login with credentials.
    ii. Go to Plants and select a plant that you added.
    iii. Click "Edit" button and verify that it access the "Edit" page.
    iv. If no update is required, click the button "No update? Go back to plant" and verify that it navigates to the plant wanted to be edited.
    v. Try to submit the empty form and verify that an error message from Flask forms appears with the required input.
    vi.Try to submit the form only with one valid of the required inputs (the first 4) and verify that a relevant warning message appears.
    vii.Try to submit the form only with one valid of the required inputs (the first 4) and verify that a relevant warning message appears.
    viii. Try to submit the form only with two valid of the required inputs(the first 4) and verify that a relevant warning message appears.
    ix. Try to submit the form only with three valid of the required inputs(the first 4) and verify that a relevant warning message appears.
    x. Try to submit the form with all the required inputs valid and with a .txt file upload for the plant's image and verify that a relevant warning message appears.(Applicaton only allows extensions jpg and png)
    xi.Try to submit the edit plant form with all inputs valid and changed from previous ones and verify that a successful update plant message appears and redirects the user to that particular plant page.
    
##### 7. Delete a plant

    i. Go to "Login" page and login with credentials.
    ii. Go to Plants and select a plant that you added.
    iii. Click "Delete" button and verify that a modal with a warning message pops up.
    iv. Click "Close" button and verify that the modal dissapears if I don't want to delete the plant.
    v. Click "Delete" button and verify that a successful message appears and user is redirected back to the Plants page.
    
##### 8. Search form

    i. Go to "Plants" page.
    ii. Type in the search form an already existing plant from the database and verify that it redirects to the results page and displays the plant found.
    iii. Type in the search form an inexistent plant and verify that it returns a 404 page.
    iv. Type in the search form a medical condition (ex. arthritis) and verify it returns the result page with the matching plant(s).
    v.  Type in the search form a medical condition that is not present in any plant in the site's database and verify it returns a 404 page.
    
##### 9. Filtered search form

    i. Go to "Plants" page.
    ii. Click the search button without selected items for filtering search and verify that a warning message appears.
    iii. Select only specific nutrients and verify returned results.

##### 10. Account page

    i. Test to access account route without being logged-in and verify that it redirects to login page and a warning appears.
    ii. Login and go to account page.
    iii. Type in a username that already exists in the DB and verify that a warning message appears.
    iv. Type a different username and verify that a success message appears. 
    v. Upload a different profile pic with other extension than allowed jpg, png and verify that a warning message appears.
    vi. Upload a different profile pic and verify that a success message appears.  
    vii. Go to "Logout" and verify that it redirects to home page and user is logged-out.

##### 11. Responsivness

    All the templates and elements of the app were tested for mobile-first approach.

## Installation


__Local installation__

    i. First clone the project:
        https://github.com/Walachul/SilvaPermaculture.git

    ii. To start developing the project:
        Make sure you have Python 3.6.

        Create a virtual environment in Windows:
            Navigate to where the project folder is and run:
            python -m venv venv 
        Activate the venv:
            Navigate to venv and inside run:
            C:\Python\Example\venv>Scripts\activate
        If successfuly, you should see the name of the virtual environment in curly braces in the front of the path:
        (venv) C:\Python\Example\venv>
        To install packages:
        Navigate to the home folder:
        (venv) C:\Python\Example> pip install requirements.txt

 **Please note that app requires the setup of environment variables.**

To setup of the following variables in Windows environment variables can be done like this:

        Navigate: Control Panel > System > Advanced system settings > Environment Variables > 
        add new > SECRET_KEY; DATABASE_URL ; ELASTICSEARCH_URL
        To get a SECRET_KEY number:
        Example: in CMD in python interpreter:
            >>>import secrets
            >>>secrets.token_hex(16)
            '84b8fec8da83b405db0ea64be18823d3'
            >>>exit()

Install elasticsearch and to see it running go to http://localhost:9200.

        And in Environment variables :
        ELASTICSEARCH_URL=http://localhost:9200

To start the app:
     (venv) C:\Python\Example> python run.py

## Deployment to Heroku
[Install Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli#download-and-install)

###### Commands

    (venv) C:\Python\Example>heroku login //for log in to Heroku
    (venv) C:\Python\Example> heroku apps:create example-app // need of unique app name

__To add Heroku Hobby-dev PostgreSQL to the project__:

    (venv) C:\Python\Example> heroku addons:add heroku-postgresql:hobby-dev

OR you can add this addon by going to

     heroku dashboard of your app > resources tab and searching for Heroku Postgres

__Add addon elasticsearch__

    heroku addons:create searchbox:starter

    However, this addon will be available if you add your credit card. You are not billed.

__Set ELASTICSEARCH_URL env variable in Heroku:

    To set the env variable ELASTICSEARCH_URL from SEARCHBOX_URl:

    (venv) C:\Python\Example>heroku config:get SEARCHBOX_URL
    <this_is_going_to_be_the_url_for_elasticsearch_url>
    copy it
    (venv) C:\Python\Example>heroku config:set ELASTICSEARCH_URL=<this_is_going_to_be_the_url_for_elasticsearch_url>

__You can view/edit config vars from the Settings window of the app.__

__If you cannot use the elasticsearch functionality or get wierd errors after implementation__
    
    1. Go to Resources Tab of the app and open SearchBox ElasticSearch.
    2. In the new window of dashboard.searchly.com, go to Dashboard menu and access indices.
    3. Create a new Index for the app.
    4. This will initialize the elasticsearch and will create the new indices for your database and tables.

__Procfile__

    web: flask db upgrade; gunicorn run:app

__Final steps for deployment__

    git commit -a -m "deployment to heroku changes"
    git push heroku master

__If you encounter errors and the app is not running__

    Hit the More button near the Open app > access view logs
