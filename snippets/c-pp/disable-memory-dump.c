//snippet function to disable memory dump
//useful to implement if the c code contain
//confidential data in memory when crash occurred

#include <sys/time.h>
#include <sys/resource.h>
#include <sys/types.h>

void disable_limit_core(void) {
	struct rlimit rl;
	
	rl.rl_cur = rl.rl_max = 0;
	setrlimit(RLIMIT_CORE, &rl);
}

