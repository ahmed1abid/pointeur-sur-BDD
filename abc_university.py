from flask import Flask, request
from flask_restful import Resource, Api 
from flask_jsonpify import jsonify
import rsa
import sys
sys.path.append('../')
from Issuer import Issuer 
import json
import sqlite3

conn = sqlite3.connect("GlobalVs.db")
c = conn.cursor()

query = """INSERT INTO GlobalVs VALUES ( '{}', '{}', '{}') ;""".format('ABC University', 'http://localhost:8080/', 'transcript')
print(query)
try:
	c.execute(query)
	conn.commit()
except:
	pass

app = Flask(__name__)

database = {121001: {"first_name": "Alice", "last_name": "Garcia", "degree":"Btech","year":2014,"status":"graduated"},
			121002: {"first_name": "Bob", "last_name": "Marley", "degree":"Phd", "year":2015,"status":"graduated"}}


abc_univ = Issuer(name='ABC University', schema='schemas/transcript.yaml', cert_name = 'transcript', db=database)

@app.route("/")
def hello():
	with open("servers/company.html", 'r') as f:
		return f.read().format("ABC University", "<p>Pass your courses :)</p>", "8080")


@app.route("/pkey")
def get_pkey():
	return jsonify({"pkey":abc_univ.keypair[0].save_pkcs1()})

@app.route("/cert_name")
def get_cert_name():
	return jsonify({"cert_name":"transcript"})

@app.route("/cert_schema")
def get_schema():
	return jsonify(abc_univ.schema)

@app.route("/get_cert", methods = ['POST'])
def issue():
	# dis = {'answer':str(int(request.json['a'])+int(request.json['b']))}

	# print(request.json)

	proofs = request.json['proofs']
	values = request.json['values']
	receiver = request.json['receiver']
	recv_ssn = request.json['recv_ssn']
	maker_addr = '0x9e7cd1df366a5d315e0f42d3d3e3100943281cb0'
	response = json.loads(abc_univ.issue(proofs = proofs, values = values, receiver = receiver, maker_addr=maker_addr, recv_ssn = recv_ssn))
	if response == {}:
		return response,400
	return jsonify(response),201

if __name__ == '__main__':
	app.run(port=8080)