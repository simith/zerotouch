import os
from flask import Flask
from flask import jsonify 

class CertGenerator(object):
    
    def __init__(self): # this method creates the class object.
        pass



    def createCerts(self,thingName):
        # create a Private/Public Keypair
        certFolder = "../certs/"
        rootCaFileName =  certFolder +"iotRootCA.pem"
        thingKeyFileName = certFolder +thingName + ".key"
        thingCsrFileName = certFolder +thingName + ".csr"
        factoryCAPemFile = certFolder + "FactoryCACertificate.pem"
        catoryCAKeyFile = certFolder + "FactoryCACertificate.key"
        csrFileName = certFolder +thingName + ".csr"
        deviceCertFileName = certFolder + thingName + ".crt"
        deviceCertFileNameWithCA = certFolder + thingName + "-with-ca" + ".crt"

        commandStr = "openssl genrsa -out "+thingKeyFileName+" 2048"
        self.shellComand(commandStr)
        # create a CSR to send off to the CA for signing
        commandStr = "openssl req -new -key "+ thingKeyFileName + " -out " + thingCsrFileName  +" -subj \"/C=GB/ST=London/L=London/O=Global Security/OU=IT Department/CN="+thingName+"\" "
        self.shellComand(commandStr)
        # Let the CA sign the cert now
        commandStr = "openssl x509 -req -in " + csrFileName  +" -CA "+ factoryCAPemFile+ " -CAkey "+ catoryCAKeyFile + " -CAcreateserial -out "+deviceCertFileName+" -days 365 -sha256"
        self.shellComand(commandStr)
        # Let's join the CA cert to device cert for verification and trust
        commandStr = "cat "+ deviceCertFileName + " " + factoryCAPemFile  +   " > " + deviceCertFileNameWithCA
        self.shellComand(commandStr)

        # get the 3 files Device cert, Private key and Root CA and send it back to the Device
        devCertFile = self.getFile(deviceCertFileNameWithCA)
        devPrivFile = self.getFile(thingKeyFileName)
        rootCAFile = self.getFile(rootCaFileName)
        print(devCertFile)
        print(devPrivFile)
        print(rootCAFile)

        jsonObject = {}
        jsonObject['thing'] = thingName
        jsonObject['device-cert']=devCertFile
        jsonObject['device-privkey']= devPrivFile
        jsonObject['rootca-cert']= rootCAFile
        #also send the rootCA certificate
        jsonResponse = jsonify(jsonObject)
        return jsonResponse



    def shellComand(self,command):
        os.system(command)

    def getFile(self,fileName):
        with open(fileName, 'r') as myfile:
            data=myfile.read()
            return data;
        
if __name__ == "__main__":
    CertGenerator().createCerts("thermo-dynamics-001")