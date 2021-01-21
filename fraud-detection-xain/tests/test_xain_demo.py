import sys
from pathlib import Path

import papermill as pm


def test_sherpa_demo():
    # 1. run provider notebook
    notebook_path = (
        (Path(__file__).parent / "../notebooks/nevermined_provider.ipynb")
        .resolve()
        .as_posix()
    )
    config_file_path = (Path(__file__).parent / "../config.ini").resolve().as_posix()
    provider_keyfile_path = (
        (Path(__file__).parent / "../resources/accounts/provider.json")
        .resolve()
        .as_posix()
    )

    result = pm.execute_notebook(
        notebook_path,
        "/tmp/out.ipynb",
        progress_bar=False,
        stdout_file=sys.stdout,
        parameters={
            "CONFIG_FILE": config_file_path,
            "PROVIDER_KEYFILE": provider_keyfile_path,
        },
    )

    # get the compute did. the notebook cell are tagged
    compute1_did = None
    compute2_did = None
    compute3_did = None
    for cell in result["cells"]:
        if "compute1_did" in cell["metadata"]["tags"]:
            compute1_did = cell["outputs"][0]["text"].strip().split()[-1]
        elif "compute2_did" in cell["metadata"]["tags"]:
            compute2_did = cell["outputs"][0]["text"].strip().split()[-1]
        elif "compute2_did" in cell["metadata"]["tags"]:
            compute2_did = cell["outputs"][0]["text"].strip().split()[-1]

    # 2. run consumer notebook
    notebook_path = (
        (Path(__file__).parent / "../notebooks/nevermined_consumer.ipynb")
        .resolve()
        .as_posix()
    )
    consumer_keyfile_path = (
        (Path(__file__).parent / "../resources/accounts/consumer.json")
        .resolve()
        .as_posix()
    )
    result = pm.execute_notebook(
        notebook_path,
        "/tmp/out.ipynb",
        progress_bar=False,
        stdout_file=sys.stdout,
        parameters={
            "CONFIG_FILE": config_file_path,
            "CONSUMER_KEYFILE": consumer_keyfile_path,
            "ASSET_COMPUTE_DID_1": compute1_did,
            "ASSET_COMPUTE_DID_2": compute2_did,
            "ASSET_COORDINATOR_DID": compute3_did
        },
    )

    assert result["metadata"]["papermill"]["exception"] is None
