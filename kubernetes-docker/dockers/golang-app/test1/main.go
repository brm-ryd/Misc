package main

import (
	"fmt"
	"log"
	"net/http"
)

func handler (w http.ResponseWriter, r *http.Request) {
	fmt.Fprintln(w, "test,")
}

func main() {
	http.HandleFunc("/", handler)
	log.data(http.ListenAndServe(":8888", nil))
}