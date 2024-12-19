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

5. Install packages with `pip install -r requirements.txt`. If you get an error about Microsoft Visual C++ not being installed, follow the steps in this answer: https://stackoverflow.com/a/64262038.

6. Run `fastapi dev main.py` to start up the backend on http://127.0.0.1:8000.


# Production Deployment (Linux only)

Production (non-development) deployment is done with Docker, so it can only be performed on a Linux system. Most developers don't need to worry about this, it will just be used to create the artefact for demos or publically accessible instances.

## From local repository

1. Install docker and the docker compose plugin.

2. Get an SSL certificate for the domain your Linux system is reachable through. (I recommend [certbot](https://certbot.eff.org/instructions?ws=other&os=pip) with [acme-dns](https://github.com/acme-dns/acme-dns-client))

3. Edit the `frontend > volumes` section of `docker-compose.yml` to make your SSL certificates accessible from within the frontend container.

4. Edit the `frontend > environment` section of `docker-compose.yml` to point the variables `SSL_CERTIFICATE_PATH` and `SSL_CERTIFICATE_KEY_PATH` to your SSL certificate and SSL certificate private key files respectively.

> If you're not using SSL certificates, remove references to SSL from `frontend/nginx.conf.template`.

5. Edit the `frontend > ports` section of `docker-compose.yml` to set the external ports for the frontend to listen on. For example `8080:443` will point port 8080 on the host to port 443 (HTTPS) in the container.

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
