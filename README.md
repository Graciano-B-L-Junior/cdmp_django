<h1>Casa da moeda pessoal - web application to monitoring and analalyze your spends</h1>

<img src="https://github.com/Graciano-B-L-Junior/cdmp_django/assets/44882375/0afd88ff-5769-4758-a559-1e6ad3aee378" height=500>
<img src="https://github.com/Graciano-B-L-Junior/cdmp_django/assets/44882375/ed28d849-9ca3-47c7-b8e3-2de384b930f1" height=500>
<img src="https://github.com/Graciano-B-L-Junior/cdmp_django/assets/44882375/13cbd6e9-221d-4003-bc3e-efa23dfe0d16" width=1500>
<img src="https://github.com/Graciano-B-L-Junior/cdmp_django/assets/44882375/ddf2ed16-a640-46f2-96aa-f23318ae4107" width=1500>


## About project
It's a full stack project,created to simplify search, analyze, and manage personal (or bussiness if you set categories) spends.

## Motivation
I have a google sheet to put my spends and then find where spended more, but are just numbers, and read an annual spends is a mess to me, then i think to create a web system to resolve this issue.

# How to install and run
#### This project need **docker** and **docker-compose** to build and run

## Instaling docker and docker-compose (windows and linux users)
*  install [docker desktop for windows] (https://docs.docker.com/desktop/install/windows-install/) for windows, attention with requirements fit with your computer to install docker
*  install [docker desktop for linux] (https://docs.docker.com/desktop/install/linux-install/) select your current based platform, if you have doubt how to install, ask to chatgpt or search on google

## build images and start up containers
*  in terminal prompt, **sudo docker-compose build**, this will build the containers for development environment
*  Then prompt **sudo docker-compose up** to run containers
*  Open browser and access <http://localhost:8000>

## Using production environment
*  in terminal prompt **sudo docker-compose -f docker-compose.prod.yaml build**, this will build the containers for production environment
*  Then prompt **sudo docker-compose up** to run containers
*  Open browser and access <http://localhost>

## Tecnologies used
*  python
*  Django (web framework)
*  Postgres (Database)
*  Nginx (Web server load balancer)
*  Docker and docker-compose
*  shell script
