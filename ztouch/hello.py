import os
from flask import Flask
from certmaker.certgen import CertGenerator

app = Flask(__name__)

@app.route('/ztouch/thing/<thingname>/certs/')
def configure_thing(thingname):   
    certgen = CertGenerator()
    response = certgen.createCerts(thingname)
    return response



app.run(host= '0.0.0.0')
