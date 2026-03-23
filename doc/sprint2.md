# LocalFinds - Sprint 2 Ceremony Minutes
  
Date: 2026-03-05

Members present:

* Aaron O'Brien
* Mark Berkey
* Gayani Don Francis

Minutes: 120
  
## LocalFinds

This sprint, we completed:

* As a user, I want LocalFinds to be deployed on Render so that I can access it.
* As a user, I want to be able to log in so that others know who I am.
* As a user, I want to be able to make an account so that others know who I am.
* As a user, I want LocalFinds to be styled in a way that is easy to read and navigate.
* As a user, I want my account credentials to be stored in a database so that they are not deleted.
* As a user, I want to be able to store account credentials in the database and validate my session so that they are not deleted and I cannot be impersonated.
* As a user, I want to insure through executing tests that the account database functions work properly so that my credentials are secure.
* As a team member, I want to access doc/contributing.md so that I know the AI policy and tools I should employ.
* As a team member, I want to access doc/sprint1.md so that I can reflect on the previous sprint.


Here are screenshots of the website in its current state:

![Home Page](/doc/images/sprint2/screenshot1.png)
![View Post Page](/doc/images/sprint2/screenshot2.png)
![Login Page](/doc/images/sprint2/screenshot3.png)
![Create Account Page](/doc/images/sprint2/screenshot4.png)
![Home Page Signed In](/doc/images/sprint2/screenshot5.png)
![Create Post Page](/doc/images/sprint2/screenshot6.png)

## Retro

### Good

* SQLite made user database creation simple, especially when using the posts database as a reference.
* Flask made routing additional webpages simple.
* Testing the user database functions were simple when using the posts database functions as a reference.

### Bad

* CSS is difficult to perfect.
* Website does not look correct on mobile. 

### Actionable Commitments

* As a team, we will continue making progress on this website. Focusing on styling new pages and implementing the ability to update/delete posts and accounts. Furthermore, testing will be implemented for the routes and passwords will be encrypted in the accounts database.

## Next Sprint Planning

Points | Story
-------|--------
3      | As a team member, I want to access doc/architecture.md so that I know what components the website consists of and how they interact.
1      | As a team member, I want to access doc/sprint2.md so that I can reflect on the previous sprint.
3      | As a user, I want my password to be encrypted in the backend so that my credentials are secure.
3      | As a user, I want to be able to delete posts so that I can
3      | As a user, I want to be able to edit posts so that I can correct mistakes.
3      | As a user, I want to be able to delete my account so that I can
3      | As a user, I want to be able to edit my account so that I can correct mistakes.
5      | As a user, I want to insure through executing tests that the routes behave correctly so that I know the website is behaving properly.
3      | As a user, I want a styled create account page so that it is easily accessible.
3      | As a user, I want a styled login page so that it is easily accessible.
