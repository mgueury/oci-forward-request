variable docker_image_app {
    default=""
} 

variable api_key {
    default="12345"
} 

resource oci_container_instances_container_instance starter_container_instance {
  count = var.docker_image_app == "" ? 0 : 1
  availability_domain = data.oci_identity_availability_domain.ad.name
  compartment_id      = local.lz_appdev_cmp_ocid  
  container_restart_policy = "ALWAYS"
  containers {
    display_name = "app"
    image_url = var.docker_image_app
    is_resource_principal_disabled = "false"
    environment_variables = { 
      "API_KEY" = "${var.api_key}"
    }    
  } 
  display_name = "${var.prefix}-ci"
  graceful_shutdown_timeout_in_seconds = "0"
  shape                                = "CI.Standard.E4.Flex"  
  shape_config {
    memory_in_gbs = "4"
    ocpus         = "1"
  }
  state = "ACTIVE"
  vnics {
    display_name           = "${var.prefix}-ci"
    hostname_label         = "${var.prefix}-ci"
    skip_source_dest_check = "true"
    subnet_id              = data.oci_core_subnet.starter_private_subnet.id
  }
  freeform_tags = local.freeform_tags    
}