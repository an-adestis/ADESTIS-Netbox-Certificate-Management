# Add your plugins and plugin settings here.
# Of course uncomment this file out.
from netbox_certificate_management.apps import AdestisCertificateManagementAppConfig
# To learn how to build images with your required plugins
# See https://github.com/netbox-community/netbox-docker/wiki/Using-Netbox-Plugins

PLUGINS = [
    #"netbox_bgp",
    "netbox_certificate_management",
    "adestis_netbox_applications",
    # "adestis_netbox_certificate_management"
]

PLUGINS_CONFIG = {
    "netbox_certificate_management": {
        'top_level_menu': True,
        },
    "adestis_netbox_plugin_applications": {},
    # "adestis_netbox_certificate_management": {}
}
