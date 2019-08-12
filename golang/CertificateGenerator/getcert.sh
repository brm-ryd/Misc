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
kubectl certificate approve ${csr_name}

echo ""
echo "downloading certificate..."
kubectl get csr ${csr_name} -o jsonpath='{.status.certificate}' \
    | base64 --decode > $(basename ${csr} .csr).crt

echo ""
echo "cleaning ..."
kubectl delete csr ${csr_name}

echo ""
echo "add these 'users' list in kubeconfig file"
echo "- name: ${name}"
echo "  user: "
echo "  client-certificate: ${PWD}/${basename ${csr} .csr).crt"
echo " 
 client-key: ${PWD}/$(basename ${csr} .csr)-key.pem"
echo ""
echo "add role binding for this user"