# cloud.gov Customer app

It just uses the django-admin interface to act as the UI for the machine
readable source of truth for customer data.

https://customers.fr.cloud.gov

Team members will need to request access to #cg-customer to have your e-mail
added to the django database so that when login requests from this
[uaa module](https://github.com/18F/cg-django-uaa) returns an e-mail address,
django will check against it's allowed users database and permit/revoke access.

## Deploy to cloud.gov

### Database

```sh
# Production
cf cs aws-rds medium-psql customer-db

# Staging
cf cs aws-rds shared-psql customer-db
```

### S3 Bucket

```sh
cf create-service s3 basic customer-s3
```

### OAuth Service

```sh
# Production
cf create-service cloud-gov-identity-provider oauth-client \
  customer-uaa-client -c '{"redirect_uri": ["https://customers.fr.cloud.gov"]}'

# Staging
cf create-service cloud-gov-identity-provider oauth-client \
  customer-uaa-client \
  -c '{"redirect_uri": ["https://customers-staging.fr.cloud.gov"]}'
```

Next, run: `cf service customer-uaa-client` to get the fugacious link. Open the
link and create a user-provided-service using the credentials.

```sh
cf cups customer-uaa-creds -p '{"UAA_CLIENT_ID": "client-id", "UAA_CLIENT_SECRET": "client_secret"}'
```

### Other credentials
```sh
cf cups customer-django-creds -p '{"SECRET_KEY": "your-secret-key"}'
```

### Deploy

```sh
cf push
```

### Add initial account(s) with access.

```sh
cf ssh customers
for f in /home/vcap/app/.profile.d/*.sh; do source "$f"; done;
cd app
$HOME/app/.cloudfoundry/python/bin/python3 manage.py createsuperuser \
  --username foo --email foo@example.org --noinput
```

### Local development

#### Database setup
You need to have a Postgres database running. With your locally running
database, run `createdb customer_data`

If it is not running via localhost:5432, you will need to export the database
url.

```
export DATABASE_URL="postgres://user:pw@ipaddr:port/customer_data"
```

#### Get dependencies

`pip install -r requirements.txt`

#### Running locally

`./start_local.sh`
