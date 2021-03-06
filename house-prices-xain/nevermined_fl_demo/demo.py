"""Main demo code"""

import copy
import json
import sys

from common_utils_py.agreements.service_agreement import ServiceAgreement
from common_utils_py.agreements.service_types import ServiceTypes
from contracts_lib_py.account import Account
from web3 import Web3
from nevermined_sdk_py import Config, Nevermined
from nevermined_sdk_py.nevermined.keeper import NeverminedKeeper as Keeper

from nevermined_fl_demo.utils import dates_generator, wait_for_compute_jobs
from nevermined_fl_demo.download import download

PARITY_ADDRESS = "0x068ed00cf0441e4829d9784fcbe7b9e26d4bd8d0"
PARITY_PASSWORD = "secret"
PARITY_KEYFILE = "resources/accounts/provider.json"

# Disable warnings emitted by web3
if not sys.warnoptions:
    import warnings

    warnings.simplefilter("ignore")


def demo():
    """The Nevermined Federated Learning demo.

    This demo showcases the nevermined Federated Learning capabilities.
    FLow:
        1. Setup nevermined
        2. Setup accounts
        3. Publish compute to the data assets
        4. Publish algorithm
        5. Publish workflows
        6. Order computations
        7. Execute workflows

    """

    print("Setting up...\n")

    date_created = dates_generator()

    # 1. Setup nevermined
    nevermined = Nevermined(Config("config.ini"))
    keeper = Keeper.get_instance()
    provider = "0x068Ed00cF0441e4829D9784fCBe7b9e26D4BD8d0"

    # 2. Setup accounts
    acc = Account(
        Web3.toChecksumAddress(PARITY_ADDRESS), PARITY_PASSWORD, PARITY_KEYFILE
    )
    nevermined.accounts.request_tokens(acc, 100)
    provider_data0 = acc
    provider_data1 = acc
    provider_coordinator = acc
    consumer = acc

    # 3. Publish compute to the data
    with open("resources/metadata/metadata0.json") as f:
        metadata_data0 = json.load(f)
        metadata_data0["main"]["dateCreated"] = next(date_created)
    with open("resources/metadata/metadata1.json") as f:
        metadata_data1 = json.load(f)
        metadata_data1["main"]["dateCreated"] = next(date_created)

    ddo_compute0 = nevermined.assets.create_compute(
        metadata_data0, provider_data0, providers=[provider],
    )
    assert ddo_compute0 is not None, "Creating asset compute0 on-chain failed"
    print(
        f"[DATA_PROVIDER0 --> NEVERMINED] Publishing compute to the data asset for asset0: {ddo_compute0.did}"
    )

    ddo_compute1 = nevermined.assets.create_compute(
        metadata_data1, provider_data1, providers=[provider],
    )
    assert ddo_compute1 is not None, "Creating asset compute1 on-chain failed"
    print(
        f"[DATA_PROVIDER1 --> NEVERMINED] Publishing compute to the data asset for asset1: {ddo_compute1.did}"
    )

    with open("resources/metadata/metadata_compute_coordinator.json") as f:
        metadata_compute_coordinator = json.load(f)
        metadata_compute_coordinator["main"]["dateCreated"] = next(date_created)

    ddo_compute_coordinator = nevermined.assets.create_compute(
        metadata_compute_coordinator, provider_coordinator, providers=[provider],
    )
    assert (
        ddo_compute_coordinator is not None
    ), "Creating asset compute_coordinator on-chain failed"
    print(
        f"[COORDINATOR_PROVIDER --> NEVERMINED] Publishing coordinator compute asset: {ddo_compute_coordinator.did}"
    )

    # 4. Publish algorithm
    with open("resources/metadata/metadata_transformation.json") as f:
        metadata_transformation = json.load(f)
        metadata_transformation["main"]["dateCreated"] = next(date_created)

    ddo_transformation = nevermined.assets.create(
        metadata_transformation, consumer, providers=[provider],
    )
    assert (
        ddo_transformation is not None
    ), "Creating asset transformation on-chain failed"
    print(
        f"[DATA_SCIENTIST --> NEVERMINED] Publishing algorithm asset: {ddo_transformation.did}"
    )

    # 5. Publish the workflows
    with open("resources/metadata/metadata_workflow.json") as f:
        metadata_workflow = json.load(f)
    with open("resources/metadata/metadata_workflow_coordinator.json") as f:
        metadata_workflow_coordinator = json.load(f)

    metadata_workflow0 = copy.deepcopy(metadata_workflow)
    metadata_workflow0["main"]["workflow"]["stages"][0]["input"][0][
        "id"
    ] = ddo_compute0.did
    metadata_workflow0["main"]["workflow"]["stages"][0]["transformation"][
        "id"
    ] = ddo_transformation.did

    metadata_workflow1 = copy.deepcopy(metadata_workflow)
    metadata_workflow1["main"]["workflow"]["stages"][0]["input"][0][
        "id"
    ] = ddo_compute1.did
    metadata_workflow1["main"]["workflow"]["stages"][0]["transformation"][
        "id"
    ] = ddo_transformation.did

    metadata_workflow_coordinator["main"]["dateCreated"] = next(date_created)

    ddo_workflow0 = nevermined.assets.create(
        metadata_workflow0, consumer, providers=[provider],
    )
    assert ddo_workflow0 is not None, "Creating asset workflow0 on-chain failed"
    print(
        f"[DATA_SCIENTIST --> NEVERMINED] Publishing compute workflow for asset0: {ddo_workflow0.did}"
    )

    ddo_workflow1 = nevermined.assets.create(
        metadata_workflow1, consumer, providers=[provider],
    )
    assert ddo_workflow1 is not None, "Creating asset workflow1 on-chain failed"
    print(
        f"[DATA_SCIENTIST --> NEVERMINED] Publishing compute workflow for asset1: {ddo_workflow1.did}"
    )

    ddo_workflow_coordinator = nevermined.assets.create(
        metadata_workflow_coordinator, consumer, providers=[provider],
    )
    assert (
        ddo_workflow_coordinator is not None
    ), "Creating asset workflow_coordinator on-chain failed"
    print(
        f"[DATA_SCIENTIST --> NEVERMINED] Publishing compute workflow for coordinator: {ddo_workflow_coordinator.did}"
    )

    # 6. Order computations
    service0 = ddo_compute0.get_service(service_type=ServiceTypes.CLOUD_COMPUTE)
    service_agreement0 = ServiceAgreement.from_service_dict(service0.as_dictionary())
    agreement_id0 = nevermined.assets.order(
        ddo_compute0.did, service_agreement0.index, consumer, consumer
    )
    print(
        f"[DATA_SCIENTIST --> DATA_PROVIDER0] Requesting an agreement for compute to the data for asset0: {agreement_id0}"
    )

    event = keeper.lock_reward_condition.subscribe_condition_fulfilled(
        agreement_id0, 60, None, (), wait=True
    )
    assert event is not None, "Reward condition is not found"

    event = keeper.compute_execution_condition.subscribe_condition_fulfilled(
        agreement_id0, 60, None, (), wait=True
    )
    assert event is not None, "Execution condition not found"

    service1 = ddo_compute1.get_service(service_type=ServiceTypes.CLOUD_COMPUTE)
    service_agreement1 = ServiceAgreement.from_service_dict(service1.as_dictionary())
    agreement_id1 = nevermined.assets.order(
        ddo_compute1.did, service_agreement1.index, consumer, consumer
    )
    print(
        f"[DATA_SCIENTIST --> DATA_PROVIDER1] Requesting an agreement for compute to the data for asset1: {agreement_id1}"
    )

    event = keeper.lock_reward_condition.subscribe_condition_fulfilled(
        agreement_id1, 60, None, (), wait=True
    )
    assert event is not None, "Reward condition is not found"

    event = keeper.compute_execution_condition.subscribe_condition_fulfilled(
        agreement_id1, 60, None, (), wait=True
    )
    assert event is not None, "Execution condition not found"

    service_coordinator = ddo_compute_coordinator.get_service(
        service_type=ServiceTypes.CLOUD_COMPUTE
    )
    service_agreement_coordinator = ServiceAgreement.from_service_dict(
        service_coordinator.as_dictionary()
    )
    agreement_id_coordinator = nevermined.assets.order(
        ddo_compute_coordinator.did, service_agreement_coordinator.index, consumer, consumer
    )
    print(
        f"[DATA_SCIENTIST --> COORDINATOR_PROVIDER] Requesting an agreement for coordinator compute: {agreement_id_coordinator}"
    )

    event = keeper.lock_reward_condition.subscribe_condition_fulfilled(
        agreement_id_coordinator, 60, None, (), wait=True
    )
    assert event is not None, "Reward condition is not found"

    event = keeper.compute_execution_condition.subscribe_condition_fulfilled(
        agreement_id_coordinator, 60, None, (), wait=True
    )
    assert event is not None, "Execution condition not found"

    # 7. Execute workflows
    compute_coordinator_id = nevermined.assets.execute(
        agreement_id_coordinator,
        ddo_compute_coordinator.did,
        service_agreement_coordinator.index,
        consumer,
        ddo_workflow_coordinator.did,
    )
    print(
        f"[DATA_SCIENTIST --> COORDINATOR_PROVIDER] Requesting execution for coordinator compute: {compute_coordinator_id}"
    )

    compute_asset0_id = nevermined.assets.execute(
        agreement_id0,
        ddo_compute0.did,
        service_agreement0.index,
        consumer,
        ddo_workflow0.did,
    )
    print(
        f"[DATA_SCIENTIST --> DATA_PROVIDER0] Requesting execution for compute to data for asset0: {compute_asset0_id}"
    )

    compute_asset1_id = nevermined.assets.execute(
        agreement_id1,
        ddo_compute1.did,
        service_agreement1.index,
        consumer,
        ddo_workflow1.did,
    )
    print(
        f"[DATA_SCIENTIST --> DATA_PROVIDER1] Requesting execution for compute to data for asset1: {compute_asset1_id}"
    )

    jobs = [
        (agreement_id_coordinator, compute_coordinator_id),
        (agreement_id0, compute_asset0_id),
        (agreement_id1, compute_asset1_id),
    ]
    return jobs


def main():
    """Main routine that calls the demo and waits for the results of the compute
    jobs.

    """
    jobs = demo()

    acc = Account(
        Web3.toChecksumAddress(PARITY_ADDRESS), PARITY_PASSWORD, PARITY_KEYFILE
    )
    nevermined = Nevermined(Config("config.ini"))

    print("Waiting for compute jobs...\n")
    try:
        dids = wait_for_compute_jobs(nevermined, acc, jobs)
    except ValueError:
        print("Some jobs have failed!")

    print("All jobs finished successfully!\n")
    print("Downloading data assets...")
    download(nevermined, acc, dids)


if __name__ == "__main__":
    main()
