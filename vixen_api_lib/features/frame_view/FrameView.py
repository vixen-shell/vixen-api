from .setting import FrameSetting
from .utils import get_webview, layerise_frame
from ..Gtk_imports import Gtk

def create_frame(frame_setting: FrameSetting):
    is_layer = True if frame_setting.layer else False

    frame = Gtk.Window()
    frame.set_title(frame_setting.title)
    
    frame.add(get_webview(
        is_layer = is_layer,
        feature = frame_setting.feature,
        route = frame_setting.route
    ))

    if not is_layer:
        if not frame_setting.instantiable:
            def on_delete_event(frame, event):
                frame.hide()
                return True
            
            frame.connect('delete-event', on_delete_event)

    if is_layer:
        layerise_frame(frame, frame_setting.layer)

    if frame_setting.instantiable or frame_setting.show_on_startup:
        frame.show_all()
    
    return frame