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
        kernel_name="python",
        parameters={
            "CONFIG_FILE": config_file_path,
            "PROVIDER_KEYFILE": provider_keyfile_path,
        },
    )

    # get the compute did. the notebook cell is tagged with `compute_did`
    compute_did = None
    for cell in result["cells"]:
        if "compute_did" in cell["metadata"]["tags"]:
            compute_did = cell["outputs"][0]["text"].strip().split()[-1]
    print(f"COMPUTE_DID: {compute_did}")

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
        kernel_name="python",
        parameters={
            "CONFIG_FILE": config_file_path,
            "CONSUMER_KEYFILE": consumer_keyfile_path,
            "ASSET_DID": compute_did,
        },
    )

    assert result["metadata"]["papermill"]["exception"] is None
