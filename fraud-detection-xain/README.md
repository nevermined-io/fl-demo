# Creditcard Fraud Detection Federated Learning Demo

## Description

In this demo we will be using version 0.8 of the [XAIN Federated Learning
Framework](https://github.com/xaynetwork/xaynet/tree/v0.8.0).

In this particular example the goal of the model to train is to detect fraudulent credit card transactions given two different datasets. This dataset was downloaded from
[kaggle](https://www.kaggle.com/mlg-ulb/creditcardfraud)
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

1. Using [`nevermined-tools`](https://github.com/nevermined-io/tools)
   start the nevermined network with the compute stack and wait for everything
   to be online

```bash
$ ./start_nevermined.sh --latest --no-marketplace --local-spree-node --events-handler --compute

# in another terminal
$ ./scripts/wait_for_compute_api.sh
```

2. Inside the [`fraud-detection-xain`](https://github.com/nevermined-io/fl-demo/tree/master/fraud-detection-xain)
   setup the demo

```bash
# Install the demo
$ pip -r requirements.txt

# Copy the artifacts
$ ./scripts/wait_for_migration_and_extract_keeper_artifacts.sh
```

## Running the Demo

The demo contains three jupyter notebooks

- [nevermined_provider.ipynb](https://github.com/nevermined-io/fl-demo/blob/master/fraud-detection-xain/notebooks/nevermined_provider.ipynb): shows how data providers can advertise their data and services through nevermined
- [nevermined_consumer.ipynb](https://github.com/nevermined-io/fl-demo/blob/master/fraud-detection-xain/notebooks/nevermined_consumer.ipynb): shows how a data consumer access services and run computations on the data from the data providers
- [federated_fraud_demo.ipynb](https://github.com/nevermined-io/fl-demo/blob/master/fraud-detection-xain/notebooks/federated_fraud_demo.ipynb): contains the actual machine learning code that is executed on the data providers infrastructure

1. Start jupyter-lab
```bash
$ jupyter-lab
```

2. Run all cells of `nevermined_provider.ipynb`
3. Run all cells of `nevermined_consumer.ipynb`

## Access the running demo

- Accessing the argo workflows UI

Open [http://localhost:2476/workflows](http://localhost:2746/workflows) in the
browser

- Accessing minio

Open [http://localhost:8060/](http://localhost:8060/) in the browser

Login with the default credentials:
- Access Key: `AKIAIOSFODNN7EXAMPLE`
- Secret Key: `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`