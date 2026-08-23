#!/bin/bash

docker compose -f docker-compose-prod.yml logs smartthingsbridge

docker compose -f docker-compose-prod.yml up -d --pull always --force-recreate smartthingsbridge

#git pull
