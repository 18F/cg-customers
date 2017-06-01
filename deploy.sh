#!/bin/bash

set -e
set -o pipefail

# Install cf cli
curl -v -L -o cf-cli_amd64.deb 'https://cli.run.pivotal.io/stable?release=debian64&source=github'
sudo dpkg -i cf-cli_amd64.deb
cf -v

# Install autopilot plugin for blue-green deploys
go get github.com/contraband/autopilot
cf install-plugin -f /home/ubuntu/.go_workspace/bin/autopilot

if [ "$CIRCLE_BRANCH" == "master" ]
then
	CF_MANIFEST="manifest-staging.yml"
	CF_SPACE="customer-stage"
	CF_APP="customers-staging"
elif [ "$CIRCLE_BRANCH" == "production" ]
then
	CF_MANIFEST="manifest.yml"
	CF_SPACE="customer-prod"
	CF_APP="customers"
else
  echo Unknown environment, quitting. >&2
  exit 1
fi

# We use the deployer-account broker to get the credentials of
# our deployer accounts.
# Currently, the deployer accounts are scoped to a single space.
# As a result, we will filter by space for which credentials to use.
CF_ORGANIZATION="cloud-gov"
if [ "$CF_SPACE" == "customer-prod" ]
then
	CF_USERNAME=$CF_USERNAME_PROD_SPACE
	CF_PASSWORD=$CF_PASSWORD_PROD_SPACE
elif [ "$CF_SPACE" == "customer-stage" ]
then
	CF_USERNAME=$CF_USERNAME_STAGE_SPACE
	CF_PASSWORD=$CF_PASSWORD_STAGE_SPACE
else
	echo "Unknown space. Do not know how to deploy to the $CF_SPACE space."
	exit 1
fi

echo manifest: $CF_MANIFEST
echo space:    $CF_SPACE

function deploy () {
  local manifest=${1}
  local org=${2}
  local space=${3}
  local app=${4}

  CF_API="https://api.fr.cloud.gov"
  # Log in
  cf api $CF_API
  cf auth $CF_USERNAME $CF_PASSWORD
  cf target -o $org -s $space

  # Run autopilot plugin
  cf zero-downtime-push $app -f $manifest
}

# Set manifest path
MANIFEST_PATH=$CF_MANIFEST
deploy "$MANIFEST_PATH" "$CF_ORGANIZATION" "$CF_SPACE" "$CF_APP"
