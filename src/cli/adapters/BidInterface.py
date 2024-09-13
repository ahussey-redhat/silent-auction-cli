import cli.controllers.Bid

import typer
import json

from pygments import highlight
from pygments.formatters.terminal256 import Terminal256Formatter
from pygments.lexers.data import JsonLexer


BID = cli.controllers.Bid.Bid()

app = typer.Typer()

@app.command()
def list_for_auction(auction_id: int):
    raw_json_response = json.dumps(BID.get_bids_for_auction(auction_id), indent=2)
    print(
        highlight(
            raw_json_response,
            lexer=JsonLexer(),
            formatter=Terminal256Formatter()
        )
    )

@app.command()
def list_highest_for_auction(auction_id: int):
    raw_json_response = json.dumps(BID.get_highest_bid_for_auction(auction_id), indent=2)
    print(
        highlight(
            raw_json_response,
            lexer=JsonLexer(),
            formatter=Terminal256Formatter()
        )
    )

@app.command()
def list_highest_for_all_auctions():
    raw_json_response = json.dumps(BID.get_highest_bids_for_all_auctions(), indent=2)
    print(
        highlight(
            raw_json_response,
            lexer=JsonLexer(),
            formatter=Terminal256Formatter()
        )
    )

@app.command()
def place(auction_id: int, amount: int):
    raw_json_response = json.dumps(
        BID.create_bid(
            auction_id=auction_id,
            bid_amount=amount
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

if __name__ == "__main__":
    app()