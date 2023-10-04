import argparse
from nornir import InitNornir
from nornir_salt.plugins.functions import FFun
from nornir_utils.plugins.functions import print_result
from nornir_napalm.plugins.tasks import napalm_get, napalm_cli, napalm_configure
from nornir.core.task import Task
from utilities.check_config_changes import compare_changes
from backup_script import post_change_backup
import os 

# Create config parser to set dry_run when running script
parser = argparse.ArgumentParser()


parser.add_argument(
    "--dry_run", dest="dry", action="store_true", help="Will not run on devices"
)


parser.add_argument(
    "--no_dry_run", dest="dry", action="store_false", help="Will run on devices"
)

parser.add_argument('--list', nargs='*', help='delimited list input', type=str)

parser.set_defaults(dry=True)
args = parser.parse_args()


# Deploy network configuration task to hosts
def deploy_network(task):
    """Configures network with NAPALM"""
    task.run(
        name=f"Configuring {task.host.name}!",
        task=napalm_configure,
        filename=f"crq_changes/{task.host.name}.txt",
        dry_run=args.dry,
        replace=False
    )

def get_hostnames(list):
    #hostnames = [host.split("/"[-1]) for host in list ]
    hostnames = [os.path.splitext(x)[0].split("/")[-1] for x in list]
    print(f"These hostnames {hostnames}")
    return hostnames




def main():
    nr = InitNornir(
        config_file="config.yaml")
    print(args.list)
    compare = compare_changes()
    print(f"These compared: {compare}")
    #crqs = args.list
    crqs = get_hostnames(args.list)
    filtered_hosts = FFun(nr, FL=crqs)
    result = filtered_hosts.run(task=deploy_network)
    print_result(result)
    post_change_backup(filtered_hosts)
# Add line to update Golden config after change?


if __name__ == "__main__":
    main()
