#
# Used to provide a common interface for Keycloak integration
#
import os
import json
import datetime
import base64

from typer import prompt, Argument
from keycloak import KeycloakOpenID

HOME_DIR = os.environ["HOME"]

def generate_token(keycloak_openid):
    username = prompt("What's your username?")
    password = prompt("What's your password?", hide_input=True)
    token = keycloak_openid.token(
        username,
        password,
        grant_type="password",
        scope="openid"
    )
    with open(f"{HOME_DIR}/.config/.silent-auction.txt", "w") as fp:
        fp.write(json.dumps(token))
    return token

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
            with open(f"{HOME_DIR}/.config/.silent-auction.txt", "r") as fp:
                load_token = json.loads(fp.read().strip())
                access_token_parts = load_token['access_token'].split('.')
                access_token_payload = json.loads(base64.urlsafe_b64decode(access_token_parts[1] + '=' * (4 - len(access_token_parts[1]) % 4)))

                now = datetime.datetime.now()
                access_token_exp = datetime.datetime.fromtimestamp(access_token_payload['exp'])
                access_token_exp_minus_seconds = access_token_exp - datetime.timedelta(seconds=100)

                if now > access_token_exp:
                    print("Session expired. Please log in again.")
                    return generate_token(self.keycloak_openid)
                if access_token_exp_minus_seconds <= now < access_token_exp:
                    # print("Token expired. Refreshing")
                    try:
                        self.token = self.refresh_token(load_token)
                        return self.token
                    except BaseException as e:
                        print(e)
                        return generate_token(self.keycloak_openid)
                return load_token
        except BaseException as e:
            print(e)
            return generate_token(self.keycloak_openid)

    def get_user_info(self):
        # Get Userinfo
        userinfo = self.keycloak_openid.userinfo(self.token['access_token'])
        return userinfo

    def refresh_token(self, token):
        # Refresh token
        return self.keycloak_openid.refresh_token(token['refresh_token'])

    def logout(self):
        # Logout
        self.keycloak_openid.logout(self.token['refresh_token'])