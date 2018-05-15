#include	<iostream>
#include	<optional>
#include	<algorithm>
#include	<functional>
#include	<iterator>
#include	<map>
#include	<vector>
#include	<string>

using	namespace	std;

template	<typename	T>
class	trie
{
			map<T,	trie>	tries;
      public:
          template	<typename	It>
          void	insert(It	it,	It	end_it)	{
            if	(it	==	end_it)	{	return;	}
            tries[*it].insert(next(it),	end_it);
          }

          template	<typename	C>
					void	insert(const	C	&container)	{
						insert(begin(container),	end(container));
					}

          void	insert(const	initializer_list<T>	&il)	{
            insert(begin(il),	end(il));
          }

          void	print(vector<T>	&v)	const	{
						if	(tries.empty())	{
										copy(begin(v),	end(v),
															ostream_iterator<T>{cout,	"	"});
										cout	<<	'n';
						}
						for	(const	auto	&p	:	tries)	{
										v.push_back(p.first);
										p.second.print(v);
										v.pop_back();
						}
					}

          void	print()	const	{
						vector<T>	v;
						print(v);
          }

          template	<typename	It>
					optional<reference_wrapper<const	trie>>
					subtrie(It	it,	It	end_it)	const	{
						if	(it	==	end_it)	{	return	ref(*this);	}
						auto	found	(tries.find(*it));
						if	(found	==	end(tries))	{	return	{};	}

						return	found->second.subtrie(next(it),	end_it);
          }

          template	<typename	C>
					auto	subtrie(const	C	&c)	{
						return	subtrie(begin(c),	end(c));
					}
};

int	main()
{
		trie<string>	t;

		t.insert({"hello",	"how",	"are",	"you", "doing"});
	  t.insert({"hola",	"i",	"am",	"fine",	"thanks"});
		t.insert({"what",	"are",	"you",	"doing", "now", "?"});
		t.insert({"i",	"am",	"playing",	"a",	"game"});

    cout	<<	"sentences:n";
		t.print();

    cout	<<	"npossible	suggestions	after	"hello":n";
		if	(auto	st	(t.subtrie(initializer_list<string>{"hello"}));
				st)	{
				st->get().print();
		}
}
