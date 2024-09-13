#!/usr/bin/env python3
#
# This application is the command line interface to the Silent Auction application
#

import cli.adapters.SchedulerInterface as SchedulerInterface
import cli.adapters.AuctionInterface as AuctionInterface
import cli.adapters.BidInterface as BidInterface

import cli.configuration.variables as app_variables

from typer_shell import make_typer_shell

import base64
import json
import logging

def shell_prompt():
    app_variables.KC.get_token()
    access_token = app_variables.TOKEN['access_token']
    access_token_payload =  json.loads(base64.urlsafe_b64decode((access_token.split('.')[1]) + '=' * (4 - len((access_token.split('.')[1])) % 4)))
    return f"silent-auction-cli ({access_token_payload['preferred_username']}): "

app = make_typer_shell(
    prompt=shell_prompt(),
    intro="Starting the Silent Auction CLI application",
)

app.add_typer(AuctionInterface.app, name="auctions")
app.add_typer(BidInterface.app, name="bids")

@app.command()
def show_token():
    print(f"Token: {app_variables.TOKEN}")

@app.command()
def login():
    app_variables.KC.get_token()
    logging.debug(app_variables.TOKEN)

@app.command()
def logout():
    app_variables.KC.logout(app_variables.TOKEN)

def main():
    scheduler = SchedulerInterface.SchedulerInterface()
    scheduler.start()
    app()

if __name__ == "__main__":
    main()