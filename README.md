# OCI Forward Request

The repository contains:
- a program that convert API_KEY security to OCI Security
- in the particular case of Oracle Generative AI Agent
- the API that are accessible (if policy exists ) are the one of Oracle Generative AI Agent

## Requirements

The lab is using Cloud Shell with Public Network.

The lab assume that you have access to OCI Cloud Shell with Public Network access. To check if you have it, start Cloud Shell and you should see Network: Public on the top. If not, try to change to Public Network. If it works, there is nothing to do.

OCI Administrator have that right automatically. Or your administrator has maybe already added the required policy.

#### Solution:
  If not, please ask your Administrator to follow this document:
  
  https://docs.oracle.com/en-us/iaas/Content/API/Concepts/cloudshellintro_topic-Cloud_Shell_Networking.htm#cloudshellintro_topic-Cloud_Shell_Public_Network

   He/She just need to add a Policy to your tenancy :
   ```
   allow group <GROUP-NAME> to use cloud-shell-public-network in tenancy
   ```

## Installation
From OCI Cloud Shell with access to Public Network

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
-----------------------------------------------------------------------
APEX login:

APEX Workspace
http://11.22.33.44/ords/_/landing
  Workspace: APEX_APP
  User: APEX_APP
  Password: <DB password>

APEX APP
http://11.22.33.44/ords/r/apex_app/apex_app/
  User: dana.alhammadi@company.com / <DB password>
```

## Destroy

```
cd starter
./destroy.sh
```

## Known issue

1. If you try to deploy the same installation, it can happens that some object have a unique name and the second installation will fail because of duplicate names.  
  Work-around: 
  - Edit the starter/env.sh file
  - Set the TF_VAR_prefix to an unique value


To build the solution: 
- start a OCI Cloud Shell 
    - in Public network 
    - set Architecture to x86 - Intel/AMD
- wget of this repository
- unzip
- cd oci-forward-request*
- cd starter
- edit the env.sh file and set a value to the KEY
- run ./build.sh
- The URL is given at the end

Use it in Oracle Digital Assistant:

https://

To destroy
- run ./destroy.sh
