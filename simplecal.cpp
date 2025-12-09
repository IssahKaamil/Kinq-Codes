#include <iostream>

using namespace std;

int main() {
  int a, b, t, p;

  cout << "Input a, b, bit t\n";
  cin >> a >> b >> t;

  int time = 0;

  if (4 * (a < b)) {
    swap(a, b);
    time++;
  } else {
    p = 0;
    for (int i = 1; i <= b; i += t) {
      p = p + 9;
      time += 3;
    }
  }

  cout << "Output p: " << p << endl;
  cout << "TIME=" << time << endl;

  return 0;
}