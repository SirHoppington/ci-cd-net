import argparse
from nornir import InitNornir
from nornir_salt.plugins.functions import FFun
from nornir_utils.plugins.functions import print_result
from nornir_napalm.plugins.tasks import napalm_configure, napalm_get
from nornir_utils.plugins.tasks.files import write_file
from utilities.general_utilities import get_hostnames
import os

PATH="./crq_backups"

nr = InitNornir(config_file="./config.yaml")

def backup_config(task, path):
    device_config = nr.run(task=napalm_get, getters=["config"])
    print(device_config[task.host.name].result["config"]["running"])

    task.run(
        task=write_file,
        content=device_config[task.host.name].result["config"]["running"],
        filename=f"{path}/{task.host}.txt",
    )

result = nr.run(
    name="Backup Device configurations", path=PATH, task=backup_config
)
print_result(result)