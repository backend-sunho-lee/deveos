from flask import Flask, request, make_response, jsonify, send_file
import io

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'


#: 하나의 함수, 여러 메소드 설정
@app.route('/tutorial/methods', methods=['GET', 'POST', 'PUT', 'DELETE'])
def tutorial6():
    if request.method == 'GET': return '조회를 하고 싶을 때는 GET을 써주세요'
    elif request.method == 'POST': return '새로운 데이터를 만들 때는 POST를 써주세요'
    elif request.method == 'PUT': return '수정을 할 때는 PUT을 써주세요'
    elif request.method == 'DELETE': return '삭제를 할 때는 DELETE를 써주세요'


'''
참고
http://flask.pocoo.org/docs/0.12/api/#incoming-request-data
'''

#: 동적 라우팅 파라미터
@app.route('/tutorial/parameters/string/<parameter1>/num/<int:parameter2>')
def tutorial1(parameter1, parameter2):
    '''
    :param parameter1: 데이터 타입을 정해주지 않으면 default로 string으로 처리된다.
    :param parameter2: 데이터 타입을 정해주면 해당 데이터 타입으로만 받을 수 있다.

    :return: 결과값을 json으로 HTTP 상태코드와 함께 출력해준다.
    '''
    return make_response(jsonify(parameter1=parameter1, parameter2=parameter2), 200)


#: 쿼리 스트링
@app.route('/tutorial/queryString')
def tutorial2():
    '''
    /tutorial?qw=something 같이 요청한다.
    쿼리스트링은 데이터타입이 string이기 때문에 int를 받으려면 int(qs)로 변환시켜주어야한다.
    '''
    # get()함수를 쓰는 이유: 만약 요청에 포함되지 않았을 때 None으로 들어오게하여 에러 처리를 보다 쉽게 할 수 있다.
    #query_string = request.args.get('qs', None)

    # 특정 파라미터가 아닌 입력된 모든 파라미터를 받고 싶은 경우
    query_string = request.args
    return make_response(jsonify(query_string), 200)


#: 폼 데이터 받기
@app.route('/tutorial/form', methods=['POST'])
def tutorial3():
    '''
    데이터는 POST, PUT 메소드를 사용하는 것을 추천합니다.
    '''
    form = request.form.get('form', None)
    return make_response(jsonify(form=form), 200)


#: 쿼리스트링과 폼 구분없이 데이터 받기
@app.route('/tutorial/data', methods=['POST'])
def tutorial4():
    '''
    values를 통해 쿼리스트링과 폼의 구분없이 데이터를 받을 수 있다.

    만약 쿼리스트링과 폼 동시에 데이터가 올 경우 쿼리스트링의 값을 받는다.
    getlist()로 받으면 어디서 들어오든, 동시에 들어오든 상관없이 배열로 받을 수 있다.
    '''
    data1 = request.values.get('data1', None)
    data2 = request.values.getlist('data2', None)
    return make_response(jsonify(data1=data1, data2=data2), 200)


if __name__ == '__main__':
    app.run()
