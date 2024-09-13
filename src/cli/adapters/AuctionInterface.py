import cli.controllers.Auction

import typer
import json
from datetime import datetime

from pygments import highlight
from pygments.formatters.terminal256 import Terminal256Formatter
from pygments.lexers.data import JsonLexer


AUCTION = cli.controllers.Auction.Auction()

app = typer.Typer()

@app.command()
def list():
    raw_json_response = json.dumps(AUCTION.list_auctions(), indent=2)
    print(
        highlight(
            raw_json_response,
            lexer=JsonLexer(),
            formatter=Terminal256Formatter()
        )
    )

@app.command()
def create(name: str, description: str, start: datetime, end: datetime, starting_bid: int, image_url: str):
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
def delete(auction_id: int):
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

if __name__ == "__main__":
    app()