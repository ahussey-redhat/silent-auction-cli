#!/usr/bin/env python3
from datetime import datetime
from multiprocessing.spawn import freeze_support
from os import access

#
# This application is the command line interface to the Silent Auction application
#

import cli.repositories.Auction
import cli.repositories.Bid as Bid
import cli.repositories.User as User

import cli.adapters.KeycloakInterface
import cli.adapters.SchedulerInterface as SchedulerInterface

import cli.configuration.variables as app_variables

from typer_shell import make_typer_shell
from typer import prompt

import base64
import json
import logging

from pygments import highlight
from pygments.formatters.terminal256 import Terminal256Formatter
from pygments.lexers.data import JsonLexer

#
# Global variables
#
# - Auction Class
AUCTION = cli.repositories.Auction.Auction()
# - Authentication Scheduler
SCHEDULER = SchedulerInterface.SchedulerInterface()


def shell_prompt():
    access_token = app_variables.TOKEN['access_token']
    access_token_payload =  json.loads(base64.urlsafe_b64decode((access_token.split('.')[1]) + '=' * (4 - len((access_token.split('.')[1])) % 4)))
    return f"silent-auction-cli ({access_token_payload['preferred_username']}): "

app = make_typer_shell(
    prompt=shell_prompt(),
    intro="Starting the Silent Auction CLI application"
)

@app.command()
def show_token():
    print(f"Token: {app_variables.TOKEN}")

@app.command()
def list_auctions():
    raw_json_response = json.dumps(AUCTION.list_auctions(), indent=2)
    print(
        highlight(
            raw_json_response,
            lexer=JsonLexer(),
            formatter=Terminal256Formatter()
        )
    )

@app.command()
def create_auction(name: str, description: str, start: datetime, end: datetime, starting_bid: int, image_url: str):
    raw_json_response = json.dumps(
        AUCTION.create_auction(
            item_name=name,
            description=description,
            auction_start=start,
            auction_end=end,
            starting_bid=starting_bid,
            image_path=image_url
        ),
        indent=2
    )
    print(
        highlight(
            raw_json_response,
            lexer=JsonLexer(),
            formatter=Terminal256Formatter()
        )
    )

@app.command()
def delete_auction(auction_id: int):
    raw_json_response = json.dumps(
        AUCTION.delete_auction(
            auction_id=auction_id
        ),
        indent=2
    )
    print(
        highlight(
            raw_json_response,
            lexer=JsonLexer(),
            formatter=Terminal256Formatter()
        )
    )


def main():
    SCHEDULER.start()
    app()

if __name__ == "__main__":
    main()