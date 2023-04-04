from subprocess import call

# Funkce pro vztvoření klíče, cert. requestu a certifikátu, použití openssl
def createcert(name):
    keydir = "certdir/keyes/"
    #name = "P000000000000000000001"
    keyend = ".key"

    keypath = keydir+name+keyend

    requestdir = "certdir/requests/"
    reqend = ".csr"
    requestpath = requestdir+name+reqend
    cn = "/CN="
    CNname = cn+name

    certdir = "certdir/certs/"
    certend = ".crt"
    certpath = certdir+name+certend

    call(["openssl", "ecparam", "-genkey", "-name" ,"secp192k1", "-out",keypath])

    call(["openssl", "req", "-new", "-sha1", "-key", keypath, "-nodes", "-out", requestpath, "-subj", CNname])

    call(["openssl", "x509", "-req", "-sha1", "-days", "730", "-in", requestpath, "-CA", "ca.crt", "-CAkey", "ca.key", "-CAcreateserial", "-out", certpath])