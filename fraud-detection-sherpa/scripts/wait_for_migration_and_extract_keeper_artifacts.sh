#!/bin/bash

RETRY_COUNT=0
COMMAND_STATUS=1

mkdir -p artifacts

until [ $COMMAND_STATUS -eq 0 ] || [ $RETRY_COUNT -eq 120 ]; do
  nevermined_contracts_docker_id=$(docker container ls | grep nevermined-contracts | awk '{print $1}')
  docker cp ${nevermined_contracts_docker_id}:/nevermined-contracts/artifacts/ready ./artifacts/
  COMMAND_STATUS=$?
  sleep 5
  let RETRY_COUNT=RETRY_COUNT+1
done

if [ $COMMAND_STATUS -ne 0 ]; then
  echo "Waited for more than two minutes, but keeper contracts have not been migrated yet. Did you run an Ethereum RPC client and the migration script?"
  exit 1
fi

docker cp ${nevermined_contracts_docker_id}:/nevermined-contracts/artifacts/. ./artifacts/
