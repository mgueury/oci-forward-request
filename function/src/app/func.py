
import io
import json
import logging
import os
import traceback
import oci
import requests
from fdk import response

# -- log --------------------------------------------------------------------

def log(s):
    logging.getLogger().info(s)

# -- handler -----------------------------------------------------------------

def handler(ctx, data: io.BytesIO = None):
    # agent_endpoint_ocid = os.getenv('TF_VAR_agent_endpoint_ocid')
    # tenancy_ocid = os.getenv('TF_VAR_tenancy_ocid')
    # region = os.getenv('TF_VAR_region')
    # log( "agent_endpoint_ocid=" + agent_endpoint_ocid );
    # log( "tenancy_ocid=" + tenancy_ocid );
    # log( "region=" + region );

    name = "World"
    try:
        body = json.loads(data.getvalue())
        log("body="+body) 
        name = body.get("name")
    except (Exception, ValueError) as ex:
        log(str(ex))

    log( "BEFORE SIGNER" )
    signer = oci.auth.signers.get_resource_principals_signer()
    config = {'region': signer.region, 'tenancy': signer.tenancy_id}
    log( "AFTER SIGNER" )

    api_key = 'key'
    api_key_value = ctx.Headers().get(api_key)
    log( "key=" + key )
    path=ctx.RequestURL()

    # if api_key_value != 'Key ' + os.getenv('API_KEY'):
    #    log( json.dumps(dict(request.headers), indent=4) ) 
    #    return "ERROR" , 401

    target_url = f'https://agent-runtime.generativeai.{signer.region}.oci.oraclecloud.com/20240531/{path}' 
    log( target_url )    

    # resp = requests.post(target_url, json=request.json, auth=signer)
    # log(resp)
    # return resp.content

    return response.Response(
        ctx, response_data=json.dumps(
            {"api_key" : api_key,
            "path" : path,
            "target_url" : target_url,
            "ctx.Headers": ctx.Headers()},            
            sort_keys=True, indent=4),
        headers={"Content-Type": "application/json"}
    )


    """
    return response.Response(
        ctx, response_data=json.dumps(
            {"Message": "Hello {0}".format(name),
            "ctx.Config" : dict(ctx.Config()),
            "ctx.Headers" : ctx.Headers(),
            "ctx.AppID" : ctx.AppID(),
            "ctx.FnID" : ctx.FnID(),
            "ctx.CallID" : ctx.CallID(),
            "ctx.Format" : ctx.Format(),
            "ctx.Deadline" : ctx.Deadline(),
            "ctx.RequestURL": ctx.RequestURL(),
            "ctx.Method": ctx.Method()},
            sort_keys=True, indent=4),
        headers={"Content-Type": "application/json"}
    )


    log( "BEFORE SIGNER" )
    signer = SignatureProvider.create_with_resource_principal()        
    # signer = oci.auth.signers.get_resource_principals_signer()
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

from borneo import NoSQLHandle, NoSQLHandleConfig, Regions
from borneo.iam import SignatureProvider
from borneo import QueryRequest

# NoSQL connection  
def get_connection():
    provider = SignatureProvider.create_with_resource_principal()        
    config = NoSQLHandleConfig( os.getenv('TF_VAR_nosql_endpoint'), provider )
    config.set_default_compartment( os.getenv('TF_VAR_compartment_ocid') )
    config.set_logger( None )        
    return NoSQLHandle(config)
handle = get_connection()

from fdk import response

def handler(ctx, data: io.BytesIO = None):
    
    a = []
    try:
        request = QueryRequest().set_statement('select deptno, dname, loc from dept')
        while True: 
            result = handle.query_iterable(request)
            for row in result:
                a.append(row)
            if request.is_done(): break
    except Exception as e:
        print(traceback.format_exc(), flush=True)
        print(e, flush=True)  
    print(a, flush=True)
    return response.Response(
        ctx, response_data=json.dumps(a),
        headers={"Content-Type": "application/json"}
    )

    


    
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

export OCI_CLI_AUTH=instance_principal
oci generative-ai-agent-runtime session create 
  --agent-endpoint-id "ocid1.genaiagentendpoint.oc1.eu-frankfurt-1.xxxxxx" 
  --display-name "Test" 
  --description "Test" 
  --endpoint https://agent-runtime.generativeai.eu-frankfurt-1.oci.oraclecloud.com

# -- handler -----------------------------------------------------------------

/*
# NoSQL connection  
def get_connection():
    provider = SignatureProvider.create_with_resource_principal()        
    config = NoSQLHandleConfig( os.getenv('TF_VAR_agent_endpoint'), provider )
    config.set_default_compartment( os.getenv('TF_VAR_compartment_ocid') )
    config.set_logger( None )        
    return NoSQLHandle(config)
    handle = get_connection()

    a = [ 
        { "deptno": "10", "dname": "ACCOUNTING", "loc": "Seoul"},
        { "deptno": "20", "dname": "RESEARCH", "loc": "Cape Town"},
        { "deptno": "30", "dname": "SALES", "loc": "Brussels"},
        { "deptno": "40", "dname": "OPERATIONS", "loc": "San Francisco"}
    ]  
    print(a, flush=True)
    return response.Response(
        ctx, response_data=json.dumps(a),
        headers={"Content-Type": "application/json"}
    )
"""