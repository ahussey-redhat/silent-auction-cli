import datetime

class AuctionEntity:
    def __init__(self, item_name: str, description: str, auction_start: datetime, auction_end: datetime, starting_bid: int, image_path: str):
        self.item_name = item_name
        self.description = description
        self.auction_start = auction_start
        self.auction_end = auction_end
        self.starting_bid = starting_bid
        self.image_path = image_path
    def auction(self):
        return (
            self.item_name,
            self.description,
            self.auction_start,
            self.auction_end,
            self.starting_bid,
            self.image_path
        )
