# Ente selfhosting
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

(Personal preference: Change docker volumes to local directories)

What wasn't included in any guide - and I raised concerns about it over here: https://github.com/ente-io/ente/discussions/5212 

1. Port `2112` of `museum`-container can be commented out if you do not use promotheus

2. Change `POSTGRES_PASSWORD` and `MINIO_ROOT_PASSWORD` (and optionally `MINIO_ROOT_USER`) in the `compose.yaml`!
In the `./scripts/compose/` directory you need to adjust the `minio-provision.sh` file with the new `MINIO_ROOT_PASSWORD` (and optionally `MINIO_ROOT_USER`) *AND* the `credentials.yaml`with the new `POSTGRES_PASSWORD` and `MINIO_ROOT_PASSWORD` (and optionally `MINIO_ROOT_USER`)

3. take the `museum.yaml`from https://github.com/ente-io/ente/discussions/3778 (full version attached in the end here) and use the script provided from [this kind github](https://github.com/EdyTheCow/ente-selfhost) repo to generate new secrets
```
docker run --rm ghcr.io/edythecow/ente-server-tools go run tools/gen-random-keys/main.go
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
