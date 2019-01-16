from flask import Flask, request, make_response, jsonify

app = Flask(__name__)


# 전체 사용자 조회
@app.route('/users', methods=['GET'])
def get_users():
	return make_response(jsonify(), 200)

# 사용자 추가
# 사용자 수정
# 사용자 삭제
# 특정 사용자 조회
