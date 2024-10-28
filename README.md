# Talriz
CSE 312 Project. Project will focused around creating a marketplace, this will include allowing users to sell items for certain prices and also include auction system. Future things could also be creating a tinder like site where we swipe right and left for items from certain categories.

Languages and Frameworks to know
Python
Html
CSS
JS
Django
MYSQL
(Possible React TBD)


GIT things to know
Before starting a new branch make sure the new branch is branched from dev
and to git fetch and git pull any new changes.
ex. Go to dev then (git fetch origin dev -> git checkout <YOUR BRANCH> -> git merge origin/dev -> handle all conflicts then git add . -> git commit -m "Message") 
If you need to push your branch into dev then.
ex. Go to dev then (git pull origin dev, git merge <YOUR BRANCH> , Fix any conflicts and be sure to do git add and git commit and push)

It will let you know if there are any issues with merging or pulling. You have to find where the issue is


To start the server using the database this assumes you created a databsae called talriz_db and created a user named lejimene or just changing user
in docker yml file to another valid user. In some cases you may need to change port in yml for db to 3307:3306 instead of 3306:3306.
Then do
docker-compose up --build
After wards do CRTL C to end and uncomment the command manage.py migrate and comment rest. Then do the same for makemigrations
After completing both do comment out everything but the python manage.py runserver
Below is the link deployment
http://localhost:8080/
