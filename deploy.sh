#!/bin/bash

# deploy and delete previous version. 
gcloud app deploy
gcloud app versions list --format="value(version.id)" --sort-by="~version.createTime" | tail -1 | xargs gcloud app versions delete

echo "Deployed successfully"
gcloud app versions list --format="value(version.id)" | xargs echo "Version ID: $1"