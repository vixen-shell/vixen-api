"""
Author            : Nohavye
Author's Email    : noha.poncelet@gmail.com
Repository        : https://github.com/vixen-shell/vixen-client.git
Description       : Module for creating a Gtk webview.
License           : GPL3
"""
from ..Gtk_imports import Gdk, WebKit2
from ...globals import get_front_url

def webview(
        is_layer: bool,
        feature_name: str,
        route: str | None
):
    def webKit_settings():
        settings = WebKit2.Settings()
        settings.set_property("hardware_acceleration_policy", WebKit2.HardwareAccelerationPolicy.ALWAYS)
        settings.set_property("enable-developer-extras", True)
        return settings

    webview = WebKit2.WebView()
    webview.set_settings(webKit_settings())

    route_param = f'&route={route}' if route else ''
    webview.load_uri(f"{get_front_url()}/?feature={feature_name}{route_param}")
    
    if is_layer:
        webview.set_background_color(
            Gdk.RGBA(red=0, green=0, blue=0, alpha=0.0)
        )

    return webview