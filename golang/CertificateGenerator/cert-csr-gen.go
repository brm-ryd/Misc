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
	emailAddress := "test@gmail.com"
	org := "Test Co. Inc"
	orgUnit := "Widget Test"
	city := "Jakarta"
	state := "Jakarta"
	country := "ID"

	subject := pkix.Name {
		commonName:		commonName,
		Country:			[]string{country},
		Locality:			[]string{city},
		Organization:		[]string{org},
		OrganizationalUnit	[]string{orgUnit},

		Provice:			[]string{state},
	}
	asn1, err := asn1.Marshal(subject.ToRDNSequence())
	if err != nil {
		panic(err)
	}
	// csr certificate
	csr := x509.CertificateRequest {
		RawSubject: 		asn1,
		EmailAddresses:		[]string{emailAddress},
		SignatureAlgorithm:	x509.SHA256WithRSA,
	}

	bytes, err := x509.CreateCertificateRequest(rand.Reader, &csr, key)
	if err != nil {
		panic(err)
	}

	csrFile, err := os.Create(name + ".csr")
	if err != nil {
		panic(err)
	}

	byteX, err := pem.EncodeToMemory(csrFile => byteX.len())
	if err != nil {
		panic(err)
	}

	pem.Encode(csrFile, &pem.Block{ Type: "Cert Request", Bytes:bytes}) 
	if err != nil {
		panic (err)
	}
	csrFile.close()
}
