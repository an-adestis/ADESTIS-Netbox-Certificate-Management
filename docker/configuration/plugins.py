# Add your plugins and plugin settings here.
# Of course uncomment this file out.

# To learn how to build images with your required plugins
# See https://github.com/netbox-community/netbox-docker/wiki/Using-Netbox-Plugins

PLUGINS = [
    #"netbox_bgp",
    "netbox_cars",
    "adestis_netbox_applications"
]

PLUGINS_CONFIG = {
    "netbox_cars": {},
    "adestis_netbox_plugin_applications": {},
    
}
