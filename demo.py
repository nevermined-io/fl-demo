import copy
import datetime
import json
import sys

from common_utils_py.agreements.service_agreement import ServiceAgreement
from common_utils_py.agreements.service_factory import ServiceDescriptor
from common_utils_py.agreements.service_types import ServiceTypes
from contracts_lib_py.account import Account
from nevermined_sdk_py import Config, Nevermined
from nevermined_sdk_py.gateway import GatewayProvider
from nevermined_sdk_py.nevermined.keeper import NeverminedKeeper as Keeper
from web3 import Web3


ACCOUNT_1_ADDRESS = "0x00Bd138aBD70e2F00903268F3Db08f2D25677C9e"
ACCOUNT_1_PASSWORD = "node0"
ACCOUNT_1_KEYFILE = "resources/accounts/key_file_2.json"

ACCOUNT_2_ADDRESS = "0x068ed00cf0441e4829d9784fcbe7b9e26d4bd8d0"
ACCOUNT_2_PASSWORD = "secret"
ACCOUNT_2_KEYFILE = "resources/accounts/key_file_provider_data0.json"


DS_ACCOUNT_ADDRESS = ACCOUNT_1_ADDRESS # 0x00Bd1
DS_ACCOUNT_PASSWORD = ACCOUNT_1_PASSWORD
DS_ACCOUNT_KEYFILE = ACCOUNT_1_KEYFILE

PROVIDER_1_ACCOUNT_ADDRESS = ACCOUNT_2_ADDRESS # 0x00Bd1
PROVIDER_1_ACCOUNT_PASSWORD = ACCOUNT_2_PASSWORD # 0x068e
PROVIDER_1_ACCOUNT_KEYFILE = ACCOUNT_2_KEYFILE

PROVIDER_2_ACCOUNT_ADDRESS = ACCOUNT_2_ADDRESS # 0x00Bd1
PROVIDER_2_ACCOUNT_PASSWORD = ACCOUNT_2_PASSWORD # 0x068e
PROVIDER_2_ACCOUNT_KEYFILE = ACCOUNT_2_KEYFILE


# Disable warnings emitted by web3
if not sys.warnoptions:
    import warnings

    warnings.simplefilter("ignore")


# this is so that we can change the `dateCreated` field in the ddos so that we
# avoid problems with duplicated ddos when running the demo
def dates_generator():
    now = datetime.datetime.utcnow()
    delta = datetime.timedelta(seconds=1)
    while True:
        now += delta
        yield now.isoformat(timespec="seconds") + "Z"


