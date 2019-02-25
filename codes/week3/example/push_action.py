import eospy.cleos
import os
from pprint import pprint

# 연결할 노드의 HOST 입력
# cleos는 블록체인과 통신하는 도구(cli). Cleos 클래스의 객체를 만들어 코드에서 활용/실행한다. 클래스의 멤버(API실행하는 함수) 사용하는 것
ce = eospy.cleos.Cleos(url='http://fabius.ciceron.xyz:8888')

# 실행할 액션과 계정 입력
payload = {
    "account": "sunny.token",
    "name": "transfer",
    "authorization": [{
                      "actor": "sunny",
                      "permission": "active",
    }]
}

# 액션의 매개변수 입력. 파이썬의 딕셔너리 데이터 타입 사용, JSON 형식
arguments = {
    "from": "sunny",  # sender
    "to": "debbie",  # receiver
    "quantity": '1.0000 SPT'  # In EOS
}


#Converting payload to binary
# https://developers.eos.io/eosio-nodeos/reference#abi_json_to_bin
# EOSIO RPC API 중 abi_json_to_bin 호출하여 블록체인에 보낼 수 있는 형식인 바이너리로 변환한 값을 응답한다
data=ce.abi_json_to_bin(payload['account'],payload['name'],arguments)

#Inserting payload binary form as "data" field in original payload
# 바이너리로 변환된 값을 payload에 추가한다
payload['data']=data['binargs']

#final transaction formed
trx = {"actions": [payload]}
print('---------------------- trx -----------------------')
pprint(trx)
print('--------------------------------------------------')


# 계정의 private key를 입력한다
key = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"

# cleos.py과 함께 확인
resp = ce.push_transaction(trx, key, broadcast=True)


print('-------------- push action result ----------------')
pprint(resp)
print('--------------------------------------------------')
