from flask import Flask, make_response, jsonify, request
import requests

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World!'


#: 연락처 생성
@app.route('/ex/addressbook', methods=['POST'])
def ex_emplace():
    newrow = {
        "first_name": request.values.get('first_name'),
        "last_name": request.values.get('last_name'),
        "phone": request.values.get('phone')
    }
    response = requests.post('http://fabius.ciceron.xyz/addressbook', data=newrow)
    row = response.json()
    return make_response(jsonify(response.json()), 200)


#: 연락처 목록 조회
@app.route('/ex/addressbook')
def find_list():
    response = requests.get('http://fabius.ciceron.xyz/addressbook')
    rows = response.json()
    return make_response(jsonify(rows), 200)


#: 연락처 조회
@app.route('/ex/addressbook/<int:id>', methods=['GET'])
def find_one(id):
    response = requests.get('http://fabius.ciceron.xyz/addressbook/{}'.format(id))
    row = response.json()
    return make_response(jsonify(row), 200)


#: 연락처 수정
@app.route('/addressbook/<int:id>', methods=['PUT'])
def modify(id):
    updaterow = {
        "first_name": request.values.get('first_name'),
        "last_name": request.values.get('last_name'),
        "phone": request.values.get('phone')
    }
    response = requests.put('http://fabius.ciceron.xyz/addressbook/{}'.format(id), data=updaterow)
    row = response.json()
    return make_response(jsonify(row), 200)


#: 연락처 삭제
@app.route('/addressbook/<int:id>', methods=['DELETE'])
def erase(id):
    response = requests.delete('http://fabius.ciceron.xyz/addressbook/{}'.format(id))
    row = response.json()
    return make_response(jsonify(row), 200)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
