# Python 기초 문법 

안녕하세요, [DEVEOS](https://deveos.org/)의 써니입니다☀️



오늘은 Python 기초 문법에 대해서 알려드릴게요. 수업시간에 필요한 부분만 다룰 예정이라, 더 깊고 제대로 파이썬을 해보고 싶으신 분들을 위해 책도 마지막에 추천드릴게요.





##Python IDLE

파이썬 설치시 함께 제공되는 **Python IDLE** 을 사용해서 코딩을 해보도록 하겠습니다.

IDEL은 Integrated Development and Learning Environment의 약자로 파이썬 통합 개발 환경을 제공하는 도구입니다.



Mac은 Terminal, Windows는 Powershell을 실행해주세요.

```shell
python
```

위 명령어만 입력하고 엔터를 누르면 아래와 같이 IDLE 쉘 창이 실행됩니다.

```shell
Python 2.7.15 (default, Oct 27 2018, 21:55:34) 
[GCC 4.2.1 Compatible Apple LLVM 10.0.0 (clang-1000.10.44.2)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> 
```



이 창에서 나가려면 `quit()` 를 입력해주시면 나가실 수 있어요.

지금 나가지 마시고~ 이따가 다 끝나고 종료할 때 입력해주시면 됩니다.





## 주석

주석은 메모처럼 사용하는 거라고 말씀드렸었는데요. 주석은 보통 한줄 주석과 여러줄 주석이 있습니다.



- 여러줄 주석

```python
"""
여러줄 주석은 이렇게
입력해주시면 됩니다
"""
```



- 한줄 주석

```python
# 한줄 주석
```





## 자료형

파이썬에는 다양한 자료형들이 있습니다.



### 숫자

1, 2, -1, -2, 0, 12.45, -56, 7 과 같이 정수형, 음수형, 0, 소수점 등이 있습니다.



### 문자열

파이썬은 문자열을 입력하는 다양한 방법이 있습니다.



```python
'따옴표 하나'
''따옴표 두개씩''
'''따옴표 세개씩'''
"쌍따옴표 하나"
""쌍따옴표 두개씩""
"""쌍따옴표 세개씩"""
```

이렇게 다양한 방법이 있는 이유는 문자열 안에 입력한 따옴표와 구분짓기 위해서입니다.



```python
'She said "Hello" to me.'
""She said "Hello" to me.""
```

이런식으로 입력했을 때, 파이썬은 `"Hello"` 를 문자열 변수로 인식하는게 아니라 문자열에 포함된 문자라고 인식합니다.



### 리스트(list)

한국어로는 '배열'이라고 합니다.



```python
[1, 2, 3]
["월", "화", "수"]
```

`[]` 괄호를 사용하여 리스트를 나타냅니다.

리스트는 입력 순서가 고정됩니다. 이 입력 순서로 배열 내용을 검색하거나 찾기도 합니다.



### 딕셔너리(Dictionary)

Key와 Value의 한 쌍으로 대응관계를 나타내는 자료형입니다.



```python
{"Key": "Value"}
{1: "사과", "숫자": 2}
```

`,` 쉼표로 여러개를 나열하며, Value에는 어떤 자료형이 들어가도 상관없습니다.

딕셔너리는 입력 순서가 고정되지 않습니다.





### 변수 선언

> Python IDLE에 입력해보세요

```python
a = 1
b = "Thank you"
c = [1, 2, 3]
d = {'name': 'sunny', 'phone': 20190125}
```

파이썬은 C++과 다르게 변수를 선언할 때 데이터 타입을 입력하지 않습니다. 값에 따라 변수의 데이터 타입이 자동으로 설정됩니다.



```python
>>> a
1

>>> b
'Thank you'

>>> c
[1, 2, 3]

>>> d
{'phone': 20190125, 'name': 'sunny'}
```

위의 코드를 Python IDLE에 입력하고 a, b, c, d를 차례대로 입력하면 입력했던 값들이 출력되는 것을 확인할 수 있습니다.





## 함수

```python
def 함수이름 (매개변수):
    # 함수 몸체
```

파이썬은 괄호를 사용하지 않고, 들여쓰기로 구분을 합니다. 들여쓰기를 인덴트라고 합니다.

그래서 들여쓰기로 지역을 구분하기 때문에 잘못되어 있으면 에러가 나타나므로 주의하셔야 합니다.



####Hello, World!

새로운 프로그래밍 언어를 시작하면 Hello World! 실습부터 해야겠죠?



```python
def hi(name):
    return "Hello, " + name
```

hi 함수를 선언해줍니다.



```python
>>> print(hi("sunny"))
Hello, sunny
```

hi 함수에 name 매개변수의 값으로 sunny를 넣어주고 print 함수로 출력하면 `Hello, sunny` 가 출력되는 것을 확인하실 수 있습니다.





## if 조건문

조건문은 조건의 참/거짓(True/False)에 따라 달라지는 계산이나 상황을 수행하는 프로그래밍 문법입니다.

```python
if 조건식:
    # 조건이 참(True)인 경우
else:
    # 조건이 거짓(False)인 경우
```



방금 작성한 hi 함수에 조건문을 적용해보도록 하겠습니다.

```python
def hi(name):
    if name == "sunny":
        return "Hello, " + name
    else:
        return "Nice to meet you!"
```

'name이 sunny인가요?'을 조건식으로 넣었습니다.



```python
>>> print(hi("sunny"))
Hello, sunny
>>> print(hi("debbie"))
Nice to meet you!
```

만약 name이 sunny가 맞다면 True이므로 "Hello, sunny"가 출력되고

name이 sunny가 아니라면 False이므로 else로 넘어가서 "Nice to meet you"가 출력됩니다.





---

여기까지 수업에서 활용되는 Python 문법을 다뤄봤구요. 더 자세히 더 제대로 파이썬을 사용하고 싶으신 분들을 위해 [점프 투 파이썬](https://wikidocs.net/book/1) 이란 책을 추천드리겠습니다. 파이썬의 배경부터 필요한 지식들을 잘 알려준 책이고, 길지 않아서 맘만 먹으면 일주일도 안걸려서 다 하실 수 있을겁니다.

무료로 제공되니 'https://wikidocs.net/book/1' 링크로 들어가셔서 보셔도 됩니다.

 

![ì í í¬ íì´ì¬ì ëí ì´ë¯¸ì§ ê²ìê²°ê³¼](http://image.yes24.com/momo/TopCate1232/MidCate001/123103781.jpg)



