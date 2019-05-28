int front = 0, back = 0;
int elements[10];
uSemaphore e1(1), full(0), e2(1), empty(0);
int fullc = 0, emptyc = 10;

_Task Producer {
  void main() {
    for (;;) {
      //producing an element
      e2.p(); //simulate general p
      emptyc -= 1;
      if (emptyc < 0) {
        e2.V();
        empty.P();
      }
      else {
        e2.V();
      }
      // queue element
      e1.P(); //simulate general v
      if (fullc < 0) {
        full.V();
      }
      fullc += 1;
      e1.V();
    }
    //producing stopping val
  }
};

_Task Consumer {
  void main() {
    for(;;) {
      e1.P(); //simulate general p
      fullc -= 1;
      if(fullc < 0) {
        e1.V();
        full.P();
      }
      else{
        e1.V();
      }
      // remove queue element
      e2.P(); //simulate general v
      if (emptyc < 0) {
        emptyc.V();
      }
      emptyc += 1;
      e2.V();

    if (stopping value ?) break;
      //will consume element
    }
  }
};
