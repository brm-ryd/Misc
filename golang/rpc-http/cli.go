package main

import (
	"fmt"

	"rpc-http/client"
	"rpc-http/server"
)

func main() {
	server.StartServer()

	c := client.CreateClient()
	defer c.Close()

	reply := client.PerformRequest(c)

	fmt.Println(reply.Message)
}
