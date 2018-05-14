package client

import (
	"fmt"
	"log"
	"net/rpc"

	"rpc-http/contract"
)

const port = 1234

func CreateClient() *rpc.Client {
	client, err := rpc.DialHTTP("tcp", fmt.Sprintf("localhost:%v", port))
	if err != nil {
		log.Fatal("dialing:", err)
	}
	return client
}

func PerformRequest(c *rpc.Client) contract.HelloWorldResp {
	args := &contract.HelloWorldReq{Name: "World"}
	var reply contract.HelloWorldResp
	err := c.Call("HelloWorldHandler.HelloWorld", args, &reply)

	if err != nil {
		log.Fatal("error:", err)
	}

	return reply
}
