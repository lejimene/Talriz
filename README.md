# Talriz
CSE 312 Project. Project will focus around creating a marketplace, this will include allowing users to sell items for certain prices and also include auction system. Future things could also be creating a tinder like site where we swipe right and left for items from certain categories.

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


To start the server using the database this assumes you created a database called talriz_db and created a user named lejimene or just changing user
in docker yml file to another valid user. In some cases you may need to change port in yml for db to 3307:3306 instead of 3306:3306.
Then do
docker-compose up --build
After wards do CRTL-C to end and uncomment the command manage.py migrate and comment rest. Then do the same for makemigrations
After completing both do comment out everything but the python manage.py runserver
Below is the link deployment
http://localhost:8080/

## Part 3 Objective 3 (Dark Mode)
The Dark Mode feature allows users to toggle between a light and dark theme on the website for improved readability 
and a more comfortable viewing experience, especially in low-light environments. This feature enhances user interaction by providing
a visually distinct and customizable interface.

### Key Features:
* Toggle Button: Users can switch between light and dark modes by clicking the "Toggle Dark Mode" button located in the nav bar.
* Persistent Theme Preference: The user's theme preference is saved in the browsers "localStorage", ensuring the selected theme persists across page reloads and future visits.
* Automatic Theme Update: When dark mode is activated, the page's background and text color adjust accordingly, with the text becoming light-colored for better contrast against dark backgrounds.
* Image Adjustment: Images that are typically dark (such as the main marketplace icon) are automatically adjusted, ensuring visibility and maintaining the overall design consistency in dark mode.
* Accessibility: The dark mode feature ensures text and UI elements maintain high contrast for readability and accessibility.
### Testing Procedure (Dark Mode)
1. Start your server using docker compose up
2. Open the browser and navigate to http://localhost:8080/
3. Create an account and login to the site
4. Once brought to the main marketplace page, verify that the initial theme of the website is in "light mode"
5. Locate the "Toggle Dark Mode" button at the top navigation bar
6. Click the "Toggle Dark Mode" button once
   1. Verify that most backgrounds are swapped to dark colors except the "Sign Out" and "Toggle Dark Mode" buttons
   2. Verify that most text is swapped to lighter colors such as white 
   3. Verify that the main website icon is swapped to white
7. Refresh the page
   1. Ensure that the current theme persists through the reload
8. Restart the server with "docker compose restart"
9. Refresh the page 
   1. Verify that the current theme persists through the restart and reload
10. Click the "Toggle Dark Mode" button again
    1. Verify that the backgrounds are swapped back to the initial "Light Mode" state colors
    2. Verify that the text is swapped back to the initial "Light Mode" state colors (black)
    3. Verify that the main website icon is swapped back to black

