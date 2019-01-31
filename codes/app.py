from flask import Flask, make_response, jsonify, request

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello World!'


rows = []


#: 연락처 생성
@app.route('/addressbook', methods=['POST'])
def emplace():
    newrow = {
        "id": len(rows) + 1,
        "first_name": request.values.get('first_name'),
        "last_name": request.values.get('last_name'),
        "phone": request.values.get('phone')
    }
    rows.append(newrow)
    return make_response(jsonify(newrow), 200)


#: 연락처 목록 조회
@app.route('/addressbook')
def find_list():
    return make_response(jsonify(adrs=rows), 200)


#: 연락처 조회
@app.route('/addressbook/<int:id>', methods=['GET'])
def find_one(id):
    row = [r for r in rows if r['id'] == id]
    if not row:
        row = {
            "message": '존재하지 않는 사용자입니다'
        }
    else:
        row = row[0]
    
    return make_response(jsonify(row), 200)


#: 연락처 수정
@app.route('/addressbook/<int:id>', methods=['PUT'])
def modify(id):
    row = [r for r in rows if r['id'] == id]
    if not row:
        row = {
            "message": '존재하지 않는 사용자입니다'
        }
    else:
        row = row[0]

    row['first_name'] = request.values.get('first_name')
    row['last_name'] = request.values.get('last_name')
    row['phone'] = request.values.get('phone')

    return make_response(jsonify(row), 200)


#: 연락처 삭제
@app.route('/addressbook/<int:id>', methods=['DELETE'])
def erase(id):
    del rows[id-1]
    return make_response(jsonify(id=id), 200)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
