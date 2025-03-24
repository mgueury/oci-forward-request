resource "oci_identity_policy" "starter_fn_policy" {
    provider       = oci.home    
    name           = "${var.prefix}-policy"
    description    = "${var.prefix} policy"
    compartment_id = local.lz_serv_cmp_ocid

    statements = [
        "allow any-user to manage genai-agent-family in compartment id ${local.lz_serv_cmp_ocid}"
        # "allow any-user to manage genai-agent-family in tenancy where request.principal.type='computecontainerinstance'"
    ]
}
