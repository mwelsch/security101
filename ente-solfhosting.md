# Ente selfhosting with traefik
Based on [this github guide](https://github.com/ente-io/ente/blob/main/server/docs/docker.md):

1. Create a directory where you'll run Ente

    ```sh
    mkdir ente && cd ente
    ```

2. Copy the starter compose.yaml and two of its support files from the
   repository onto your directory. You can do it by hand, or use (e.g.) curl

    ```sh
    # compose.yaml
    curl -LO https://raw.githubusercontent.com/ente-io/ente/main/server/compose.yaml

    mkdir -p scripts/compose
    cd scripts/compose

    # scripts/compose/credentials.yaml
    curl -LO https://raw.githubusercontent.com/ente-io/ente/main/server/scripts/compose/credentials.yaml

    # scripts/compose/minio-provision.sh
    curl -LO https://raw.githubusercontent.com/ente-io/ente/main/server/scripts/compose/minio-provision.sh

    cd ../..
    ```

3. Modify `compose.yaml`. Instead of building from source, we want directly use
   the published Docker image from `ghcr.io/ente-io/server`

    ```diff
    --- a/server/compose.yaml
    +++ b/server/compose.yaml
    @@ -1,9 +1,6 @@
     services:
       museum:
    -    build:
    -      context: .
    -      args:
    -        GIT_COMMIT: development-cluster
    +    image: ghcr.io/ente-io/server
    ```

4. Create an (empty) configuration file. You can later put your custom
   configuration in this if needed.

    ```sh
    touch museum.yaml
    ```

5. (Personal preference: Change docker volumes to local directories)

# Traefik part for museum
## This is specific to your traefik config so read carefully
1. Add the network your traefik container is in. In my case the tail of the file looks like this:
```
networks:
  internal:
  default:
    external:
      name: web
```
2. Change the museum part to be also included in that network and add labels. With this change you do not need to publicly expose port 8080
```
   #ports:
    #  - 8080:8080 # API
    #  - 2112:2112 # Prometheus metrics - FURTHER ON I DESCRIBED WHY YOU MIGHT BE ABLE TO COMMENT THIS OUT
    [...]
    networks:
      - internal
      - default
    labels:
      - traefik.http.routers.enteapi.rule=Host(`api.example.com`)
      - traefik.http.routers.enteapi.tls.certresolver=YOURDEFAULTCERTRESOLVER
      - traefik.http.services.enteapi.loadbalancer.server.port=8080
```

 
# What wasn't included in any guide - and I raised concerns about it over here: https://github.com/ente-io/ente/discussions/5212 

1. Port `2112` of `museum`-container can be commented out if you do not use promotheus

2. Change `POSTGRES_PASSWORD` and `MINIO_ROOT_PASSWORD` (and optionally `MINIO_ROOT_USER`) in the `compose.yaml`!
In the `./scripts/compose/` directory you need to adjust the `minio-provision.sh` file with the new `MINIO_ROOT_PASSWORD` (and optionally `MINIO_ROOT_USER`) *AND* the `credentials.yaml`with the new `POSTGRES_PASSWORD` and `MINIO_ROOT_PASSWORD` (and optionally `MINIO_ROOT_USER`)

3. I commented out Port `5432` of the PostgreSQL container since the museum container accesses it locally and after 5 minutes I got approx 10 requests/second from someone trying to bruteforce their way into the database

4. take the `museum.yaml`from https://github.com/ente-io/ente/discussions/3778 (full version attached in the end here) and use the script provided from [this kind github](https://github.com/EdyTheCow/ente-selfhost) repo to generate new secrets
```
docker run --rm ghcr.io/edythecow/ente-server-tools go run tools/gen-random-keys/main.go
```

# Running the web app behind traefik:
For this step lets run the web app in a seperate location (could also be a seperate server afaik) to keep stuff simple. From [this guide](https://help.ente.io/self-hosting/guides/web-app)
```
git clone https://github.com/ente-io/ente.git
cd ente
git submodule update --init --recursive
```
Create a `web/Dockerfile` (my content is below, I commented out the parts not required for ente photos and updated the FROM version to 23 rather than 20. Use the default one or modify mine if you want to host Ente Auth).

Add the following to a `compose.yaml` in the root github directory (docker-compose will build the image in this case, if you want to build manually and insert the new tag manually each time: use the above guide (https://help.ente.io/self-hosting/guides/web-app) to build the web app, remove the build part and comment out the image part and insert your image name)

YOU MIGHT NEED TO ADJUST FOR YOUR TRAEFIK CONFIG

# Create accounts
You can create an account and obtain the OTP from the docker logs if you did not configure an email server


# Combine everything into one docker-compose
IF EVERYTHING WORKED SO FAR:


```
services:
  ente-web:
    build:
      context: web
    #image: <image-name> # name of the image you used while building
    #ports:
    #  - 3000:3000
    #  - 3001:3001
    #  - 3002:3002
    #  - 3003:3003
    #  - 3004:3004
    environment:
      - NODE_ENV=development
      - ENDPOINT=https://api.example
      - ALBUMS_ENDPOINT=https://albums.example
    restart: always
    labels:
      - traefik.http.routers.photos.rule=Host(`photos.example`)
      - traefik.http.routers.photos.tls.certresolver=default
      - traefik.http.routers.photos.service=svc_photos
      - traefik.http.services.svc_photos.loadbalancer.server.port=3000
      - traefik.http.routers.albums.rule=Host(`albums.example`)
      - traefik.http.routers.albums.tls.certresolver=default
      - traefik.http.routers.albums.service=svc_albums
      - traefik.http.services.svc_albums.loadbalancer.server.port=3004
      #IF YOU WANT TO USE ENTE AUTH
      #- traefik.http.routers.auth.rule=Host(`auth.example`)
      #- traefik.http.routers.auth.tls.certresolver=default
      #- traefik.http.routers.auth.service=svc_auth
      #- traefik.http.services.svc_auth.loadbalancer.server.port=3002
    networks:
      - default


networks:
  default:
    external:
      name: web

```

`museum.yaml`
```
# HTTP connection parameters
http:
    # If true, bind to 443 and use TLS.
    # By default, this is false, and museum will bind to 8080 without TLS.
    # use-tls: true

# Specify the base endpoints for various apps
apps:
    # Default is https://albums.ente.io
    #
    # If you're running a self hosted instance and wish to serve public links,
    # set this to the URL where your albums web app is running.
    public-albums: https://albums.example.com


# Passkey support (optional)
# Use case: MFA
webauthn:
    # Our "Relying Party" ID. This scopes the generated credentials.
    # See: https://www.w3.org/TR/webauthn-3/#rp-id
    rpid: accounts.example.com
    # Whitelist of origins from where we will accept WebAuthn requests.
    # See: https://github.com/go-webauthn/webauthn
    rporigins:
        - "https://accounts.example.com"

s3:
    are_local_buckets: true
    b2-eu-cen:
        key: admin
        secret: changeme
        endpoint: https://minio.example.com
        region: eu-central-2
        bucket: b2-eu-cen
key:
    encryption: mysecret
    hash: mysecret
jwt:
    secret: mysecret



# Add this once you have done the CLI part
#internal:
#    admins:
#        - 1580559962386438


# SMTP configuration (optional)
#
# Configure credentials here for sending mails from museum (e.g. OTP emails).
#
# The smtp credentials will be used if the host is specified. Otherwise it will
# try to use the transmail credentials. Ideally, one of smtp or transmail should
# be configured for a production instance.
#
# username and password are optional (e.g. if you're using a local relay server
# and don't need authentication).
#smtp:
#    host: 
#    port: 
#    username: 
#    password: 
#    # The email address from which to send the email. Set this to an email
#    # address whose credentials you're providing.
#    email: 
```
`Dockerfile` for building ONLY PHOTOS web app
```
FROM node:23-bookworm-slim as builder

WORKDIR ./ente

COPY . .
COPY apps/ .

# Will help default to yarn versoin 1.22.22
RUN corepack enable

# Endpoint for Ente Server
ENV NEXT_PUBLIC_ENTE_ENDPOINT=https://your-ente-endpoint.com
ENV NEXT_PUBLIC_ENTE_ALBUMS_ENDPOINT=https://your-albums-endpoint.com

RUN yarn cache clean
RUN yarn install --network-timeout 1000000000
RUN yarn build:photos #&& yarn build:accounts && yarn build:auth && yarn build:cast

FROM node:23-bookworm-slim
WORKDIR /app

COPY --from=builder /ente/apps/photos/out /app/photos
#COPY --from=builder /ente/apps/accounts/out /app/accounts
#COPY --from=builder /ente/apps/auth/out /app/auth
#COPY --from=builder /ente/apps/cast/out /app/cast

RUN npm install -g serve

ENV PHOTOS=3000
EXPOSE ${PHOTOS}

#ENV ACCOUNTS=3001
#EXPOSE ${ACCOUNTS}

#ENV AUTH=3002
#EXPOSE ${AUTH}

#ENV CAST=3003
#EXPOSE ${CAST}

# The albums app does not have navigable pages on it, but the
# port will be exposed in-order to self up the albums endpoint
# `apps.public-albums` in museum.yaml configuration file.
ENV ALBUMS=3004
EXPOSE ${ALBUMS}

CMD ["sh", "-c", "serve /app/photos -l tcp://0.0.0.0:${PHOTOS}"]
# & serve /app/accounts -l tcp://0.0.0.0:${ACCOUNTS} & serve /app/auth -l tcp://0.0.0.0:${AUTH} & serve /app/cast -l tcp://0.0.0.0:${CAST}"]
```
