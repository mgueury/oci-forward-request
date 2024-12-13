# OCI Forward Request

The goal is to allow Oracle Digital Assistant - ODA (SaaS) to use Oracle Generative AI Agent running in another tenancy. 

The repository contains:
- a program that converts API_KEY security to OCI Security
- in the particular case of the API Oracle Generative AI Agent

## Architecture

This program converts the security protocol from API_KEY to RESOURCE_PRINCIPAL and Policies

ODA (SaaS) ----( API_KEY ) ---> APIGW (OCI) --> Container Instance ----( Resource Principal )----> OCI Generative AI Agent

Resource principal uses an OCI Policy to get access to the OCI Generative AI Agent APIs.

## Installation
From OCI Cloud Shell with *Public Network* and *Architecture X86*

- Double check that OCI Cloud shell uses:
    - *Public Network* (for more info see Note 3 below)
    - *Architecture* (see menu) X86 

- Download
```
git clone https://github.com/mgueury/oci-forward-request.git
cd oci-forward-request
```
- Build (optional: edit file starter/env.sh to put your own password)
```
cd starter
./build.sh
Answer the questions: 
- Compartment ocid
- Auth Token (To create a docker image in the Container Registry)
- API_KEY value
```

Output looks like
```
-- OCI Forward Request -------------------------------------------
URL for Gen AI Agent: https://xxxx.apigateway.eu-frankfurt-1.oci.customer-oci.com/forward/app/20240531

In Oracle Digital Assistant: add 2 REST API Services:
- https://xxxx.apigateway.eu-frankfurt-1.oci.customer-oci.com/forward/app/20240531/agentEndpoints/{agentEndpointId}/sessions
- https://xxxx.apigateway.eu-frankfurt-1.oci.customer-oci.com/forward/app/20240531/agentEndpoints/{agentEndpointId}/sessions/{sessionId}/actions/execute

For each of them
- Authentication Type: API_KEY
- Include as: Header
- API_KEY Key : Key
- API_KEY Value : 12345678
```

## Destroy

```
cd starter
./destroy.sh
```

## Notes

1. This works only if a policy is added to allow the Container Instance to manage GenAI Agent. Ex:
   allow group Default/forward-ci-dyngroup to manage genai-agent-family in compartment xxxxx
2. If you call the API with wget / curl / postman, ... Key=Key / Value=Key 12345678
3. Requirements: Use Cloud Shell with Public Network.
   
    This setup assumes that you have access to OCI Cloud Shell with Public Network access. To check if you have it, start Cloud Shell and you should see Network: Public on the top. If not, try to change to Public Network. If it works, there is nothing to do.
   
    OCI Administrator have that right automatically. Or your administrator has maybe already added the required policy.
   
    **Solution:**
   
    If not, please ask your Administrator to follow this document:
    [https://docs.oracle.com/en-us/iaas/Content/API/Concepts/cloudshellintro_topic-Cloud_Shell_Networking.htm#cloudshellintro_topic-Cloud_Shell_Public_Network](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/cloudshellintro_topic-Cloud_Shell_Networking.htm#cloudshellintro_topic-Cloud_Shell_Public_Network)
    He/She just need to add a Policy to your tenancy :
    ```
    allow group <GROUP-NAME> to use cloud-shell-public-network in tenancy
    ```
