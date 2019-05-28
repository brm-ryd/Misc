//implement using uC++
#include <iostream>
using namespace std;
_Coroutine Fibonacci { // uBaseCoroutine
  int fn;              // used for communication
  void main () {       // distinquished member
      int fn1, fn2;    //retained between resumes
      fn = 0;  fn1 = fn;
      suspend();  //return to last resume
      fn = 1; fn2 = fn1; fn1 = fn;
      suspend();  //return to last resume
      for (;;) {
        fn = fn1+ fn2; fn2 = fn1; fn1=fn;
        suspend(); //return to last resume
      }
  }
public:
  int next() {
    resume();  //transfer to last suspend
    return fn;
  }
};

void uMain::main() { //argc, argv class variable
  Fibonacci f1, f2;{
  for (int i = 1; i<= 10; i+=1) {
    cout << f1.next() << " " << f2.next() << endl;
  }
  uRetCode = 3; //return code optional
}
