# Proof of Kort-cept

"Proof of Kort-cept" is a Gamified Webapp of the Kort native App for mobile devices.

OpenStreetMap (OSM) is a collaborative project to create a free map of the world. It consists of volunteers contributing data manually. The tools required to make meaningful changes to those may often be overwhelming. Gamification of these tools can help to engage more users, to motivate existing ones which finally achieves better coverage and detail level of OSM. The mobile app "Kort Native" addressed this issue 2017 by providing the player with bite-sized "Missions", where they complete a Mission by adding missing data in a rewarding way with "Koins" and badges.
"Proof of Kort-cept" aims to expand these gamification principles by rebooting Kort as a webapp and turning Koins into an exchangeable in-game currency which can be used to purchase strategic in-game resources. On top of these vital changes, "Experience Points" shall be introduced as status points which will allow players to level-up and unlock more mission types on their journey.

## Usage (with docker and docker-compose)

After a `docker-compose up --build` visit `https://localhost:8443`.
Under `https://localhost:8443/api` the backend/api is running.

### Prerequisites

* Docker and docker-compose setup on your local machine.


### Setup

Use `docker-compose build --pull` to build and update existing images. 

### Start

Use `docker-compose up` to start the applications. If you want to start
the services in the background, use `docker-compose up -d` and 
`docker-compose logs -f` to display the logs. For details on how to use 
docker-compose, refer to the compose documentation.

### Create a superuser

Run `docker-compose run --rm backend python manage.py createsuperuser`
to create a superuser for this instance.

### Database

The database is being started automatically when using docker-compose.

## Deploying

### Build and push new images

* `docker-compose -f docker-compose.push.yml build --pull`
* `docker-compose -f docker-compose.push.yml push`
