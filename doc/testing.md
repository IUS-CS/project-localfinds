# LocalFinds - Testing

## Access and Execution
All tests can be found in the /tests directory in the root of the repository. 
All tests can be executed using the commands ``` make setup ``` and ```make test```. 

## Libraries Implemented
- **pytest** library is used to manage test execution, including fixtures that create temporary databases and simulate routes. 
- **Selenium** web-application is used for client-side browser testing by automating user interactions. 

## Scripts
- **```test_accounts.py```** thoroughly tests each function in the ```accounts.py``` model script which interfaces with the accounts database.
- **```test_posts.py```** thoroughly tests each function in the ```posts.py``` model script which interfaces with the posts database.
- **```test_routes.py```** thoroughly tests each route in the entry-point script ```app.py```. Additionally, **```test_routes.py```** includes integration testing between the HTML requests and the two databases (accounts and posts). This is done by making assertions regarding not only the HTML response, but also regarding the changes in the state of the temporary databases.
- **```test_client.py```** thoroughly tests the frontend browser UI and ensures system functionality. System testing will be included in this script with assertions referencing every component of our system.
