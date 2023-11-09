import yaml
import json
from termcolor import colored
from web3 import Web3
from User import User
import json

# Load the contract ABI and address from the JSON file
with open("./build/contracts/DataRegistry.json", "r") as json_file:
    contract_data = json.load(json_file)

# Extract the contract ABI and address
contract_abi = contract_data["abi"]
contract_address = contract_data["networks"]["5777"]["address"]

name = "DIMS"
wallet_file = None
user = None
ssn = None
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
data_registry = w3.eth.contract(address=contract_address, abi=contract_abi)

# Select a specific user address for testing (use one of the sample addresses)
user_address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"

while True:
    print("# " + name + "> ", end="")
    inp = input()
    inp_list = inp.split(' ')

    if inp_list[0] in ['initialize', 'init']:
        if inp_list[1] in ['user']:
            print("Enter your name: ", end = "")
            name = input()
            print("Hello " + colored(name, 'blue'))
            print("Please give your wallet file path: ", end = "")
            wallet_file = input() or "wallet.yaml"
    
            print("Enter your ssn: ", end = "")
            ssn = int(input())
            print("Your SSN: " + colored(ssn, 'blue'))

            print("Enter your data: ", end = "")
            data = input()
            
        
            
            try:
                user = User(name=name, wallet_file=wallet_file, ssn=ssn,data=data)
                user.encrypt_data()
                print("Wallet Loaded")

            except Exception as e:
                print("Error in loading wallet")
                raise e

    if inp_list[0] in ['display', 'show', 'view']:
        if inp_list[1] in ['user_data']:
            if user is None:
                print('User is None, use "init user"')
                continue

            print("User Name: " + user.name)
            print("User SSN: " + str(user.ssn))
            
            if user.wallet:
                print("Certificates available: " + str(user.wallet.keys()))
                for cert_name in user.wallet.keys():
                    print("*********" + colored('CERTIFICATE', 'red') + ": " + colored("{}".format(cert_name), 'yellow') + " ***********\n")
                    cert_file = user.wallet[cert_name]
                    cert_data = yaml.safe_load(open(cert_file))
                    for attr, value in cert_data.items():
                        if attr != 'Attributes':
                            print(colored(attr, 'blue') + " : " + colored(str(value), 'green'))
                        else:
                            for ind_attr, ind_value in value.items():
                                print('\t' + colored(ind_attr, 'blue') + ' : ' + colored(str(ind_value), 'green'))
                    print("\n*************************************************\n")

    if inp_list[0] in ['send', 'store', 'upload']:
        if inp_list[1] in ['data']:
                if user.data:
                        data_to_store = user.data
                        if data_to_store:
                            data_to_store_hex = "0x" + data_to_store.encode('utf-8').hex()

                            # Fetch the latest nonce and chain ID
                            nonce = w3.eth.get_transaction_count(user_address)
                            chain_id = w3.eth.chain_id

                            # Encode the function call
                            transaction = data_registry.functions.storeData(data_to_store_hex).build_transaction({
                                    'gas': 2000000,
                                    'gasPrice': 20000000000,
                                    'from': user_address,
                                    'nonce': nonce,
                                    'chainId': chain_id
                                })

                            tx_hash = w3.eth.send_transaction(transaction)
                            print("Data sent to the blockchain. Transaction Hash:", tx_hash.hex())
                        else:
                            print("No data to send.")
                else:
                        print("User address is not set. Make sure to set it to your Ethereum address.")
