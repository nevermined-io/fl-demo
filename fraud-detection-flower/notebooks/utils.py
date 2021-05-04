from datetime import datetime
import json
from pathlib import Path

RESOURCES_PATH = (Path(__file__).parent / "../resources").resolve().as_posix()


def wait_for_event(keeper, service_agreement_id):
    event = keeper.lock_reward_condition.subscribe_condition_fulfilled(
        service_agreement_id, 60, None, (), wait=True
    )
    assert event is not None, "Reward condition is not found"


def date_now():
    return datetime.utcnow().isoformat(timespec="seconds") + "Z"


def metadata_dataset_template():
    return _load_metadata("metadata_dataset_template.json")


def metadata_compute_template():
    return _load_metadata("metadata_compute_template.json")


def metadata_algorithm_template():
    return _load_metadata("metadata_algorithm_template.json")


def metadata_workflow_template():
    return _load_metadata("metadata_workflow_template.json")


def metadata_workflow_coordinator():
    return _load_metadata("metadata_coordinator.json")


def print_json(d):
    print(json.dumps(d, indent=2))


def _load_metadata(name):
    with open(f"{RESOURCES_PATH}/metadata/{name}") as f:
        return json.load(f)