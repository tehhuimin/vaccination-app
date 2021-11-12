## Prerequisites

The backend of this project is run based on docker and docker-compose.

Please install docker at `https://docs.docker.com/install/` and docker-compose at `https://docs.docker.com/compose/install/`.

## Running the Project

### Backend

1. Copy the `.env.example` file available and create an `.env` file at the same directory. Update the fields accordingly for secret data.
2. `docker-compose --env-file .env config`

   * This command will configure the `docker-compose.yml` by taking in the environment variables stated in `.env`
   * Note: please ensure to install docker-compose version 1.8+ for the config to work properly
3. `docker-compose up --force-recreate`

   1. This will start the process of building the backend image from the source Python 3.6 base image, and installing pip packages stated inside the `requirements.txt` file.

      - Please refer to `Dockerfile` for more details.
      - All codes will be mounted as a volume inside the `/code` directory.
   2. A PostgreSQL base image will also be pulled from the docker registry.
   3. After building the image, the processes will be started as stated in the `docker-compose.yml` file.

      * Upon starting up, a data migration will be carried out based on the migrations stated inside the `migrations` folder.
      * Upon starting up, a loaddata will also be done using the following command: `python ./manage.py loaddata booking/fixtures/data.json`. If you do not wish to have this be done, please comment out this line.
      * A `--force-recreate` flag is set  when calling `docker-compose up` to prevent data from being uploaded multiple times. You can remove this as well.
4. Visit APIs documentation at `localhost:8000/swagger/`
5. To list running docker containers, you can run `docker ps`, note the container id stated in the output.
6. To execute commands inside the image, you can run `docker exec -it <container_id> bash` then run whatever commands you need.

   If you would like to run the test cases, run `python manage.py test` after getting into the backend image.


### Frontend 

Run the codes as stated in the frontend `README.md`.


## The Tech Stack

1. This project uses Django-Rest-Framework to deploy REST API.
2. The database used is Postgresql. The ORM comes with Django is being used.
3. `drf-yasg` is used to run Swagger for API documentation.
