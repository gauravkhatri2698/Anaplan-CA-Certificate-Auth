from base64 import b64encode
import os
from OpenSSL import crypto
import requests
import json

certfile = "server.txt"
keyfile = "private key.key"

"""
docstring
"""

st_cert=open(certfile, 'rt').read()
cert=crypto.load_certificate(crypto.FILETYPE_PEM, st_cert)

st_key=open(keyfile, 'rt').read()
key=crypto.load_privatekey(crypto.FILETYPE_PEM, st_key)

pem = crypto.dump_certificate(crypto.FILETYPE_TEXT, cert)
# print (pem)
random_str = os.urandom(100)
signed_str = crypto.sign(key, random_str, "sha512")

auth_headers = "'authorization': 'CACertificate %s'" % (st_cert.replace("\n", "").replace("-----BEGIN CERTIFICATE-----", "").replace("-----END CERTIFICATE-----", ""))
# print(auth_headers, '\n')
encodedstr = b64encode(random_str)
signedstr = b64encode(signed_str)
# print("{")
# print("   'encodedData': %s " %encodedstr.decode("ascii") )
# print("   'encodedSignedData': %s" % signedstr.decode("ascii") )
# print("}")

public_cert = st_cert.replace("\n", "").replace("-----BEGIN CERTIFICATE-----", "").replace("-----END CERTIFICATE-----", "")

getHeaders = {"Authorization":"CACertificate " + public_cert, "Content-Type": "application/json"}

print(getHeaders)

body_encoded_strings = '{' + '\r\n' + '"encodedData"' + ' : ' + '"' + encodedstr.decode("utf-8") + '"' + ',' + '\r\n' + \
'"encodedSignedData"' + ' : ' + '"' + signedstr.decode("utf-8") + '"' + '\r\n' + '}'

print(body_encoded_strings)

#Make a POST request to generate a token.
getTokenJson = requests.post('https://auth.anaplan.com/token/authenticate',
	headers=getHeaders,
	data = json.dumps(body_encoded_strings))

print(getTokenJson.json())