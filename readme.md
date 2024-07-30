# Tea2Tachi

A Discord bot to bind Tea and Tachi to your Discord user, and trigger a sync operation with one command.

## Available commands

- `/bind_account`: Bind your keys to your Discord account

- `/sync`: Start a manual sync of your data from Tea to Tachi

- `/logbook`: Check the latest imports and their statuses

## How to install

Build the Docker image from your local computer:
```
docker build -t tea2tachi .
```

## How to run

Either using a one-liner docker run command:
```
docker run -d --name tea2tachi --mount source=tea2tachi_data,target=/app/data -e DISCORD_KEY='your_discord_api_key_here' -e TEA_API_URL='https://maitea.app/api/v1/export/tachi' -e TACHI_API_URL='https://kamai.tachi.ac/ir/direct-manual/import' tea2tachi:latest
```

## Build and run with docker-compose

Or with docker-compose:
```
tea2tachi:
    image: tea2tachi:latest
    restart: unless-stopped
    container_name: tea2tachi
    environment:
        - DISCORD_KEY=your_discord_api_key_here
        - TEA_API_URL=https://maitea.app/api/v1/export/tachi
        - TACHI_API_URL=https://kamai.tachi.ac/ir/direct-manual/import
    volumes:
        - tea2tachi_data:/app/data
    build:
        context: ./tea2tachi
        dockerfile: Dockerfile
```

If using compose, please change the context according to your own configuration.
The configuration above handles building locally. in a relative folder of name tea2tachi.

You can then build and deploy with two commands:
```
# Rebuild all images
docker compose build
# Run system
docker compose up
```