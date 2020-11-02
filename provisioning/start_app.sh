#!/bin/bash

if [[ -z "${MONGO_PASSWORD}" ]]; then
    echo "There is not MONGO_PASSWORD env. variable defined!"
    exit 1
fi

docker run -d -e "MONGO_INITDB_ROOT_USERNAME=admin" -e "MONGO_INITDB_ROOT_PASSWORD=${MONGO_PASSWORD}"  -p 27017-27019:27017-27019 -v ~/mongo_data:/data/db --name mongodbauth mongo:latest
docker run -d -e "MONGO_PASSWORD=${MONGO_PASSWORD}" -p 8080:8080 felipez/insilico:prototype