# Erase 액션 작성



##서버 접속 방법

1. 콘솔창 열기

   Windows: Ubuntu 실행 또는 Putty

   Mac: Terminal 실행

   

2. 로그인

   ssh deveos@fabius.ciceron.xyz

   비밀번호: deveos2018

   

3. 본인 폴더 이동

```shell
cd 본인폴더/contracts/addressbook
```





###Putty 사용하실 경우

![puttyì ëí ì´ë¯¸ì§ ê²ìê²°ê³¼](https://images.sftcdn.net/images/t_app-cover-l,f_auto/p/6a5919fa-96d1-11e6-b8e8-00163ec9f5fa/1811083446/putty-screenshot.jpg)

**Host Name** 입력하는 곳에 `fabius.ciceron.xyz` 입력 후 **Open** 버튼 누르기



```shell
login as:
```

와 같이 누구로 로그인할 것이냐는 문자가 뜨면



```shell
deveos
```

를 입력해주시고 엔터를 눌러주세요. 그 다음, 비밀번호 `deveos2018`을 입력해주시고 엔터를 눌러주시면 됩니다.







## Erase 코드 입력

```shell
vim addressbook.cpp
```

vim으로 addressbook.cpp 파일을 엽니다



```c++
[[eosio::action]] void erase(name key) {
    adr adrtable(_self, _code.value);
    auto existing = adrtable.find(key.value);
    adrtable.erase(existing);
}
```

이 코드를 `[[eosio::action]] void upsert() {}` 괄호가 끝나는 부분 }와 그 뒤에 있는 클래스가 끝나는 괄호 }; 사이에 입력해주세요.



```c++
EOSIO_DISPATCH( addressbook, (upsert)(erase) )
```

`(upsert)`만 입력되어 있을텐데, `(erase)` 도 추가해주세요. 새로운 액션을 추가했음을 명시해줍니다.





### 완성된 코드

```c++
#include <eosiolib/eosio.hpp>

using namespace eosio;
using namespace std;

class [[eosio::contract]] addressbook : public contract {
    private:
        struct [[eosio::table]] person {
            name key; //필드
            string first_name;
            string last_name;
            string phone;

            uint64_t primary_key() const { return key.value; }
        };  
        typedef multi_index<"people"_n, person> adr;

    public:
        using contract::contract;

        [[eosio::action]] void upsert (
                name key, 
                string first_name,
                string last_name,
                string phone ) { 
            adr adrtable(_code, _code.value);
            auto existing = adrtable.find(key.value);
    
            if (existing == adrtable.end()) {
                adrtable.emplace(key, [&](auto& row) {
                    row.key = key;
                    row.first_name = first_name;
                    row.last_name = last_name;
                    row.phone = phone;
                }); 
            } else {
                adrtable.modify(existing, key, [&](auto& row) {
                    row.key = key;
                    row.first_name = first_name;
                    row.last_name = last_name;
                    row.phone = phone;
                }); 
            }   
        }   

        [[eosio::action]] void erase (name key) {
            adr adrtable(_self, _code.value);
            auto existing = adrtable.find(key.value);
            adrtable.erase(existing);
        }   
};

EOSIO_DISPATCH( addressbook, (upsert)(erase) )
```



코드를 다 입력했다면, `esc` 키를 눌러주시고 `:wq` 를 입력 후 엔터를 쳐서 vim에서 나와주세요.





##Erase 액션 실행

```shell
cleos wallet open
```



```shell
cleos wallet unlock --password PW5K81jfmqEaRYAVm4NrQa1WggcWUhurZ57PhnFJk7fyJgqmjkywb
```



```shell
eosio-cpp -o addressbook.wasm addressbook.cpp --abigen
```

컴파일 해서 오류가 나타났다면, 오타나 괄호 등 틀린 부분이 있나 확인하고 수정해주세요.



```shell
cleos set contract sunny.adr ../addressbook/ -p sunny.adr@active
```



```shell
cleos get table sunny.adr sunny.adr people
```

```shell
{
  "rows": [{
      "key": "sunny",
      "first_name": "sunny",
      "last_name": "lee",
      "phone": "01033334444"
    }
  ],
  "more": false
}
```

현재 여러분 데이터가 위와 같이 저장되어 있을거에요.



```shell
cleos push action sunny.adr erase '["sunny"]' -p sunny@active
```

이제 여러분 데이터를 삭제하는 액션을 실행했습니다.

```shell
{
  "rows": [],
  "more": false
}
```

위에 저장되어 있던 데이터가 사라진 것을 확인하실 수 있습니다.

