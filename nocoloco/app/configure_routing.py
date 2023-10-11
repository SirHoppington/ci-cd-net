import argparse
from nornir import InitNornir
from nornir_salt.plugins.functions import FFun
from nornir_utils.plugins.functions import print_result
from nornir_jinja2.plugins.tasks import template_file
from nornir_utils.plugins.tasks.data import load_yaml
from nornir_napalm.plugins.tasks import napalm_configure
from nornir_netmiko.tasks import netmiko_send_config
from utilities.general_utilities import get_hostnames
from backup_script import get_napalm_backups
import os

# Create config parser to set dry_run when running script
parser = argparse.ArgumentParser()

parser.add_argument(
    "--dry_run", dest="dry", action="store_true", help="Will not run on devices"
)


parser.add_argument("--list", nargs="*", help="delimited list input", type=str)

parser.add_argument(
    "--no_dry_run", dest="dry", action="store_false", help="Will run on devices"
)

parser.add_argument("--hash", help="GitHub Hash for backup", type=str)

parser.set_defaults(dry=True)
parser.set_defaults(hash=None)
args = parser.parse_args()


# Deploy network configuration task to hosts
def deploy_routing(task):
    """Configures network with NAPALM"""
    data = task.run(
        name=f"Loading YAML for {task.host.name}",
        task=load_yaml,
        file=f"./inventory/hosts.yaml",
    )
    task.host["routing"] = data.result[task.host.name]["routing"]
    r = task.run(task=template_file, template=f"routing.j2", path="./config_templates")
    task.host["config"] = r.result
    string_config = str(task.host["config"])
    print(string_config)
    configure = task.run(
        name=f"Configuring {task.host.name}",
        task=napalm_configure,
        #filename="./hosts.txt",
        configuration=string_config,
        dry_run=args.dry,
        replace=False,
    )
    print_result(configure)

def get_hostnames(list):
    hostnames = [os.path.splitext(x)[0].split("/")[-1] for x in list]
    return hostnames

def main():
    nr = InitNornir(config_file="config.yaml")
    crqs = get_hostnames(args.list)
    print(f"Checking configuration changes for updated hosts: {crqs}")
    filtered_hosts = FFun(nr, FL=crqs)
    filtered_hosts.run(task=get_napalm_backups, hash=args.hash)
    result = filtered_hosts.run(task=deploy_routing)
    filtered_hosts.run(task=get_napalm_backups)


if __name__ == "__main__":
    main()
