from flask import Flask, make_response, jsonify, request
import json
import requests
import eospy.cleos

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World!'


@app.route('/get_table_rows', methods=['POST'])
def get_table_rows():
    data = {
        "json": True,
        "code": request.values.get('account'),
        "scope": request.values.get('scope'),
        "table": request.values.get('table')
    }
    data = json.dumps(data)

    response = requests.post("http://fabius.ciceron.xyz:8888/v1/chain/get_table_rows", data=data)
    resp = response.json()
    return make_response(jsonify(resp), 200)


cleos = eospy.cleos.Cleos(url='http://fabius.ciceron.xyz:8888')

@app.route('/get_table', methods=['POST'])
def get_table():
    account = request.values.get('account')
    scope = request.values.get('scope')
    table = request.values.get('table')

    resp = cleos.get_table(account, scope, table)
    return make_response(jsonify(resp), 200)


@app.route('/issue', methods=['POST'])
def issue():
    account = request.values.get('account')
    key = request.values.get('key')

    payload = {
        'account': account,
        'name': 'issue',
        'authorization': [{
            'actor': account,
            'permission': 'active'
        }]
    }
    arguments = {
        'to': request.values.get('to'),
        'quantity': request.values.get('quantity')
    }

    data = cleos.abi_json_to_bin(payload['account'], payload['name'], arguments)
    payload['data'] = data['binargs']
    trx = {'actions': [payload]}

    resp = cleos.push_transaction(trx, key, broadcast=True)
    return make_response(jsonify(resp), 200)


@app.route('/transfer', methods=['POST'])
def transfer():
    key = request.values.get('key')
    actor = request.values.get('from')

    payload = {
        'account': request.values.get('account'),
        'name': 'transfer',
        'authorization': [{
            'actor': actor,
            'permission': 'active'
        }]
    }
    arguments = {
        'from': actor,
        'to': request.values.get('to'),
        'quantity': request.values.get('quantity')
    }

    data = cleos.abi_json_to_bin(payload['account'], payload['name'], arguments)
    payload['data'] = data['binargs']
    trx = {'actions': [payload]}

    resp = cleos.push_transaction(trx, key, broadcast=True)
    return make_response(jsonify(resp), 200)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
