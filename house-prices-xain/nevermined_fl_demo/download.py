"""Download data asset files"""

from pathlib import Path

DOWNLOADS_PATH = Path("./downloads")


def download(nevermined, account, dids, downloads_path=DOWNLOADS_PATH.as_posix()):
    """Download data assets.

    nevermined (:py:class:`nevermined_sdk_py.Nevermined`): A nevermined instace.
    account (:py:class:`contracts_lib_py.account.Account`): Account that published
        the compute jobs.
    dids (list): A list of dids to download
    downloads_path (str, Optional): The path to store the downloaded files.
        Defaults to `./downloads`

    """
    for did in dids:
        ddo = nevermined.assets.resolve(did)
        service_agreement = ddo.get_service("access")

        nevermined.assets.download(
            did, service_agreement.index, account, downloads_path,
        )
        print(f"Downloaded asset {did}")
