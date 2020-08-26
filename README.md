# Nevermined Federated Learning Demo

## Description

This demo is meant to showcase the Nevermined Federated Learning capabilities
that leverages the _Data In-Situ Computation_ capabilities to bring a model to
the data so that the data can remain private.

In this demo we will be using version 0.8 of the [XAIN Federated Learning
Framework](https://github.com/xaynetwork/xaynet/tree/v0.8.0) as we will also
use their
[`keras_house_prices`](https://github.com/xaynetwork/xaynet/tree/v0.8.0/python/client_examples/keras_house_prices)
example as a base.

In this particular example the goal of the model to train is to predict the
final price of houses given two different datasets describing several
characteristics of residential homes. This dataset was downloaded from
[kaggle](https://www.kaggle.com/c/house-prices-advanced-regression-techniques/data)
and split into two.

## Use Case

![Demo architecture](images/fl-demo-architecture.png)

1. Two Data Providers publish their respective datasets
2. A Data Scientist discovers the assets and purchases permission to run
   computations on the data from both the data providers.
3. Data Scientist publishes information about the algorithm that it wants to
   run on the data and makes it discoverable to each data provider
4. Data providers download the algorithm, configure the execution environment
   and begin training
5. The Coordinator orchestrates the Federated Learning session by at the
   beginning of each round sending the model weights to all participants,
   waiting for the updated participants weights and aggregating the results
   into a new global model.
6. Finally the trained model is published and ready to be downloaded by the Data
   Scientist

## Setup

1. Using [`nevermined-tools`](https://github.com/keyko-io/nevermined-tools)
   start the nevermined stack and wait for the contracts to be deployed and
   artifacts to be copied to `$HOME/.nevermined/nevermined-contracts/artifacts`

```bash
$ ./start_nevermined.sh --latest --no-commons --no-gateway --local-spree-node
```

2. Using [`nevermined-tools`](https://github.com/keyko-io/nevermined-tools)
   start and configure the compute stack through `minikube`

```bash
# There are some bugs affecting minikube with k8s 1.18.0 so we need to use 1.17.0
$ minikube config set kubernetes-version 1.17.0

# Start compute stack
$ ./scripts/setup_minikube.sh

# If minikube refuses to start due to virtualization problems be can set the minikube driver to docker
$ MINIKUBE_DRIVER=docker ./scripts/setup_minikube.sh

# Create a configmap for the artifacts
$ kubectl create configmap artifacts \
    --from-file=$HOME/.nevermined/nevermined-contracts/artifacts/ \
    --namespace=nevermined-compute

# Start the argo-artifacts service
$ helm install argo-artifacts stable/minio --set service.type=LoadBalancer \
    --set fullnameOverride=argo-artifacts

# If helm can't find argo-artifacts add the helm repo and try again
$ helm repo add stable https://kubernetes-charts.storage.googleapis.com/
$ helm repo update
```

3. Using [nevermined-gateway](https://github.com/keyko-io/nevermined-gateway)
   start the Provider gateway

```bash
# Copy the accounts folder from the nevermined-tools repo into the nevermined-gateway folder

# Copy the artifacts
$ ./scripts/wait_for_migration_and_extract_keeper_artifacts.sh

# Set the environment variables
export FLASK_APP=nevermined_gateway/run.py
export PROVIDER_ADDRESS=0x068ed00cf0441e4829d9784fcbe7b9e26d4bd8d0
export PROVIDER_PASSWORD=secret
export PROVIDER_KEYFILE="./accounts/provider.json"
export RSA_PRIVKEY_FILE="./accounts/rsa_priv_key.pem"
export RSA_PUBKEY_FILE="./accounts/rsa_pub_key.pem"
export CONFIG_FILE=config.ini

# start the gateway api
$ flask run --host=0.0.0.0 --port=8030
```

4. Using
   [nevermined-compute-api](https://github.com/keyko-io/nevermined-compute-api/)
   start the Provider compute api

```bash
# Copy the accounts folder from the nevermined-tools repo into the nevermined-compute-api folder

# Copy the artifacts
$ ./scripts/wait_for_migration_and_extract_keeper_artifacts.sh

# Set the environment variables
export PROVIDER_ADDRESS=0x068ed00cf0441e4829d9784fcbe7b9e26d4bd8d0
export PROVIDER_PASSWORD=secret
export PROVIDER_KEYFILE="./accounts/provider.json"

# start the compute api
$ python -m nevermined_compute_api.run
```

5. (Optional) Build the docker images. See [Building the docker
   images](#building-the-docker-images)

6. Using [`nevermined-fl-demo`](https://github.com/keyko-io/nevermined-fl-demo)
   run the demo

```bash
# Copy the artifacts
$ ./scripts/wait_for_migration_and_extract_keeper_artifacts.sh

# Run the demo
$ python demo.py
```

## Access the running demo

- Accessing the argo workflows UI

```bash
# Setup port forwarding for the argo server
$ kubectl -n nevermined-compute port-forward deployment/argo-server 2746:2746
```

Open [http://localhost:2476/workflows](http://localhost:2746/workflows) in the
browser

- Accessing minio

```bash
# Find out the host url
$ minikube service argo-artifacts --url
```

Login with the default credentials:
- Access Key: `AKIAIOSFODNN7EXAMPLE`
- Secret Key: `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`

## Building the docker images

In case the docker images are not published in the keykoio docker repo or local
changes were made and we want to test them before publishing the images we need
to build them locally.

Currently the demo makes use of four docker images:
- `keykoio/nevermined-pod-config-py:latest` (compute stack)
- `keykoio/nevermined-pod-publishing-py:latest` (compute stack)
- `keykoio/xain-fl:latest` (federated learning on the compute stack)
- `keykoio/xain-fl-participant` (demo)



Building the
[`nevermined-pod-config-py`](https://github.com/keyko-io/nevermined-pod-config-py/)
image:

```bash
# enter the minikube docker environment
$ eval $(minikube -p minikube docker-env)

# from the root of the nevermined-pod-config-py repo run
$ docker build -t keykoio/nevermined-pod-config-py:latest .
```

Building the
[`nevermined-pod-publishing-py`](https://github.com/keyko-io/nevermined-pod-publishing-py/)
image:

```bash
# enter the minikube docker environment
$ eval $(minikube -p minikube docker-env)

# from the root of the nevermined-pod-publishing-py repo run
$ docker build -t keykoio/nevermined-pod-publishing-py:latest .
```

Building the [`xain-fl`](https://github.com/keyko-io/xain-fl) image:

```bash
# enter the minikube docker environment
$ eval $(minikube -p minikube docker-env)

# from the root of the xain-fl repo run
$ docker build -f docker/Dockerfile -t keykoio/xain-fl:latest .
```

Building the
[`xain-fl-participant`](https://github.com/keyko-io/nevermined-fl-demo) image:

```bash
# enter the minikube docker environment
$ eval $(minikube -p minikube docker-env)

# from the root of the nevermined-fl-demo repo run
$ cd keras_house_prices
$ docker build -t keykoio/xain-fl-participant:latest .
```