def demo():
    # 1. Setup nevermined
    # 2. Setup accounts
    # 3. Publish assets
    # 4. Publish compute?
    # 5. Publish algorithm
    # 6. Start coordinator
    # 7. Publish workflows
    # 8. Order assets and execute computations

    date_created = dates_generator()

    # 1. Setup nevermined
    nevermined = Nevermined(Config("config.ini"))
    keeper = Keeper.get_instance()
    gateway = GatewayProvider.get_gateway()
    # provider = PARITY_ADDRESS

    # 2. Setup accounts
    ds_account = Account(Web3.toChecksumAddress(DS_ACCOUNT_ADDRESS), DS_ACCOUNT_PASSWORD, DS_ACCOUNT_KEYFILE)
    prov1_account = Account(Web3.toChecksumAddress(PROVIDER_1_ACCOUNT_ADDRESS), PROVIDER_1_ACCOUNT_PASSWORD, PROVIDER_1_ACCOUNT_KEYFILE)
    prov2_account = Account(Web3.toChecksumAddress(PROVIDER_2_ACCOUNT_ADDRESS), PROVIDER_2_ACCOUNT_PASSWORD, PROVIDER_2_ACCOUNT_KEYFILE)

    # provider_data0 = acc
    # provider_data1 = acc
    # provider_coordinator = acc
    # consumer = acc

    # 3. Getting the Metadata
    with open("resources/metadata/metadata0.json") as f:
        metadata_data1 = json.load(f)
        metadata_data1["main"]["dateCreated"] = next(date_created)
    with open("resources/metadata/metadata1.json") as f:
        metadata_data2 = json.load(f)
        metadata_data2["main"]["dateCreated"] = next(date_created)
    with open("resources/metadata/metadata_compute0.json") as f:
        metadata_compute1 = json.load(f)
        metadata_compute1["main"]["dateCreated"] = next(date_created)
    with open("resources/metadata/metadata_compute1.json") as f:
        metadata_compute2 = json.load(f)
        metadata_compute2["main"]["dateCreated"] = next(date_created)

    # We don't need that part, we just only need to create 2 compute services
    #
    # ddo_data0 = nevermined.assets.create(
    #     metadata_data0,
    #     provider_data0,
    #     providers=[provider],
    # )
    # assert ddo_data0 is not None, "Creating asset data0 on-chain failed"
    # print(f"Created asset data0: {ddo_data0.did}")
    #
    # ddo_data1 = nevermined.assets.create(
    #     metadata_data1,
    #     provider_data1,
    #     providers=[provider],
    # )
    # assert ddo_data1 is not None, "Creating asset data1 on-chain failed"
    # print(f"Created asset data1: {ddo_data1.did}")

    # 4 Publish compute
    # TODO: We probably also need a compute for the coordinator?

    compute_service_attributes = nevermined.assets._build_compute(metadata_compute1,                                                                  prov1_account)
    compute_service_type1 = [ServiceDescriptor.compute_service_descriptor(
        compute_service_attributes, gateway.get_execute_endpoint(nevermined.assets._config))
    ]

    ddo_compute1 = nevermined.assets.create(
        metadata_compute1,
        prov1_account,
        service_descriptors=compute_service_type1,
        providers=[prov1_account.address],
        authorization_type='PSK-RSA'
    )
    assert ddo_compute1 is not None, "Creating asset compute1 on-chain failed"
    print(f"Created Compute Service {ddo_compute1.did} using account {prov1_account.address}")


    compute_service_attributes = nevermined.assets._build_compute(metadata_compute2,                                                                  prov1_account)
    compute_service_type2 = [ServiceDescriptor.compute_service_descriptor(
        compute_service_attributes, gateway.get_execute_endpoint(nevermined.assets._config))
    ]

    ddo_compute2 = nevermined.assets.create(
        metadata_compute2,
        prov2_account,
        service_descriptors=compute_service_type2,
        providers=[prov2_account.address],
        authorization_type='PSK-RSA'
    )
    assert ddo_compute2 is not None, "Creating asset compute2 on-chain failed"
    print(f"Created Compute Service {ddo_compute2.did} using account {prov2_account.address}")


    # 5. Publish algorithm
    with open("resources/metadata/metadata_transformation.json") as f:
        metadata_transformation = json.load(f)
        metadata_transformation["main"]["dateCreated"] = next(date_created)

    ddo_transformation = nevermined.assets.create(
        metadata_transformation,
        ds_account,
        providers=[prov1_account.address, prov2_account.address],
    )
    assert (
            ddo_transformation is not None
    ), "Creating asset transformation on-chain failed"
    print(f"Created algorithm: {ddo_transformation.did} using account {ds_account.address}")

    # 6. Start coordinator
    # TODO

    # 7. Publish the workflows
    with open("resources/metadata/metadata_workflow.json") as f:
        metadata_workflow = json.load(f)

    metadata_workflow_copy1 = copy.deepcopy(metadata_workflow)
    metadata_workflow_copy1["main"]["workflow"]["stages"][0]["input"][0][
        "id"
    ] = ddo_compute1.did
    metadata_workflow_copy1["main"]["workflow"]["stages"][0]["transformation"][
        "id"
    ] = ddo_transformation.did

    ddo_workflow1 = nevermined.assets.create(
        metadata_workflow_copy1,
        ds_account,
        providers=[prov1_account.address, prov2_account.address],
    )
    assert ddo_workflow1 is not None, "Creating asset workflow0 on-chain failed"
    print(f"Created Workflow: {ddo_workflow1.did} using account {ds_account.address}")

    metadata_workflow_copy2 = copy.deepcopy(metadata_workflow)
    metadata_workflow_copy2["main"]["workflow"]["stages"][0]["input"][0][
        "id"
    ] = ddo_compute2.did
    metadata_workflow_copy2["main"]["workflow"]["stages"][0]["transformation"][
        "id"
    ] = ddo_transformation.did

    ddo_workflow2 = nevermined.assets.create(
        metadata_workflow_copy2,
        ds_account,
        providers=[prov1_account.address, prov2_account.address],
    )

    # 8. Order computations
    nevermined.accounts.request_tokens(ds_account, 100)

    service1 = ddo_compute1.get_service(service_type=ServiceTypes.CLOUD_COMPUTE)
    service_agreement1 = ServiceAgreement.from_service_dict(service1.as_dictionary())
    agreement_id1 = nevermined.assets.order(
        ddo_compute1.did, service_agreement1.index, ds_account
    )
    print(f"Placed order for compute service 1: {agreement_id1}")

    event = keeper.lock_reward_condition.subscribe_condition_fulfilled(
        agreement_id1, 60, None, (), wait=True
    )
    assert event is not None, "Lock Reward condition is not found"
    print(f"Lock Reward condition fulfilled for compute1")

    # event = keeper.compute_execution_condition.subscribe_condition_fulfilled(
    #     agreement_id1, 60, None, (), wait=True
    # )
    # assert event is not None, "Execution condition not found"
    # print(f"Execution condition fulfilled for compute0")

    service2 = ddo_compute2.get_service(service_type=ServiceTypes.CLOUD_COMPUTE)
    service_agreement2 = ServiceAgreement.from_service_dict(service2.as_dictionary())
    agreement_id2 = nevermined.assets.order(
        ddo_compute1.did, service_agreement2.index, ds_account
    )
    print(f"Placed order for compute service 2: {agreement_id2}")

    event = keeper.lock_reward_condition.subscribe_condition_fulfilled(
        agreement_id2, 60, None, (), wait=True
    )
    assert event is not None, "Lock Reward condition is not found"
    print(f"Lock Reward condition fulfilled for compute2")

    # event = keeper.compute_execution_condition.subscribe_condition_fulfilled(
    #     agreement_id1, 60, None, (), wait=True
    # )
    # assert event is not None, "Execution condition not found"
    # print(f"Execution condition fulfilled for compute1")

    # 9. Execute workflows
    nevermined.assets.execute(
        agreement_id1,
        ddo_compute1.did,
        service_agreement1.index,
        ds_account,
        ddo_workflow1.did,
    )
    print(f"Executed workflow1")


    nevermined.assets.execute(
        agreement_id2,
        ddo_compute2.did,
        service_agreement2.index,
        ds_account,
        ddo_workflow2.did,
    )
    print(f"Executed workflow2")

if __name__ == "__main__":
    demo()
