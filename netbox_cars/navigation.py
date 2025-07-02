from netbox.plugins import PluginMenuItem, PluginMenuButton, PluginMenu
from netbox.choices import ButtonColorChoices
from django.conf import settings

_cars = [
    PluginMenuItem(
        link='plugins:netbox_cars:cars_list',
        link_text='Cars',
        permissions=["netbox_cars.cars_list"],
        buttons=(
            PluginMenuButton('plugins:netbox_cars:cars_add', 'Add', 'mdi mdi-plus-thick', ButtonColorChoices.GREEN, ["netbox_cars.cars_add"]),
        )
    ),    
]

plugin_settings = settings.PLUGINS_CONFIG.get('netbox_cars', {})

if plugin_settings.get('top_level_menu'):
    menu = PluginMenu(  
        label="Cars",
        groups=(
            ("Cars", _cars),
        ),
        icon_class="mdi mdi-key",
    )
else:
    menu_items = _cars