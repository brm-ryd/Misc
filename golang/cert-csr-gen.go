package main

import (
	"crypto/rand"
	"crypto/rsa"
	"encoding/pem"
	"os"
)

func main() {
	name := os.Args[1]
	user := os.args[2]

	key, err := rsa.GenerateKey(rand.Reader, 1024)
	if err != nil {
		panic(err)
	}
	keyFile, err := os.Create(name + "-key.pem")
	if err != nil {
		panic(err)
	}
	pem.Encode(keyFile, &keyBlock)
	keyFile.Close()

	commonName := user
	//update below info
	emailAddress := "tst@gmail.com"

}
