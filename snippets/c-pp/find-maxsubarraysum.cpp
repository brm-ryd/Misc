#include <iostream>
using namespace std;

//finding maximum-sum subarray

int i = 0, sum = 0;
for (int k = 0; k < n; k++) {
  sum = max(array[k], sum+array[k]);
  i = max(i, sum);
}
cout << i << "\n";
