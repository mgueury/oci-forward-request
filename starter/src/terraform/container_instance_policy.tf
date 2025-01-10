# Default or OracleIdentityCloudService
variable idcs_domain_name { default = "Default" }
variable idcs_url { default = "" }

data "oci_identity_domains" "starter_domains" {
    #Required
    compartment_id = var.tenancy_ocid
    display_name = var.idcs_domain_name
}

locals {
  idcs_url = (var.idcs_url!="")?var.idcs_url:data.oci_identity_domains.starter_domains.domains[0].url
}

# XXX Should be more specific to the container instance id... XXX
resource "oci_identity_policy" "starter-ci_policy" {
  provider       = oci.home
  name           = "${var.prefix}-ci-policy"
  description    = "Container instance access to OCIR"
  compartment_id = var.tenancy_ocid
  statements = [
    "allow any-user to read repos in tenancy where ALL {request.resource.type='computecontainerinstance'}",
    "allow any-user to manage genai-agent-family in tenancy where ALL {request.resource.type='computecontainerinstance'}"
  ]
  freeform_tags = local.freeform_tags
}
