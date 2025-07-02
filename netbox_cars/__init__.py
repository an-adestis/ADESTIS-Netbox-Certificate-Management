from netbox.plugins import PluginConfig

class AdestisCarsConfig(PluginConfig):
    name = 'netbox_cars'
    verbose_name = 'Cars'
    description = 'A NetBox plugin for managing cars.'
    version = '1.0.2'
    author = 'ADESTIS GmbH'
    author_email = 'pypi@adestis.de'
    base_url = 'cars'
    required_settings = []
    default_settings = {
        'top_level_menu' : True,
    }

config = AdestisCarsConfig
