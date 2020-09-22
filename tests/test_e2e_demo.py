import tempfile

from nevermined_sdk_py import Config, Nevermined
from web3 import Web3
from contracts_lib_py.account import Account

from nevermined_fl_demo.demo import demo
from nevermined_fl_demo.utils import wait_for_compute_jobs
from nevermined_fl_demo.demo import PARITY_ADDRESS, PARITY_PASSWORD, PARITY_KEYFILE
from nevermined_fl_demo.download import download


def test_e2e_demo():
    jobs = demo()
    assert len(jobs) == 3

    nevermined = Nevermined(Config("config.ini"))
    acc = Account(
        Web3.toChecksumAddress(PARITY_ADDRESS), PARITY_PASSWORD, PARITY_KEYFILE
    )
    dids = wait_for_compute_jobs(nevermined, acc, jobs)
    assert len(dids) == 3

    with tempfile.TemporaryDirectory() as tmpdirname:
        download(nevermined, acc, dids, downloads_path=tmpdirname)
