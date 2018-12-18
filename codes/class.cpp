/**
 * 긴글을 주석으로 쓰고싶을 때는 이렇게 써주시면 좋아요
 * 협업을 할 때는 주석을 남겨서 별도 전달 없이도 소통이 가능하도록 해주는게 좋습니다
 */

#include <iostream>
using namespace std;


// 클래스 선언
class Circle {};	// Circle이란 이름의 클래스 선언


// 접근 지정자
class Circle {
	private:
		// 클래스 내의 멤버 함수만 접근 가능
	public:
		// 클래스 내외의 모든 함수에게 접근 허용
};


// 클래스 멤버
class Circle {
	private:
		int radius;	// 멤버 변수
	public:
		void getArea();	// 멤버 함수
};


// 클래스 상속
class Student : public Person {};


// 함수
void function_name ( parameters ) {
	// 함수몸체(실행할 코드 입력)
}


/***************************************************************/

// 클래스 구현부
void Circle::getArea(){
	return 3.14 * radius * radius;
}
// 함수의 리턴 타입 클래스 이름 범위 지정 연산자 멤버 함수명과 매개 변수


int main() {
	Circle donut;	// Ciecle 클래스의 객체 생성. 객체 이름은 donut
	donut.radius = 1; // radius는 접근 지정자 private에 속해있기 때문에 여기서 컴파일 에러 생김
}
