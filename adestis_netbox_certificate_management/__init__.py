from netbox.plugins import PluginConfig

class AdestisCertificateConfig(PluginConfig):
    name = 'adestis_netbox_certificate_management'
    verbose_name = 'Certificate Management'
    description = 'A NetBox plugin for managing certificate.'
    version = '1.0.22'
    author = 'ADESTIS GmbH'
    author_email = 'pypi@adestis.de'
    base_url = 'certificate'
    required_settings = []
    default_settings = {
        'top_level_menu' : True,
    }
    docs_url = 'https://github.com/an-adestis/ADESTIS-Netbox-Certificate-Management/wiki'
    scripts = ['adestis_netbox_certifivate_management.scripts.MergeCertificatesScript']

config = AdestisCertificateConfig
default_app_config = "adestis_netbox_certificate_management.apps.AdestisCertificateManagementAppConfig"
