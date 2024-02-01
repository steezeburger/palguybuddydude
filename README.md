# palguybuddydude

A go service that uses palworld-rcon-buddy api to ping for player info and notiify discord whenever players join or leave.

![](docs/example.png)

## Dependencies

- [docker](https://www.docker.com/)
- [docker-compose](https://docs.docker.com/compose/)
- [palworld-rcon-buddy](https://github.com/valamidev/palworld-rcon-buddy)

## Configuration

* clone the repo
* `cp .env.example .env`
* replace `DISCORD_WEBHOOK_URL` with your discord webhook url
* `palworld-rcon-buddy` can be configured in `docker-compose.yaml`
  * see https://github.com/valamidev/palworld-rcon-buddy

## Usage

* `docker-compose up -d`

## How it works

The service uses the `palworld-rcon-buddy` api to get the player list and then compares it with the previous list to see if any players have joined or left. If any players have joined or left, it sends a discord webhook notification.

`palworld-rcon-buddy` is ran via docker-compose.

`palworld-rcon-buddy` implements its own rcon client, which worked much better than other rcon clients I tried, including `gorcon/rcon`.
