from netbox.plugins import PluginMenuItem, PluginMenuButton, PluginMenu
from netbox.choices import ButtonColorChoices
from django.conf import settings

_certificate = [
    PluginMenuItem(
        link='plugins:adestis_netbox_certificate_management:certificate_list',
        link_text='Certificate',
        permissions=["adestis_netbox_certificate_management.certificate_list"],
        buttons=(
            PluginMenuButton('plugins:adestis_netbox_certificate_management:certificate_add', 'Add', 'mdi mdi-plus-thick', ButtonColorChoices.GREEN, ["netbox_certificate.certificate_add"]),
        )
    ),    
]

plugin_settings = settings.PLUGINS_CONFIG.get('adestis_netbox_certificate_management', {})

if plugin_settings.get('top_level_menu'):
    menu = PluginMenu(  
        label="Certificate Management",
        groups=(
            ("Certificate", _certificate),
        ),
        icon_class="mdi mdi-certificate",
    )
else:
    menu_items = _certificate