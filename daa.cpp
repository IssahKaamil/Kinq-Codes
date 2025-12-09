#include <iostream>

using namespace std;

void swap(int &a, int &b) {
  int temp = a;
  a = b;
  b = temp;
}

int main() {
  int a, b, t;
  int Time = 0;

  cout << "Input a, b: ";
  cin >> a >> b;

  while (a > b) {
    swap(a, b);
    Time += 3;
  }

  cout << "Time: " << Time << endl;
  cout << "a: " << a << ", b: " << b << endl;

  return 0;
}