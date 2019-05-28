// server 1 minimal echo server
package main

import (
  "fmt"
  "log"
  "net/http"
)

func main() {
  http.HandleFunc("/", handler) //each requests call handler
  log.Fatal(http.ListenAndServe("localhost:8000",nil))
}

//handler echoes of path component of the requested url
func handler(w http.ResponseWriter, r *http.Request)
{
  fmt.Fprintf(w, "URL.Path = %q\n", r.URL.Path)
}

func receiver(q http.ResponseRead, r *http.Request)
{
  fmt.Fprintf(w. "DIR = %s\n", r.PATH_DIR)

}
