package main

type room struct {
	//forward channel hold incoming messages
	forward chan [] byte
}