import argparse
from nornir import InitNornir
from nornir_salt.plugins.functions import FFun
from nornir_utils.plugins.functions import print_result
from nornir_napalm.plugins.tasks import napalm_configure, napalm_get
from nornir_utils.plugins.tasks.files import write_file
from app.utilities.general_utilities import get_hostnames
from backup_script import get_napalm_backups
import os

# Create config parser to set dry_run when running script
parser = argparse.ArgumentParser()

parser.add_argument(
    "--dry_run", dest="dry", action="store_true", help="Will not run on devices"
)


parser.add_argument(
    "--no_dry_run", dest="dry", action="store_false", help="Will run on devices"
)

parser.add_argument("--list", nargs="*", help="delimited list input", type=str)

parser.add_argument("--hash", help="GitHub Hash for backup", type=str)

parser.set_defaults(dry=True)
parser.set_defaults(hash=None)
args = parser.parse_args()


# Deploy network configuration task to hosts
def deploy_network(task):
    """Configures network with NAPALM"""
    task.run(
        name=f"Configuring {task.host.name}",
        task=napalm_configure,
        filename=f"./crq_configs/{task.host.name}.txt",
        dry_run=args.dry,
        replace=False,
    )


def get_hostnames(list):
    hostnames = [os.path.splitext(x)[0].split("/")[-1] for x in list]
    return hostnames
nr = InitNornir(config_file="./app/config.yaml")

def backup_config(task, path):
    device_config = nr.run(task=napalm_get, getters=["config"])

    task.run(
        task=write_file,
        content=device_config.result["config"]["running"],
        filename=f"{path}/{task.host}.txt",
    )

def main():
    #nr = InitNornir(config_file="./app/config.yaml")
    crqs = get_hostnames(args.list)
    print(f"Checking configuration changes for updated hosts: {crqs}")
    filtered_hosts = FFun(nr, FL=crqs)
    print(args.hash)
    print(type(args.hash))
    filtered_hosts.run(task=get_napalm_backups, hash=args.hash)
    result = filtered_hosts.run(task=deploy_network)
    filtered_hosts.run(task=get_napalm_backups)
    print_result(result)


if __name__ == "__main__":
    main()
