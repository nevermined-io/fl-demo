# House Prices Federated Learning Demo

## Description

In this demo we will be using version 0.1.0 of the [Sherpa.ai Federated Learning and Differential Privacy Framework](https://github.com/sherpaai/Sherpa.ai-Federated-Learning-Framework).

In this particular example the goal of the model to train is to detect fraudulent credit card transactions given two different datasets. This dataset was downloaded from
[kaggle](https://www.kaggle.com/mlg-ulb/creditcardfraud)
and split into two.

## Setup

1. Using [`nevermined-tools`](https://github.com/nevermined-io/tools)
   start the nevermined network with the compute stack and wait for everything
   to be online

```bash
$ ./start_nevermined.sh --latest --no-marketplace --local-spree-node --events-handler --compute

# in another terminal
$ ./scripts/wait_for_compute_api.sh
```

2. Inside the [`fraud-detection-sherpa`](https://github.com/nevermined-io/fl-demo/tree/master/fraud-detection-sherpa)
   setup the demo

```bash
# Install the demo
$ pip -r requirements.txt

# Copy the artifacts
$ ./scripts/wait_for_migration_and_extract_keeper_artifacts.sh
```

## Running the Demo

The demo contains three jupyter notebooks

- [nevermined_provider.ipynb](https://github.com/nevermined-io/fl-demo/blob/master/fraud-detection-sherpa/notebooks/nevermined_provider.ipynb): shows how data providers can advertise their data and services through nevermined
- [nevermined_consumer.ipynb](https://github.com/nevermined-io/fl-demo/blob/master/fraud-detection-sherpa/notebooks/nevermined_consumer.ipynb): shows how a data consumer access services and run computations on the data from the data providers
- [federated_fraud_demo.ipynb](https://github.com/nevermined-io/fl-demo/blob/master/fraud-detection-sherpa/notebooks/federated_fraud_demo.ipynb): contains the actual machine learning code that is executed on the data providers infrastructure

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