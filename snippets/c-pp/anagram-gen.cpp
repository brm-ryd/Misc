/* Anagram implementation in CPP - pretty fast to do the job though still need some improvement
for optimization */

#include <iostream.h>
#include <string.h>
using namespace std;

class wrd
{
 private:
	int sz, cnt; //length inp words and num to display 
	string wstr;
	void rot(int); //shift word char rotate
	void tmplwrd(); 
 public:
	wrd(string); //constructor
	void anagram(int);
};

wrd::wrd(string instr): wstr(instr), cnt(0)
{
 sz = instr.length();
}

void wrd::anagram(int newsize)
{
 if(newsize==1)
	return;
 for(int j=0; j<newsize;j++) {
 	anagram(newsize - 1);
	if(newsize==2)
		tmplwrd();
	rot(newsize);
  }
}

//rotate left char to end
void wrd::rot(int newsize)
{
 int j;
 int position = sz - newsize;
 char tmp = wstr[position];
 for(j=position+1; j< sz;j++)
	wstr[j-1] = wstr[j];
 wstr[j-1] = tmp;
}

void wrd::tmplwrd()
{
 if(cnt  < 99)
	cout << " ";
 if(cnt < 9)
	cout << " ";
 cout << ++cnt << " ";
 cout << wstr << "    ";
 if(cnt % 6 == 0)
	cout << endl;
}

int main()
{
 string input;
 int len;
 cout << "enter word: ";
 cin >> input;
 len = input.length();
 wrd WORD(input);   //object from class above 'wrd'
 WORD.anagram(len); //anagram process
 return 0;
}
