import os
import shutil
from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get, napalm_cli
from nornir.core.filter import F
BACKUP_DIR = "gold_config"

# Initiate Nornir object via config file
nr = InitNornir(
    config_file="./config.yaml")


# Function to create backup directory if it doesn't already exist
def create_backups_dir():
    if not os.path.exists(BACKUP_DIR):
        os.mkdir(BACKUP_DIR)


# Function to save configuration to a txt file with hostname
def save_config_to_file(hostname, config):
    filename = f"{hostname}.txt"
    with open(os.path.join(BACKUP_DIR, filename), "w") as f:
        f.write(config)


# Use Napalm backup feature to retrieve backup for IOS devices
def get_napalm_backups():
    prod_devices = nr.filter(F(groups__contains='prod'))
    backup_results = prod_devices.run(task=napalm_get, getters=["config"])
    for hostname in backup_results:
        config = backup_results[hostname][0].result["config"]["running"]
        save_config_to_file(hostname=hostname, config=config)
        shutil.copy(f"./gold_config/{hostname}.txt", f"./crq_configs/{hostname}.txt")


# Function to update the golden config for devices within the "devices" Nornir object
def post_change_backup(devices):
    backup_results = devices.run(task=napalm_get, getters=["config"])
    for hostname in backup_results:
        config = backup_results[hostname][0].result["config"]["running"]
        save_config_to_file(hostname=hostname, config=config)

# Manual alternative backup using napalm_cli to retrieve backup for IOS devices
# def get_napalm_backups():
#    backup_results = nr.run(task=napalm_cli, commands=["show running-config"])
#
#    for hostname in backup_results:
#        config = backup_results[hostname][0].result["show running-config"]
#        save_config_to_file(hostname=hostname, config=config)


def main():
    create_backups_dir()
    get_napalm_backups()


if __name__ == "__main__":
    main()
