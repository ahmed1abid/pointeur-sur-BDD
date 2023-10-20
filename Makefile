# Commands
PYTHON = python3
PIP = pip
TRUFFLE = truffle
GANACHE = ganache-cli
GANACHE_PORT = 8545

# User CLI file
USER_CLI = cli.py

# Issuer CLI file
ISSUER_CLI = issuer_cli.py

# Ethereum Smart Contracts directory
CONTRACTS_DIR = ./contracts

# Truffle Configuration
TRUFFLE_CONFIG = truffle-config.js

# Run the user CLI
run-user:
	$(PYTHON) $(USER_CLI)

# Run the issuer CLI
run-issuer:
	$(PYTHON) $(ISSUER_CLI)

# Install Python dependencies
install-python-deps:
	$(PIP) install -r requirements.txt

# Start the Ganache development blockchain
start-ganache:
	$(GANACHE) -p $(GANACHE_PORT) --deterministic --accounts 6

# Deploy smart contracts using Truffle
deploy-contracts:
	$(TRUFFLE) migrate --reset --config $(TRUFFLE_CONFIG)

# Deploy smart contracts using Truffle
compile-contracts:
	$(TRUFFLE) compile

# Phony targets
.PHONY: run-user run-issuer install-python-deps start-ganache deploy-contracts initialize-user display-wallet set-issuer get-cert start-ganache deploy-contracts compile-contracts
