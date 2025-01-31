from netbox.plugins import PluginConfig

class AdestisAccountManagementConfig(PluginConfig):
    name = 'adestis_netbox_certificate_management'
    verbose_name = 'Certificate Management'
    description = 'A NetBox plugin for managing certficates.'
    version = '1.0.0'
    author = 'ADESTIS GmbH'
    author_email = 'pypi@adestis.de'
    base_url = 'certificates'
    required_settings = []
    default_settings = {
        'top_level_menu' : True,
    }

config = AdestisAccountManagementConfig
