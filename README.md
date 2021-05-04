[![banner](https://raw.githubusercontent.com/nevermined-io/assets/main/images/logo/banner_logo.png)](https://nevermined.io)

# Nevermined Federated Learning Demos

![Python Package](https://github.com/nevermined-io/fl-demo/workflows/Python%20package/badge.svg?branch=master)

## Description

These demos are meant to showcase the Nevermined Federated Learning capabilities
that leverages the _Data In-Situ Computation_ capabilities to bring a model to
the data so that the data can remain private.

You can find the instructions of how to run the demos from the READMEs in each demo individual folders:

- [House Prices](house-prices-xain/README.md): Keras + [Xaynet FL framework](https://github.com/xaynetwork/xaynet)
- [Creditcard Fraud Sherpa](fraud-detection-sherpa/README.md): scikit-learn + [Sherpa FL framework](https://github.com/sherpaai/Sherpa.ai-Federated-Learning-Framework)
- [Creditcard Fraud Xaynet](fraud-detection-xain/README.md): scikit-learn + [Xaynet FL framework](https://github.com/xaynetwork/xaynet)
- [Creditcard Fraud Flower](fraud-detection-flower/README.md): scikit-learn + [Flower FL framework](https://github.com/adap/flower)

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
XAIN (https://www.xain.io/), Adap (https://adap.com/en), and sherpa.ai (https://sherpa.ai/).

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
