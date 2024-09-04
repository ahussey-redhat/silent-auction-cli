from datetime import datetime
from typing import Optional


class Bid:
    #
    # Bid Entity Class
    #
    # Endpoints
    # - Create Bid: Creates a new bid
    # - View Bid: View details about an existing bid
    # - Update Bid: Updates an existing bid
    # - Delete Bid: Deletes an existing bid
    #
    def __init__(self, auction_id: int, user_id: int, bid_time: datetime, bid_amount: int, bid_id: Optional[int] = None):
        self.bid_id = bid_id
        self.auction_id = auction_id
        self.user_id = user_id
        self.bid_time = bid_time
        self.bid_amount = bid_amount
    def create_bid(self):
        endpoint = "/api/v1/bids"
        method = 'POST'
        body = {
            "bid_id": self.bid_id,
            "auction_id": self.auction_id,
            "user_id": self.user_id,
            "bid_time": self.bid_time,
            "bid_amount": self.bid_amount
        }