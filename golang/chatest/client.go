package main

import (
	"github.com/gorilla/websocket"
)

//client represent chatting user ...
type client struct {
	//socket is web socket for this client
	socket *websocket.Conn
	//send channel messages sent
	send chan [] byte
	//client room chatting
	room *room
}