[![banner](https://raw.githubusercontent.com/nevermined-io/assets/main/images/logo/banner_logo.png)](https://nevermined.io)

# Nevermined Federated Learning Demo

![Python Package](https://github.com/nevermined-io/fl-demo/workflows/Python%20package/badge.svg?branch=master)

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

1. Using [`nevermined-tools`](https://github.com/nevermined-io/tools)
   start the nevermined network with the compute stack and wait for everything
   to be online

```bash
$ ./start_nevermined.sh --latest --no-commons --local-spree-node --events-handler --compute

# in another terminal
$ ./scripts/wait_for_compute_api.sh
```

2. Using [`nevermined-fl-demo`](https://github.com/nevermined-io/fl-demo)
   run the demo

```bash
# Install the demo
$ pip install .

# Copy the artifacts
$ ./scripts/wait_for_migration_and_extract_keeper_artifacts.sh

# Run the demo
$ nevermined-fl-demo
```

## Access the running demo

- Accessing the argo workflows UI

Open [http://localhost:2476/workflows](http://localhost:2746/workflows) in the
browser

- Accessing minio

Open [http://localhost:8060/](http://localhost:8060/) in the browser

Login with the default credentials:
- Access Key: `AKIAIOSFODNN7EXAMPLE`
- Secret Key: `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`

## Attribution

This project is based in the [Ocean Protocol
Barge](https://github.com/oceanprotocol/barge). It keeps the same Apache v2
License and adds some improvements.

This project includes
[`keras_house_prices`](https://github.com/xaynetwork/xaynet/tree/v0.8.0/python/client_examples/keras_house_prices)
example software developed by [XAIN](https://www.xain.io/).

## License

```
Copyright 2020 Keyko GmbH
This product includes software developed at
BigchainDB GmbH, Ocean Protocol (https://www.oceanprotocol.com/),
and XAIN (https://www.xain.io/)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
