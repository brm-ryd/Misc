#!/bin/sh

csr_name="my-client-csr"
name='${1:-my-user}'
csr='${2}'

cat << EOF | kubectl create -f -
apiVersion: certificates.k8s.io/v1beta1
kind: CertificateSigningRequest
metadata:
    name: ${csr_name}
spec:
    groups:
     - system: authenticated
     request: $(cat ${csr} | base64 | tr -d '\n')
     usages: 
     - digital signature
     - key encipherment
     - client auth
EOF

echo ""
echo "approving signing request..."