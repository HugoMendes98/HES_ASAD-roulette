# Roulette

> Jeu de roulette

## Run with docker-compose

This application can be launched with the following command:

```bash
docker compose up
```

By default, the application is available at `http://localhost:8080`.

> This is a version without any SSL (for tests, dev purposes or even if another security layer is used (e.g. inside a kubernetes)).

### With HTTPS and WSS

```bash
docker compose -f ./docker-compose.yml -f ./docker-compose.ssl.yml up
```

> Do not forget the `-f ./docker-compose.yml -f ./docker-compose.ssl.yml` when using different commands (such as `restart`, `down`, ...)

By default, the application is available at `http://localhost:8080` and `https://localhost:8443`.

> The HTTP always redirect to HTTPS.  
> The default certificates are self-signed.

### Refresh services

If there is an existing running _docker-compose_, the services (backend and/or frontend) can be rebuild and replaced with the following command:

```bash
docker compose up --build <service>
```

> It recreates the images and will only down the previous when ready to be restarted.

### Schema

Here's a little schema to understand the "infrastructure"

```mermaid
flowchart LR
  subgraph sSsl[service:ssl]
    ssl{ssl}
    sProxy    
  end

  subgraph sProxy[service:proxy]
    proxy{proxy}
    frontend
    backend
  end

  client((Client))
  client -- "Access application" --> ssl
  client -. "Access application (no SSL config)" .-> proxy
  ssl == "Secure with SSL/TLS" ===> proxy

  proxy -- "Access API/WS" --> backend
  proxy -- "Access HTML" --> frontend
```

> The arrow between `client` and `proxy` only exists with the first [docker-compose](#run-with-docker-compose) configuration.
