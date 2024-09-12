import cli.configuration.variables as app_variables

from datetime import datetime
import logging
import requests
import json

class Auction:
    #
    # Auction Entity Class
    #
    # Endpoints
    # - Create Auction: Creates a new auction
    # - View Auction: View details about an existing auction
    # - Update Auction: Updates an existing auction
    # - Delete Auction: Deletes an existing auction
    #
    def __init__(self):
        self.backend_url = app_variables.BACKEND_BASE_URL

    def create_auction(self, item_name: str, description: str, auction_start: datetime, auction_end: datetime, starting_bid: int, image_path: str):
        endpoint = "api/v1/auctions"
        headers = {'Authorization': f'Bearer {app_variables.TOKEN["access_token"]}'}
        data = {
            "item_name": item_name,
            "description": description,
            "auction_start": auction_start.strftime("%Y-%m-%dT%H:%M:%S"),
            "auction_end": auction_end.strftime("%Y-%m-%dT%H:%M:%S"),
            "starting_bid": starting_bid,
            "image_path": image_path
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

    def delete_auction(self, auction_id: int):
        endpoint = "api/v1/auctions/" + str(auction_id)
        headers = {'Authorization': f'Bearer {app_variables.TOKEN["access_token"]}'}
        r = requests.delete(f"{self.backend_url}{endpoint}", headers=headers)
        if r.status_code == 200 or r.status_code == 201:
            return r.json()
        if r.status_code == 401:
            print("Not authorized. Please login.")
        if r.status_code == 404:
            print("No auctions available.")

    def list_auctions(self):
        endpoint = "api/v1/auctions"
        headers = {'Authorization': f'Bearer {app_variables.TOKEN["access_token"]}'}
        r = requests.get(f"{self.backend_url}{endpoint}", headers=headers)
        if r.status_code == 200:
            return r.json()
        if r.status_code == 401:
            print("Not authorized. Please login.")
        if r.status_code == 404:
            print("No auctions available.")
