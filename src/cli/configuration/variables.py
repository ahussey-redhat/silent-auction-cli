from cli.adapters.KeycloakInterface import KeycloakInterface

import os
import logging

# Auth
KC = KeycloakInterface()
TOKEN = KC.get_token()

# Backend
BACKEND_BASE_URL=os.environ.get("BACKEND_BASE_URL")

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='(%(threadName)-9s) %(message)s'
)