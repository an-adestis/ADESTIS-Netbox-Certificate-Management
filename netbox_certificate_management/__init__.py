from netbox.plugins import PluginConfig

class AdestisCertificateConfig(PluginConfig):
    name = 'netbox_certificate_management'
    verbose_name = 'Certificate Management'
    description = 'A NetBox plugin for managing certificate.'
    version = '1.0.2'
    author = 'ADESTIS GmbH'
    author_email = 'pypi@adestis.de'
    base_url = 'certificate'
    required_settings = []
    default_settings = {
        'top_level_menu' : True,
    }

config = AdestisCertificateConfig
