import tempfile
from pathlib import Path

from contracts_lib_py.account import Account
from nevermined_fl_demo.demo import (PARITY_ADDRESS, PARITY_KEYFILE,
                                     PARITY_PASSWORD, demo)
from nevermined_fl_demo.download import download
from nevermined_fl_demo.utils import wait_for_compute_jobs
from nevermined_sdk_py import Config, Nevermined
from web3 import Web3


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
        path = Path(tmpdirname)
        filenames = [f.name for f in path.rglob("*") if f.is_file()]

    # check that we get the output of the participants
    assert filenames.count("perf.txt") == 2

    # check that we get the models from the coordinator
    for i in range(10):
        assert filenames.count(f"model_{i}.npy") == 1
