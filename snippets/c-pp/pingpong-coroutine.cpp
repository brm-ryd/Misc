//implement using uC++
_Coroutine PingPong {
  const char *name;
  const unsigned int N;
  PingPong *part;

  void main() { //ping start umain, pong starter PingPong
    for (unsigned int i=0; i< N; i+= 1) {
      cout << name << endl;
      part -> cycle();
    }
  }
public:
  PingPong(const char *name, unsigned int N, PingPong &part=
      *(PingPong *)0): name(name), N(N), part(&part) {}
  void cycle() { resume(); }
  void partner( PingPong &part) { PingPong::part = &part; resume(); }
};

void uMain::main() {
  enum { N = 20 };
  PingPong ping("ping", N), pong("pong",N, ping);
  ping.partner(pong);
}
