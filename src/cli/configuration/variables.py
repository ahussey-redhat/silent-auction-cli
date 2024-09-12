from cli.adapters.KeycloakInterface import KeycloakInterface

import os
import json
import logging

# Global vars
HOME_DIR = os.environ["HOME"]

# Auth
TOKEN = {}
KC = KeycloakInterface()
with open(f"{HOME_DIR}/.config/.silent-auction.txt", "r") as fp:
    LOAD_TOKEN_FROM_DISK = json.loads(fp.read().strip())

# Backend
BACKEND_BASE_URL=os.environ.get("BACKEND_BASE_URL")

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='(%(threadName)-9s) %(message)s'
)