from netbox.plugins import PluginMenuItem, PluginMenuButton, PluginMenu
from netbox.choices import ButtonColorChoices
from django.conf import settings

_certificates = [
    PluginMenuItem(
        link='plugins:adestis_netbox_certificate_management:certificate_list',
        link_text='Certificates',
        permissions=["adestis_netbox_certificate_management.certificate_list"],
        buttons=(
            PluginMenuButton('plugins:adestis_netbox_certificate_management:certificate_add', 'Add', 'mdi mdi-plus-thick', ButtonColorChoices.GREEN, ["adestis_netbox_certificate_management.certificate_add"]),
        )
    ),    
]

plugin_settings = settings.PLUGINS_CONFIG.get('adestis_netbox_certificate_management', {})

if plugin_settings.get('top_level_menu'):
    menu = PluginMenu(  
        label="Certificates",
        groups=(
            ("Certificates", _certificates),
        ),
        icon_class="mdi mdi-key",
    )
else:
    menu_items = _certificates