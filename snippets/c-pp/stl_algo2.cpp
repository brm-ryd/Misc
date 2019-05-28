#include <iterator>
#include <iostream>
#include <algorithm>
#include <forward_list>
using namespace std;

int main () {
  forward_list<int> lst1 = {10,20,10,45,45,50,25};
  forward_list<int> lst2 = {20,35,27,15,100,85,12,15};

  cout << "nfirst list before sorting ..." << endl;
  copy(lst1.begin(), lst1.end(), ostream_iterator<int>(cout, "t"));
  count << endl;

  cout << "nsecond list before sorting ..." << endl;
  copy(lst2.begin(), lst2.end(), ostream_iterator<int>(cout, "t"));
  count << endl;

  lst1.sort();
  lst2.sort();

  cout << "nfirst list after sorting ..." << endl;
  copy(lst1.begin(), lst1.end(), ostream_iterator<int>(cout, "t"));
  cout << endl;

  cout << "nsecond list after sorting ..." << endl;
  copy(lst2.begin(), lst2.end(), ostream_iterator<int>(cout, "t"));
  cout << endl;

  lst1.merge(lst2);

  cout << "nmerged list ..." << endl;
  copy(lst1.begin(), lst1.end(), ostream_iterator<int>(cout, "t"));

  cout << "nmerged list after remove duplicates ..." << endl;
  lst1.unique();
  copy(lst1.begin(), lst1.end(), ostream_iterator<int>(cout, "t"));

  return 0;

}
