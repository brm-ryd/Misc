// calculates sum of all multiple of 3 and 5 < MAX value.
// https://projeceuler.net/problem=1

package main

import (
	"fmt"
)

const MAX = 100000

func main() {
	work := make(chan int, MAX)
	result := make(chan int)

	// create channel of multiples of 3 and 5
	// concurrently with goroutine
	go func(){
		for i:=1;i<MAX;i++ {
			if (i % 3) == 0 || (i % 5) == 0 {
				work <- i // push to work
			}
		}
		close(work)
	} ()


// concurrently sum up work and put result in channel result
go func() {
	r := 0
	for i:= range work {
		r=r+i
	}
	result <- r
} ()

// wait for result, then print
fmt.Println("total: ", <- result)
}
