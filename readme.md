# fastapi_secrets. General description.
_'fastapi_secrets'_ is a fastapi project.
The project is created for **anonymous exchanging sensitive information in a safe way**.\
Each secret is created with a pass_key.\
Both pass_key and the content itself are encoded before saving them to the database.\
Each secret's pass_key has its lifetime (expiration date). The secret can't be read after the lifetime has expired.\
Each secret's content are destroyed after the first reading. It cannot be read by someone else later.\

# Running the project
1. install docker to your local machine if you have not already:
   https://docs.docker.com/get-docker/

2. Clone the project https://github.com/Marat-Shainurov/fastapi_secrets.git in your IDE.

3. Build a new image and run the project container from the root project directory:
   - docker-compose build
   - docker-compose up

4. Read the project's documentation (swagger or redoc format):
   - http://127.0.0.1:8000/docs/
   - http://127.0.0.1:8000/redoc/

5. Go to the main page on your browser http://127.0.0.1:8000/docs and start working with the app's endpoints.


# The project's structure
1. /app/database/ - package with main database settings. MongoDB is used as the database.
2. /app/endpoints/ - package with project endpoints.
3. /app/models/ - package with pydentic models settings.
4. /app/schemas/ - package with the pydentic/mongodb serializer.
5. /app/services/ - package with the project service functions.
6. /tests/ - testing package.
7. /main.py - main project file, where the FatsAPI app is instantiated.
8. /requirements.txt - main project dependencies.

# Testing
All the endpoint are covers by pytest test in /tests/test_main.py

# Security
CORSMiddleware settings are added to the app in main.py.
