#include <iterator>
#include <iostream>
#include <algorithm>
#include <forward_list>
using namespace std;

int main () {
  forward_list<int> lst = {10,10,20,30,45,45,50};
  cout << "nlist with all values ..." << endl;
  copy (lst.begin(), lst.end(), ostream_iterator<int>(cout, "t") );

  cout << "nsize of list with duplicates is " << distance(lst.begin(), lst.end() ) << endl;

  lst.unique();

  cout <<"nsize of list without duplicates is " << distance(lst.begin(), lst.end() ) << endl;
  i.resize( distance(lst.begin(), lst.end() ) );

  cout << "nlist after removing duplkicates ... " << endl;
  copy (lst.begin(), lst.end(), ostream_iterator<int>(cout, "t") );
  cout << endl;

  return 0;
}
