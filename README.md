# cloud.gov Customer app

[![CircleCI](https://circleci.com/gh/18F/cg-customers.svg?style=svg)](https://circleci.com/gh/18F/cg-customers)

It just uses the django-admin interface to act as the UI for the machine
readable source of truth for customer data.

[Production](https://customers.fr.cloud.gov)
[Staging](https://customers.fr-stage.cloud.gov)

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
  -c '{"redirect_uri": ["https://customers.fr-stage.cloud.gov"]}'
```

Next, run: `cf service customer-uaa-client` to get the fugacious link. Open the
link and create a user-provided-service using the credentials.

```sh
cf cups customer-uaa-creds -p '{"UAA_CLIENT_ID": "client-id", "UAA_CLIENT_SECRET": "client_secret"}'
```

### S3 bucket with billing data

In order to get the S3 bucket that is published by the
[cg-billing](https://github.com/18F/cg-billing/) app, you have to get the old
pipeline, change the org and space for where it should place the UPS, then set
new pipeline.

To change the pipeline, you use the `fly` cli.

To get the pipeline, run:

```sh
fly -t {your-concourse-target} get-pipeline -p deploy-billing > deploy_billing.yml
```

To set the pipeline, run:

```sh
fly -t {your-concourse-target} set-pipeline -n -c deploy_billing.yml -p deploy-billing
```

### Other credentials
```sh
cf cups customer-django-creds -p '{"SECRET_KEY": "your-secret-key"}'
```

### Deployer Accounts

In both the `customer-prod` and `customer-stage` spaces, create a deployer
account.

```sh
cf create-service cloud-gov-service-account space-deployer customer-deployer
```

Run this command to get the fugacious link to get the creds:
```sh
cf service customer-deployer
```

Once you have the credentials for both spaces, go to [CircleCI](https://circleci.com/gh/18F/cg-customers/edit#env-vars)
and set/replace the following variables:

- `CF_USERNAME_PROD_SPACE`
- `CF_PASSWORD_PROD_SPACE`
- `CF_USERNAME_STAGE_SPACE`
- `CF_PASSWORD_STAGE_SPACE`

Once you have setup these credentials, merges into the `master` branch  will
deploy to the staging environment and merges into the `production` branch will
deploy to the production environment.


### Add initial account(s) with access.

Once the application is deployed, if this is a fresh database, you will need
to setup a superuser so they can login.

```sh
cf ssh customers
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/app/.cloudfoundry/0/lib/
cd app
$HOME/app/.cloudfoundry/0/python/bin/python3.6 manage.py createsuperuser \
  --username foo --email foo@example.org --noinput
```

*Note: you do not set a password*

### Local development

#### Database setup
You need to have a Postgres database running. With your locally running
database, run `createdb customer_dashboard`

If it is not running via localhost:5432, you will need to export the database
url.

```
export DATABASE_URL="postgres://user:pw@ipaddr:port/customer_dashboard"
```

#### Get dependencies

`pip install -r requirements.txt`

#### Running locally

`./start_local.sh`
