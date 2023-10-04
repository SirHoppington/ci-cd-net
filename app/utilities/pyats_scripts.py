from genie.testbed import load
from utilities.pyats_config_clean import clean_ios_pyats


# load the testbed file
testbed = load('inventory/testbed.yaml')


# iterate through each device in testbed and save config to txt new txt file using pyats
for name, device in testbed.devices.items():
    device.connect()
    output = device.learn('config')
    with open(f'./gold_config/{name}.txt', 'w') as file:
        for key, value in output.items():
            file.write('%s\n' % (key))
            for key, items in value.items():
                file.write(' %s\n' % (key))
            if key == "certificate ca 01":
                for key, item in value.items():
                    for k, v in item.items():
                        file.write('  %s \n' % (k))
                file.write('  \tquit\n')
            if key == "certificate self-signed 01":
                for key, item in value.items():
                    for k, v in item.items():
                        file.write('  %s \n' % (k))
                file.write('  \tquit\n')


clean_ios_pyats()
