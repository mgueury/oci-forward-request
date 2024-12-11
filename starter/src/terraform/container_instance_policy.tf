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

# IDCS
resource "oci_identity_domains_dynamic_resource_group" "starter_ci_dyngroup" {
  #Required
  count          = (idcs_domain_name=="Default"?0:1) 
  provider       = oci.home
  display_name = "${var.prefix}-ci-dyngroup"
  idcs_endpoint = local.idcs_url
  matching_rule  = "ALL {resource.type='computecontainerinstance'}"
  schemas = ["urn:ietf:params:scim:schemas:oracle:idcs:DynamicResourceGroup"]
}

# Identity Domain
resource "oci_identity_dynamic_group" "starter_ci_dyngroup" {
  count          = (idcs_domain_name=="Default"?1:0) 
  provider       = oci.home    
  name           = "${var.prefix}-ci-dyngroup"
  description    = "Starter - All Container Instances"
  compartment_id = var.tenancy_ocid
  matching_rule  = "ALL {resource.type='computecontainerinstance'}"
  freeform_tags = local.freeform_tags
}

resource "oci_identity_policy" "starter-ci_policy" {
  provider       = oci.home
  name           = "${var.prefix}-ci-policy"
  description    = "Container instance access to OCIR"
  compartment_id = var.tenancy_ocid
  statements = [
    "allow dynamic-group ${var.idcs_domain_name}/${var.prefix}-ci-dyngroup to read repos in tenancy"
  ]
  freeform_tags = local.freeform_tags
}
