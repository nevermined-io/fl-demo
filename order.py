from pathlib import Path
from os import sys

from contracts_lib_py.account import Account
from nevermined_sdk_py import Config, Nevermined
from nevermined_sdk_py.nevermined.keeper import NeverminedKeeper as Keeper
from web3 import Web3

PARITY_ADDRESS = "0x068ed00cf0441e4829d9784fcbe7b9e26d4bd8d0"
PARITY_PASSWORD = "secret"
PARITY_KEYFILE = "resources/accounts/provider.json"

DOWNLOADS_PATH = Path("./downloads")


def order(did):
    # 1. Setup nevermined
    nevermined = Nevermined(Config("config.ini"))
    keeper = Keeper.get_instance()

    # 2. Setup accounts
    consumer = Account(
        Web3.toChecksumAddress(PARITY_ADDRESS), PARITY_PASSWORD, PARITY_KEYFILE
    )

    ddo = nevermined.assets.resolve(did)
    service_agreement = ddo.get_service("access")

    service_agreement_id = nevermined.assets.order(
        did, service_agreement.index, consumer
    )
    print(f"Ordered asset {did} with service agreement {service_agreement_id}")

    nevermined.assets.access(
        service_agreement_id,
        did,
        service_agreement.index,
        consumer,
        DOWNLOADS_PATH.as_posix(),
    )
    print(f"Downloaded asset {did}")


if __name__ == "__main__":
    order(sys.argv[1])
