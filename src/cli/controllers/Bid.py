import cli.configuration.variables as app_variables

import requests
import logging
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

    #  bid_id: Optional[int] = None
    def __init__(self):
        self.backend_url = app_variables.BACKEND_BASE_URL
    def create_bid(self, auction_id: int, bid_amount: int):
        endpoint = f"api/v1/auctions/{auction_id}/bids"
        headers = {'Authorization': f'Bearer {app_variables.TOKEN["access_token"]}'}
        data = {
            "bid_amount": bid_amount
        }
        logging.debug(
            f"""
            Headers: {headers}
            Data: {data}
            """
        )
        r = requests.post(f"{self.backend_url}{endpoint}", json=data, headers=headers)
        if r.status_code == 200 or r.status_code == 201:
            return r.json()
        if r.status_code == 401:
            print("Not authorized. Please login.")
        if r.status_code == 404:
            print("No auctions available.")
    def get_bids_for_auction(self, auction_id):
        endpoint = f"api/v1/auctions/{auction_id}/bids"
        headers = {'Authorization': f'Bearer {app_variables.TOKEN["access_token"]}'}
        r = requests.get(f"{self.backend_url}{endpoint}", headers=headers)
        if r.status_code == 200:
            return r.json()
        if r.status_code == 401:
            print("Not authorized. Please login.")
        if r.status_code == 404:
            print("No auctions available.")
    def get_highest_bid_for_auction(self, auction_id):
        endpoint = f"api/v1/auctions/{auction_id}/bids/highest"
        headers = {'Authorization': f'Bearer {app_variables.TOKEN["access_token"]}'}
        r = requests.get(f"{self.backend_url}{endpoint}", headers=headers)
        if r.status_code == 200:
            return r.json()
        if r.status_code == 401:
            print("Not authorized. Please login.")
        if r.status_code == 404:
            print("No auctions available.")
    def get_highest_bids_for_all_auctions(self):
        endpoint = f"api/v1/auctions/bids/highest"
        headers = {'Authorization': f'Bearer {app_variables.TOKEN["access_token"]}'}
        r = requests.get(f"{self.backend_url}{endpoint}", headers=headers)
        if r.status_code == 200:
            return r.json()
        if r.status_code == 401:
            print("Not authorized. Please login.")
        if r.status_code == 404:
            print("No auctions available.")
