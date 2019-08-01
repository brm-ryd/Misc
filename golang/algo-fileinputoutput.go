package main

import (
	"fmt"
	"io/ioutil"
	"log"
)

func main() {
	f := "/tmp/log.txt"
	//create file & assign permission
	err := ioutil.WriteFile(f, []byte("foobar barfoo\n"), 0644)
	if err != nil { // err is == nil when call sucess
		//fatal is like print() followed by call os.Exit(1)
		log.fatal(err)
	}
	v, err := ioutil.ReadFile(f)
	if err != nil { //err is == nil when call is successful, which will be
		log.Fatal(err)
	}

	fmt.Println("filename is: ", f)
	fmt.Println("filedata is: ", string(v))
	f = "/tmp/nosuchfile.txt"
	v, err = ioutil.ReadFile(f) // read from file (will fail!!!)
	if err != nil {             //err will be != nil since no such file to read
		log.Fatal(err) //since file does not exist, error condition occurs
	}
}
