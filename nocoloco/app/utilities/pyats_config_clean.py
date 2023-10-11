import os
# Open Golden Config file and remove first 2 lines of each file:

def clean_ios_pyats():
    for file in os.listdir("./gold_config"):
        with open(f"./gold_config/{file}", 'r') as fin:
            data = fin.read().splitlines(True)
        with open(f"./gold_config/{file}", 'w') as fout:
            fout.writelines(data[2:])

# Open Golden Config file and remove first 3 lines of each file:
def clean_ios_nornir():
    for file in os.listdir("./snapshots/configs"):
        with open(f"./snapshots/configs/{file}", 'r') as fin:
            data = fin.read().splitlines(True)
        with open(f"./snapshots/configs/{file}", 'w') as fout:
            fout.writelines(data[3:])
