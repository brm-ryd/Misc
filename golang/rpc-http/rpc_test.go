package main

import (
	"testing"

	"rpc-http/client"
	"rpc-http/server"
)

func BenchmarkDialHTTP(b *testing.B) {
	b.ResetTimer()

	for i := 0; i < b.N; i++ {
		c := client.CreateClient()
		c.Close()
	}
}

func BenchmarkHelloWorldHandlerHTTP(b *testing.B) {
	b.ResetTimer()

	c := client.CreateClient()

	for i := 0; i < b.N; i++ {
		_ = client.PerformRequest(c)
	}

	c.Close()
}

func init() {
	// start the server
	go server.StartServer()
}
