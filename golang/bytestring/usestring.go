package bytestring

import (
	"fmt"
	"io"
	"os"
	"strings"
)

// searching a string
func SearchString() {
	s := "howdy world"

	fmt.Println(strings.Contains(s, "howdy"))

	// returns true because s contains the letter a
	// would also match if it contained b or c
	fmt.Println(strings.ContainsAny(s, "abc"))

	fmt.Println(strings.HasPrefix(s, "howdy"))

	fmt.Println(strings.HasSuffix(s, "world"))
}

// modifies a string
func ModifyString() {
	s := "using string"

	// print [using string]
	fmt.Println(strings.Split(s, " "))

	// print "using string"
	fmt.Println(strings.Title(s))

	// leading white space is removed
	s = " using string "
	fmt.Println(strings.TrimSpace(s))
}

// create io.Reader interface with a string
func StringReader() {
	s := "using string\n"
	r := strings.NewReader(s)

	// prints s on Stdout
	io.Copy(os.Stdout, r)
}
