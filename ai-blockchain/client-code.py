import requests
import os
import datetime
import calendar
import time
import json
from web3 import Web3
import http.client

Tracking_ID = ""

url = 'https://www.googleapis.com/geolocation/v1/geolocate'
myobj = {'key': os.environ['GMAPS_API_KEY']}

conn = http.client.HTTPSConnection("kfs2.moibit.io")
moibit_url = 'https://kfs2.moibit.io/moibit/v0/'
moibit_header_obj = {
    'api_key': os.environ['MOIBIT_API_KEY'],
    'api_secret': os.environ['MOIBIT_API_SECRET'],
    'content-type': "application/json"
}

blockchain_url = 'https://kovan.infura.io/v3/' + \
    os.environ['WEB3_INFURA_PROJECT_ID']
abi = """[{"anonymous": false,"inputs": [{"indexed": false,"internalType": "address","name": "deviceID","type": "address"},{"indexed": false,"internalType": "string","name": "latestCID","type": "string"}],"name": "MappingUpdated","type": "event"},{"inputs": [{"internalType": "address","name": "deviceID","type": "address"},{"internalType": "string","name": "latestCID","type": "string"}],"name": "setLatestCID","outputs": [],"stateMutability": "nonpayable","type": "function"},{"inputs": [],"name": "getDeviceIDsLength","outputs": [{"internalType": "uint256","name": "","type": "uint256"}],"stateMutability": "view","type": "function"},{"inputs": [{"internalType": "uint256","name": "index","type": "uint256"}],"name": "getIDByIndex","outputs": [{"internalType": "address","name": "","type": "address"}],"stateMutability": "view","type": "function"},{"inputs": [{"internalType": "address","name": "deviceID","type": "address"}],"name": "getLatestCID","outputs": [{"internalType": "string","name": "latestCID","type": "string"}],"stateMutability": "view","type": "function"}]"""


def getGeoCordinates():
    """
    google servers map
    """

def updateLocationHistory():
    """
    wallet location history data
    """

def main():
    # fetch tracking from other functions tracking, wallet, etc
    # incomplete


if __name__ == "__main__":
    main()
