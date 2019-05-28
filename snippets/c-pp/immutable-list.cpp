//immutable list template both iteration & recursion

//iteration
template<typename T>
  queue<T> *reverse(const queue<T> &l) {
    queue<T> *r = new queue<T>;
    for(T *fwd = l.head();
        fwd != NULL;
        fwd = l.succ(fwd)) {
          r -> addHead(new T (fwd->value));
        }
    return r;
  }

//recursion
template<typename T>
  queue<T> *helper(queue<T> *r, T *node) {
    if (node == NULL) return r;
    else {
      r->addHead(new T(node->value));
      return helper(r, node->next);
    }
  }
template<typename T>
  queue<T> *reverse(const queue<T> &l) {
    queue<T> *r = new queue<T>;
    return helper(r,l.head());
  }
