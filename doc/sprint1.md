# LocalFinds - Sprint 1 Ceremony Minutes
  
Date: 2026-02-16

Members present:

* Aaron O'Brien
* Mark Berkey
* Gayani Don Francis

Minutes: 120
  
## LocalFinds

This sprint, we completed:

* As a user, I want a home page so that I can see an overview of LocalFinds and recent posts.
* As a user, I want a view post page so that I can read individual posts in detail.
* As a user, I want a post creation page so that I can add new posts to LocalFinds.
* As a user, I want the posts to be stored in a database so they can be displayed and not deleted.
* As a user, I want to be able to store posts in the database so that they are no deleted.
* As a user, I want to ensure through testing that the post database functions work properly so that I can be assured the posts will be saved.
* As a user, I want to be able to build or test LocalFinds so that I know it is working properly.
* As a team, we want a .gitignore file so that unnecessary files are not contributed to the repository.
* As a team, we want an AUTHORS file so that contributions are credited properly.
* As a team, we want an MIT License so that the project has a clear open-source license.
* As a team, we want a README.md so that users and developers understand how to use and contribute to the project.
* As a team, we want doc/organization.md so that project organization and responsibilities are documented.
* As a team, we want doc/proposal.md so that the project proposal and plan are documented.
* As a user, I want the home, view post, and create post pages to have full functionality so that I can interact with LocalFinds as intended.

Here are screenshots of the website in its current state:

![Home Page](/doc/images/sprint1/screenshot1.png)
![View Post Page](/doc/images/sprint1/screenshot2.png)
![Create Post Page](/doc/images/sprint1/screenshot3.png)

## Retro

### Good

* Working with SQLite was a joy.
* Flask made routes easy to understand and implement.
* Tests pass and website is functional.

### Bad

* Makefile too a while to understand but is an amazing tool.
* Pytest was difficult to implement as temporary databases had to be generated.
* Routing individual posts was complicated to get working.

### Actionable Commitments

* As a team, we will continue making progress on this website. Focusing on styling and implementing an accounts database where users can create accounts and log into a session.

## Next Sprint Planning

Points | Story
-------|--------
3      | As a user, I want LocalFinds to be deployed on Render so that I can access it.
5      | As a user, I want to be able to log in so that others know who I am.
5      | As a user, I want to be able to make an account so that others know who I am.
5      | As a user, I want LocalFinds to be styled in a way that is easy to read and navigate.
1      | As a user, I want my account credentials to be stored in a database so that they are not deleted.
1      | As a user, I want to be able to store account credentials in the database and validate my session so that they are not deleted and I cannot be impersonated.
1      | As a user, I want to insure through executing tests that the account database functions work properly so that my credentials are secure.
1      | As a team member, I want to access doc/contributing.md so that I know the AI policy and tools I should employ.
1      | As a team member, I want to access doc/sprint1.md so that I can reflect on the previous sprint.
