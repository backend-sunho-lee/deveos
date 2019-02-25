import eospy.cleos
import requests
import json
from pprint import pprint


def get_table_rows():
    data = {
        "json": True,
        "code": "sunny.token",
        "scope": "sunny.token",
        "table": "accounts"
    }
    data = json.dumps(data)

    resp = requests.post("http://fabius.ciceron.xyz:8888/v1/chain/get_table_rows", data=data)
    return resp.json()


def eospy_get_table_rows():
    ce = eospy.cleos.Cleos(url="http://fabius.ciceron.xyz:8888")
    resp = ce.get_table(code="sunny.token", scope="sunny.token", table="accounts")
    return resp


def issue():
    ce = eospy.cleos.Cleos(url='http://fabius.ciceron.xyz:8888')

    payload = {
        'account': 'sunny.token',
        "name": "issue",
        "authorization": [{
                          "actor": "sunny.token",
                          "permission": "active",
                          }]
    }

    arguments = {
        "to": 'debbie',  # receiver
        "quantity": '1.0000 SPT'  # In EOS
    }

    data=ce.abi_json_to_bin(payload['account'],payload['name'],arguments)
    payload['data']=data['binargs']

    trx = {"actions": [payload]}

    key = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"
    resp = ce.push_transaction(trx, key, broadcast=True)
    return resp



def transfer():
    ce = eospy.cleos.Cleos(url='http://fabius.ciceron.xyz:8888')
    
    payload = {
        "account": "sunny.token",
        "name": "transfer",
        "authorization": [{
                          "actor": "sunny",
                          "permission": "active",
                          }]
    }
    
    arguments = {
        "from": "sunny",
        "to": "debbie",
        "quantity": '1.0000 SPT'
    }

    data=ce.abi_json_to_bin(payload['account'],payload['name'],arguments)
    payload['data']=data['binargs']

    trx = {"actions": [payload]}

    key = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"
    resp = ce.push_transaction(trx, key, broadcast=True)
    return resp


print('1--------------------------------------------------')
pprint(issue())
print('2--------------------------------------------------')
pprint(eospy_get_table_rows())
print('3--------------------------------------------------')
pprint(transfer())
print('4--------------------------------------------------')
pprint(get_table_rows())
print('--------------------------------------------------')
