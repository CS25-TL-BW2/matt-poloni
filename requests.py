import requests
from decouple import config

API_KEY = config('API_KEY')
BACKEND = config('BACKEND')

headers = { "Authorization": f"Token {API_KEY}" }

def check_json(response):
    try:
        return response.json()
    except ValueError:
        print("Error: Non-JSON response")
        print("Response returned:")
        print(response)
        return None


#==========================================
# Adventure Endpoints
#==========================================


def req_adv(endpoint):
    """ 
    Returns full URL for an adventure endpoint on backend server
    """
    return f"{BACKEND}/adv/{endpoint}"


#-----------------------------------------
# Player Status & Updates
#-----------------------------------------


def adv_init():
    """ 
    GET request to api/adv/init
    """
    endpoint = req_adv("init/")
    r = requests.get(endpoint, headers=headers)
    data = check_json(r)

    return data


def adv_status():
    """ 
    POST request to api/adv/status
    """
    endpoint = req_adv("status/")

    r = requests.post(endpoint, headers=headers)
    data = check_json(r)

    return data


def adv_change_name(name):
    """ 
    POST request to api/adv/change_name
    """
    endpoint = req_adv("change_name/")
    payload = { "name": name }

    r = requests.post(endpoint, headers=headers, json=payload)
    data = check_json(r)

    return data


def adv_pray():
    """ 
    POST request to api/adv/pray
    """
    endpoint = req_adv("pray/")

    r = requests.post(endpoint, headers=headers)
    data = check_json(r)

    return data


#-----------------------------------------
# Movement
#-----------------------------------------


def adv_move(direction, next_room_id=None):
    """ 
    POST request to api/adv/move
    """
    endpoint = req_adv("move/")
    payload = { "direction": direction }
    if next_room_id is not None:
        payload["next_room_id"] = str(next_room_id)
    
    r = requests.post(endpoint, headers=headers, json=payload)
    data = check_json(r)

    return data


def adv_fly(direction, next_room_id=None):
    """ 
    POST request to api/adv/fly
    """
    endpoint = req_adv("fly/")
    payload = { "direction": direction }
    if next_room_id is not None:
        payload["next_room_id"] = str(next_room_id)
    
    r = requests.post(endpoint, headers=headers, json=payload)
    data = check_json(r)

    return data


def adv_dash(direction, num_rooms, next_room_ids):
    """ 
    POST request to api/adv/dash
    """
    endpoint = req_adv("dash/")
    payload = {
        "direction": direction,
        "num_rooms": str(num_rooms),
        "next_room_ids": next_room_ids
    }

    r = requests.post(endpoint, headers=headers, json=payload)
    data = check_json(r)

    return data


def adv_warp():
    """ 
    POST request to api/adv/warp
    """
    endpoint = req_adv("warp/")

    r = requests.post(endpoint, headers=headers)
    data = check_json(r)

    return data


def adv_recall():
    """ 
    POST request to api/adv/recall
    """
    endpoint = req_adv("recall/")

    r = requests.post(endpoint, headers=headers)
    data = check_json(r)

    return data


#-----------------------------------------
# Item Actions
#-----------------------------------------


def adv_examine(name):
    """ 
    POST request to api/adv/examine
    """
    endpoint = req_adv("examine/")
    payload = { "name": name }

    r = requests.post(endpoint, headers=headers, json=payload)
    data = check_json(r)

    return data


def adv_take(name):
    """ 
    POST request to api/adv/take
    """
    endpoint = req_adv("take/")
    payload = { "name": name }

    r = requests.post(endpoint, headers=headers, json=payload)
    data = check_json(r)

    return data


def adv_drop(name):
    """ 
    POST request to api/adv/drop
    """
    endpoint = req_adv("drop/")
    payload = { "name": name }

    r = requests.post(endpoint, headers=headers, json=payload)
    data = check_json(r)

    return data


def adv_sell(name, confirm=False):
    """ 
    POST request to api/adv/sell
    """
    endpoint = req_adv("sell/")
    payload = { "name": name }
    if confirm:
        payload["confirm"] = "yes"

    r = requests.post(endpoint, headers=headers, json=payload)
    data = check_json(r)

    return data


def adv_transmogrify(name):
    """ 
    POST request to api/adv/transmogrify
    """
    endpoint = req_adv("transmogrify/")
    payload = { "name": name }
    
    r = requests.post(endpoint, headers=headers, json=payload)
    data = check_json(r)

    return data


def adv_wear(name):
    """ 
    POST request to api/adv/wear
    """
    endpoint = req_adv("wear/")
    payload = { "name": name }

    r = requests.post(endpoint, headers=headers, json=payload)
    data = check_json(r)

    return data


def adv_undress(name):
    """ 
    POST request to api/adv/undress
    """
    endpoint = req_adv("undress/")
    payload = { "name": name }

    r = requests.post(endpoint, headers=headers, json=payload)
    data = check_json(r)

    return data


def adv_carry(name):
    """ 
    POST request to api/adv/carry
    """
    endpoint = req_adv("carry/")
    payload = { "name": name }

    r = requests.post(endpoint, headers=headers, json=payload)
    data = check_json(r)

    return data


def adv_receive(name):
    """ 
    POST request to api/adv/receive
    """
    endpoint = req_adv("receive/")
    payload = { "name": name }

    r = requests.post(endpoint, headers=headers, json=payload)
    data = check_json(r)

    return data


#==========================================
# Blockchain Endpoints
#==========================================

def req_bc(endpoint):
    """ 
    Returns full URL for a blockchain endpoint on backend server
    """
    return f"{BACKEND}/bc/{endpoint}"

#------------------------------------------

def bc_mine(proof):
    """ 
    POST request to api/bc/mine
    """
    endpoint = req_bc("mine/")
    payload = { "proof": proof }

    r = requests.post(endpoint, headers=headers, json=payload)
    data = check_json(r)

    return data


def bc_last_proof():
    """ 
    GET request to api/bc/last_proof
    """
    endpoint = req_bc("last_proof/")

    r = requests.get(endpoint, headers=headers)
    data = check_json(r)

    return data


def bc_get_balance():
    """ 
    GET request to api/bc/get_balance
    """
    endpoint = req_bc("get_balance/")

    r = requests.get(endpoint, headers=headers)
    data = check_json(r)

    return data
