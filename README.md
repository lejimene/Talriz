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


To start the server using the database assuming you created 
a database on mysql
docker-compose up -d
To update any database stuff like migrating stuff do that command and
python manage.py makemigrations
python manage.py migrate