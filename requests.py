import requests
from decouple import config

API_KEY = config('API_KEY')
BACKEND = config('BACKEND')

headers = {
  "Authorization": f"Token {API_KEY}"
}

#==========================================
# Adventure Endpoints
#==========================================

def req_adv(endpoint):
    """ 
    Returns full URL for an adventure endpoint on backend server
    """
    return f"{BACKEND}/adv/{endpoint}"

#-----------------------------------------

def init():
    """ 
    GET request to api/adv/init
    """
    endpoint = req_adv("init/")
    r = requests.get(endpoint, headers=headers)

def move(payload):
    """ 
    POST request to api/adv/move
    """
    endpoint = req_adv("move/")
    r = requests.post(endpoint, headers=headers, json=payload)

def take(payload):
    """ 
    POST request to api/adv/take
    """
    endpoint = req_adv("take/")
    r = requests.post(endpoint, headers=headers, json=payload)

def drop(payload):
    """ 
    POST request to api/adv/drop
    """
    endpoint = req_adv("drop/")
    r = requests.post(endpoint, headers=headers, json=payload)

def sell(payload):
    """ 
    POST request to api/adv/sell
    """
    endpoint = req_adv("sell/")
    r = requests.post(endpoint, headers=headers, json=payload)

def status(payload):
    """ 
    POST request to api/adv/status
    """
    endpoint = req_adv("status/")
    r = requests.post(endpoint, headers=headers, json=payload)

def examine(payload):
    """ 
    POST request to api/adv/examine
    """
    endpoint = req_adv("examine/")
    r = requests.post(endpoint, headers=headers, json=payload)

def wear(payload):
    """ 
    POST request to api/adv/wear
    """
    endpoint = req_adv("wear/")
    r = requests.post(endpoint, headers=headers, json=payload)

def undress(payload):
    """ 
    POST request to api/adv/undress
    """
    endpoint = req_adv("undress/")
    r = requests.post(endpoint, headers=headers, json=payload)

def change_name(payload):
    """ 
    POST request to api/adv/change_name
    """
    endpoint = req_adv("change_name/")
    r = requests.post(endpoint, headers=headers, json=payload)

def pray(payload):
    """ 
    POST request to api/adv/pray
    """
    endpoint = req_adv("pray/")
    r = requests.post(endpoint, headers=headers, json=payload)

def fly(payload):
    """ 
    POST request to api/adv/fly
    """
    endpoint = req_adv("fly/")
    r = requests.post(endpoint, headers=headers, json=payload)

def dash(payload):
    """ 
    POST request to api/adv/dash
    """
    endpoint = req_adv("dash/")
    r = requests.post(endpoint, headers=headers, json=payload)

def carry(payload):
    """ 
    POST request to api/adv/carry
    """
    endpoint = req_adv("carry/")
    r = requests.post(endpoint, headers=headers, json=payload)

def receive(payload):
    """ 
    POST request to api/adv/receive
    """
    endpoint = req_adv("receive/")
    r = requests.post(endpoint, headers=headers, json=payload)

def warp(payload):
    """ 
    POST request to api/adv/warp
    """
    endpoint = req_adv("warp/")
    r = requests.post(endpoint, headers=headers, json=payload)

def recall(payload):
    """ 
    POST request to api/adv/recall
    """
    endpoint = req_adv("recall/")
    r = requests.post(endpoint, headers=headers, json=payload)

def transmogrify(payload):
    """ 
    POST request to api/adv/transmogrify
    """
    endpoint = req_adv("transmogrify/")
    r = requests.post(endpoint, headers=headers, json=payload)

#==========================================
# Blockchain Endpoints
#==========================================

def req_bc(endpoint):
    """ 
    Returns full URL for a blockchain endpoint on backend server
    """
    return f"{BACKEND}/bc/{endpoint}"

#------------------------------------------

def mine(payload):
    """ 
    POST request to api/bc/mine
    """
    endpoint = req_bc("mine/")
    r = requests.post(endpoint, headers=headers, json=payload)

def last_proof():
    """ 
    GET request to api/bc/last_proof
    """
    endpoint = req_bc("last_proof/")
    r = requests.get(endpoint, headers=headers)

def get_balance():
    """ 
    GET request to api/bc/get_balance
    """
    endpoint = req_bc("get_balance/")
    r = requests.get(endpoint, headers=headers)
