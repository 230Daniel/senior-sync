# Senior Sync

Repo for the code.

Jira: https://senior-sync.atlassian.net/jira/software/projects/SYNC/boards/1


# Frontend

The frontend is a React webapp, and will communicate with the backend via an API.

## Developing Frontend

These steps will start the frontend up locally so that you can interact with it on your machine. By default, it will try to talk to the backend on http://127.0.0.1:8000, so you will need to start the backend using the steps below.

1. Uninstall any old version of NodeJS and install NodeJS 22.12 LTS from https://nodejs.org/en/download/package-manager.
 
2. Check with `node --version` that you have node 22.12 installed and with `npm --version` that you have npm 10.9.0 installed.

3. In a terminal, cd into the `frontend` folder and run `npm install` to grab all the packages.

4. Run `npm run dev` to start up the frontend, and open the link to the local website.

When you make changes and save the file, the website will automatically re-compile and update in your browser.


# Backend

The backend is a RESTful API written with FastAPI, a Python package.
This means that it accepts GET, POST, PUT, PATCH, and DELETE requests from the frontend with machine-readable JSON inputs, and returns machine-readable JSON responses.

You can think of the backend as the actual logic of the system. If you wanted to, you could use the whole application by interacting only with the backend. The frontend is designed to interact with the backend for us however, and represent those interactions nicely.

## Developing Backend

These steps will start the backend up locally so that you can interact with it on your machine.

1. Install Python 3.12 from https://www.python.org/downloads/.

2. Check with `python --version` that you are using Python 3.12.

3. In a terminal, cd into the `backend` folder and run `python -m venv venv` to create a Python virtual environment.

4. Activate your virtual environment with `.\venv\Scripts\activate`.

5. Install packages with `python -m pip install -r requirements.txt`. If you get an error about Microsoft Visual C++ not being installed, follow the steps in this answer: https://stackoverflow.com/a/64262038.

6. Run `fastapi dev` to start up the backend on http://127.0.0.1:8000.

### Setting up Mongo Database on Windows

For a youtube tutorial on the following instructions please watch https://www.youtube.com/watch?v=c2M-rlkkT5o&t=1s.

1. Install Mongodb. Go to https://www.mongodb.com/try/download/community. Select the latest version, platform and package type. Click download.

2. Run the installer and follow the installation wizard (ensure that the checkbox install mongodb as a service is checked, and install mongodb compass is checked).

3. Install Mongodb shell AKA Mongosh. Go to https://www.mongodb.com/try/download/shell. Select the latest version, platform and package type. Click download.

4. Extract the Mongosh files from the downloaded zip file.

5. Open the Mongosh folder and navigate to the mongosh.exe file. ..\mongosh-2.3.7-win32-x64\mongosh-2.3.7-win32-x64\bin\mongosh.exe. Right click the file, go to properties and copy the file location.

6. Add the mongosh.exe file path to system variables and add to path under user variables.

7. Optional, install the VS code mongodb extension. Open VS code, go to extensions, search for MongoDB for VS code, install.


## Unit testing backend

The unit tests live in the `backend/tests` folder, and are written with Pytest. They use a mock MongoDB so you don't need a database to run them.

### Run tests

1. Install the `backend/tests/requirements.txt` requirements file with pip.

2. Cd into the `backend` folder.

3. Run `pytest` to run the tests.

### Coverage report

The coverage report shows which code paths have or haven't been tested.

1. Cd into the `backend` folder.

2. Run `coverage run --include=app/** -m pytest; coverage html` to generate the report.

3. Open `backend/htmlcov/index.html` in your browser to view the interactive report.

# Production Deployment (Linux only)

Production (non-development) deployment is done with Docker, so it can only be performed on a Linux system. Most developers don't need to worry about this, it will just be used to create the artefact for demos or publically accessible instances.

The Docker deployment also includes the MongoDB database and an admin panel accessible on `/mongo` with username `mongo` and password `quickly-obtuse-situation`.

## From local repository

1. Install docker and the docker compose plugin.

2. Get an SSL certificate for the domain your Linux system is reachable through. (I recommend [certbot](https://certbot.eff.org/instructions?ws=other&os=pip) with [acme-dns](https://github.com/acme-dns/acme-dns-client))

3. Edit the `frontend > ports` section of `docker-compose.yml` to set the external ports for the frontend to listen on. For example `8443:443` will point port 8443 on the host to port 443 (HTTPS) in the container.

4. Edit the `frontend > volumes` section of `docker-compose.yml` to make your SSL certificates accessible from within the frontend container.

5. Edit the `ssl_certificate` and `ssl_certificate_key` lines of `nginx.conf` to provide nginx the paths to the SSL certificate files within the container.

> If you're not using SSL certificates, remove references to SSL from `nginx.conf`.

6. Run `docker compose up -d --build` to build and start the containers.

## From Docker Hub

The images are pushed to a private Docker Hub repo, ask for access if you need it. Images are built for amd64 and arm64.

1. Follow steps 1 to 5 above, but use `docker-compose-prebuild.yml` instead. You don't need to clone the whole repository, you just need that single file.

2. Log in to docker hub with an account that has access to the private repo 230daniel/private. `docker login`.

3. Run `docker compose -f docker-compose-prebuilt.yml up -d` to download and start the containers.

4. To update the containers when a new CI run on the main branch is completed, run:

```
docker compose -f docker-compose-prebuilt.yml down
docker compose -f docker-compose-prebuilt.yml pull
docker compose -f docker-compose-prebuilt.yml up -d
```
