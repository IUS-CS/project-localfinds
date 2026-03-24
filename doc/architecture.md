# LocalFinds - Architecture

## Overview
LocalFinds is a web application with a Flask backend written in Python, hosted via Render's cloud-based hosting. 
The backend serves HTML to the client’s browser and interacts with two SQLite databases: one for user accounts and one for posts. 

The overall system architecture is illustrated below:

![Overview](/doc/images/architecture/screenshot4.png)

## MVC 
The following Model/View/Controller (MVC) diagram visualizes how the client’s browser, Flask backend, and databases interact:

![MVC Diagram](/doc/images/architecture/screenshot3.png)

## Database Schemas
These diagrams represent sample schemas for the two databases:

![Accounts Database](/doc/images/architecture/screenshot1.png)
![Posts Database](/doc/images/architecture/screenshot5.png)

## Create Post Sequence
The diagram below details the sequence of actions that occurs when a user creates a post:
![Create Post Sequence](/doc/images/architecture/screenshot2.png)
