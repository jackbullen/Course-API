# course-API

This is a Django application programming interface (API) that I will use with a front end application. I would also like to modify it to include a Student model and make a course management system.

Files of interest are

- /courses_api/urls.py links the views with urls in the main project

- /courses/urls.py links the view with urls for the api endpoints

- /courses/views.py implements several class based views using the custom APIView and generics ListView and RetrieveView

- models.py defines all entities and relationships

- import_models.py loads the course objects from a json file into the django apps postgresql database. It uses lists of fields to filter the raw data making the code terse