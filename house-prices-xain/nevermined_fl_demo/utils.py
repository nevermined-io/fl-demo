"""Demo utils"""

import datetime
import time

def dates_generator():
    """Generates a new unique date on each call.

    Useful so that we create a new did every time we call the demo and avoid
    duplicated DID errors.

    Yields:
        str: ISO formated date with second accuracy

    """
    now = datetime.datetime.utcnow()
    delta = datetime.timedelta(seconds=1)
    while True:
        now += delta
        yield now.isoformat(timespec="seconds") + "Z"


def wait_for_compute_jobs(nevermined, account, jobs):
    """Monitor and wait for compute jobs to finish.

    Args:
        nevermined (:py:class:`nevermined_sdk_py.Nevermined`): A nevermined instance.
        account (:py:class:`contracts_lib_py.account.Account`): Account that published
            the compute jobs.
            jobs (:obj:`list` of :obj:`tuple`): A list of tuples with each tuple
                containing (service_agreement_id, compute_job_id).

    Returns:
        :obj:`list` of :obj:`str`: Returns a list of dids produced by the jobs

    Raises:
        ValueError: If any of the jobs fail

    """
    failed = False
    dids = set()
    while True:
        finished = 0

        for i, (sa_id, job_id) in enumerate(jobs):
            status = nevermined.assets.compute_status(sa_id, job_id, account)
            print(f"{job_id}: {status['status']}")

            if status["status"] == "Failed":
                logs = nevermined.assets.compute_logs(sa_id, job_id, account)
                print(logs)
                failed = True
            if status["status"] == "Succeeded":
                finished += 1
                dids.add(status["did"])

        if failed:
            raise ValueError("Some jobs failed")
        if finished == len(jobs):
            break
        # move up 4 lines
        print("\u001B[4A")
        time.sleep(5)

    return list(dids)
