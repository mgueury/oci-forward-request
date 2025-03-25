
import io
import json
import logging
import os
import oci
import requests
from fdk import response

# -- log --------------------------------------------------------------------

def log(s):
    logging.getLogger().info(s)

# -- handler -----------------------------------------------------------------

def handler(ctx, data: io.BytesIO = None):
    try:
        body = json.loads(data.getvalue())
        log("body="+body) 
    except (Exception, ValueError) as ex:
        log(str(ex))

    log( "BEFORE SIGNER" )
    signer = oci.auth.signers.get_resource_principals_signer()
    config = {'region': signer.region, 'tenancy': signer.tenancy_id}
    log( "AFTER SIGNER" )

    api_key = 'key'
    api_key_value = ctx.Headers().get(api_key)
    log( "api_key_value=" + api_key_value )
    if api_key_value != 'Key ' + os.getenv('API_KEY'):
        log( json.dumps(ctx.Headers(), indent=4) ) 
        return "ERROR" , 401

    path=ctx.RequestURL()
    path=path[path.index("20240531"):]
    target_url = f'https://agent-runtime.generativeai.{signer.region}.oci.oraclecloud.com/{path}' 
    log( target_url )    

    resp = requests.post(target_url, json=body, auth=signer)
    log(resp)
    return resp.content

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
"""