echo
echo "-- CURL TEST COMMAND --------------------------------------------------"
echo "curl -i \\"
echo "     --request POST \\"
echo "     --header \"Content-Type: application/json\" \\"
echo "     --header \"Key: Key $TF_VAR_api_key\" \\"
echo "     --data '{\"idleTimeoutInSeconds\": \"3600\"}' \\"
echo "     $UI_URL/app/20240531/agentEndpoints/{agentEndpointId}/sessions"
echo
echo "-- OCI Forward Request ------------------------------------------------"
echo
echo URL for Gen AI Agent: $UI_URL/app/20240531
echo
echo In Oracle Digital Assistant: add 2 REST API Services:
echo - $UI_URL/app/20240531/agentEndpoints/{agentEndpointId}/sessions
echo - $UI_URL/app/20240531/agentEndpoints/{agentEndpointId}/sessions/{sessionId}/actions/execute
echo
echo For each of them 
echo - Authentication Type: API_KEY
echo - Include as: Header
echo - API_KEY Key   : Key
echo - API_KEY Value : $TF_VAR_api_key
