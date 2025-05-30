
from flask_cors import CORS
from flask import Flask, request
from flask_cors import CORS
import requests
import oci
from datetime import datetime
import os
import json

# Flask
app = Flask(__name__)
CORS(app)

region = "eu-frankfurt-1"

# -- log --------------------------------------------------------------------

def log(s):
   dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
   print( "["+dt+"] "+ str(s), flush=True)

# -- forward_request --------------------------------------------------------

@app.route('/20240531/<path:path>', methods=['POST'])
def forward_request_post(path):
    log( "BEFORE SIGNER" )
    signer = oci.auth.signers.get_resource_principals_signer()
    config = {'region': signer.region, 'tenancy': signer.tenancy_id}
    log( "AFTER SIGNER" )
    
    api_key = 'Key'
    api_key_value = request.headers.get(api_key)

    if api_key_value != 'Key ' + os.getenv('API_KEY'):
        log( json.dumps(dict(request.headers), indent=4) ) 
        return "ERROR" , 401

    target_url = f'https://agent-runtime.generativeai.{region}.oci.oraclecloud.com/20240531/{path}' 
    log( target_url )

    log("forward_request="+str(request.json)) 
    resp = requests.post(target_url, json=request.json, auth=signer)
    log(resp)
    return resp.content

# -- info --------------------------------------------------------

@app.route('/info', methods=['GET'])
def info():
    return "OK"

# -- test ------------------------------------------------------------------
# Test using OCI SDK GenerativeAiAgentRuntimeClient

def test():
    # OK
    global signer
    log( "<test2>")
    endpoint = 'https://agent-runtime.generativeai.{region}.oci.oraclecloud.com'
    endpoint_id= "ocid1.genaiagentendpoint.oc1.eu-frankfurt-1.xxxxxxx"
    client = oci.generative_ai_agent_runtime.GenerativeAiAgentRuntimeClient(config = {}, service_endpoint=endpoint, signer=signer)  
    session_details = oci.generative_ai_agent_runtime.models.CreateSessionDetails(
        display_name="Test",
        description="Test"
    )
    resp = client.create_session(
            create_session_details=session_details,
            agent_endpoint_id=endpoint_id
    )
    log(resp.data)
    log( "</test2>")

# -- main -------------------------------------------------------------------

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)  

"""
export OCI_CLI_AUTH=instance_principal
oci generative-ai-agent-runtime session create 
  --agent-endpoint-id "ocid1.genaiagentendpoint.oc1.eu-frankfurt-1.xxxxxx" 
  --display-name "Test" 
  --description "Test" 
  --endpoint https://agent-runtime.generativeai.eu-frankfurt-1.oci.oraclecloud.com
"""    