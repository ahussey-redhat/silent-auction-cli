#
# Used to provide a common interface for Keycloak integration
#
import cli.configuration.variables as app_variables

import os
import json
import logging
import datetime
import base64

from typer import prompt, Argument
from keycloak import KeycloakOpenID

def generate_token(keycloak_openid):
    username = prompt("What's your username?")
    password = prompt("What's your password?", hide_input=True)
    token = keycloak_openid.token(
        username,
        password,
        grant_type="password",
        scope="openid"
    )
    with open(f"{app_variables.HOME_DIR}/.config/.silent-auction.txt", "w") as fp:
        fp.write(json.dumps(token))
    app_variables.TOKEN = token

class KeycloakInterface:
    def __init__(self):
        client_secret_key = os.environ.get("CLIENT_SECRET_KEY")

        self.keycloak_openid = KeycloakOpenID(
             server_url="https://sso.bastion.blueguardian.co/auth",
             client_id="cli",
             realm_name="silent-auction",
             client_secret_key=client_secret_key,
             verify=True
        )

    def get_token(self):
        try:
            app_variables.TOKEN = app_variables.LOAD_TOKEN_FROM_DISK
            access_token_parts = app_variables.TOKEN['access_token'].split('.')
            access_token_payload = json.loads(base64.urlsafe_b64decode(access_token_parts[1] + '=' * (4 - len(access_token_parts[1]) % 4)))

            now = datetime.datetime.now()
            access_token_exp = datetime.datetime.fromtimestamp(access_token_payload['exp'])
            access_token_exp_minus_seconds = access_token_exp - datetime.timedelta(seconds=100)

            if now > access_token_exp:
                logging.warning("Session expired. Please log in again.")
                return generate_token(self.keycloak_openid)
            if access_token_exp_minus_seconds <= now < access_token_exp:
                logging.debug("Token expired. Refreshing")
                try:
                    self.refresh_token(app_variables.TOKEN)
                except BaseException as e:
                    print(e)
                    generate_token(self.keycloak_openid)
        except BaseException as e:
            logging.warning(e)
            generate_token(self.keycloak_openid)

    def get_user_info(self):
        # Get Userinfo
        userinfo = self.keycloak_openid.userinfo(self.token['access_token'])
        return userinfo

    def refresh_token(self, token):
        # Refresh token
        with open(f"{app_variables.HOME_DIR}/.config/.silent-auction.txt", "w") as fp:
            token = self.keycloak_openid.refresh_token(token['refresh_token'])
            fp.write(json.dumps(token))
        return token

    def logout(self, token):
        # Logout
        self.keycloak_openid.logout(token['refresh_token'])
        with open(f"{app_variables.HOME_DIR}/.config/.silent-auction.txt", "w") as fp:
            fp.write(json.dumps("{}"))
