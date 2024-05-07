## 🛒 ProShop | Back-End

ProShop a Ecommerce website from Dennis Ivy Cource

this is the instruction for the project installation

# Installation Steps

1. Clone the Repo

   ```sh
   git clone git@github.com:arsham-gheibi/proshop-backend.git
   ```

2. Create .env file

   ```sh
   cp .env.sample .env
   nano .env
   ```

3. Build and run The Docker Image

   ```sh
   docker compose build
   docker compose up
   ```

4. Populate the Database with the fixture

```sh
docker exec proshop-backend-app-1 python manage.py localdbrestore
```

### ❗️ NOTE : For Removing Volumes at any time Do the following

```sh
docker compose down --volumes
```

For stopping the container at any time Do the following

```sh
docker compose stop
```

# How To Delete all local Docker images ?

```sh
docker system prune -af --volumes
```

Happy Coding 🥳
