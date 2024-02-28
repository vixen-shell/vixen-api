from typing import Dict, List
from .Gtk_imports import Gtk, GLib
from .FeatureSetting import FrameSettingsDict
from .frame_view import create_frame

class SingleFrameHandler:
    def __init__(self, frame_settings: FrameSettingsDict):
        self.frame_settings = frame_settings.single_frame_settings
        self.frames: Dict[str, Gtk.Window] = {}

    def init(self):
        def init_task():
            for id in self.frame_settings:
                frame = create_frame(self.frame_settings[id])
                self.frames[id] = frame

        GLib.idle_add(init_task)

    def show(self, id: str):
        if id in self.frames:
            frame = self.frames[id]
            if not frame.get_visible(): frame.show_all()

    def hide(self, id: str):
        if id in self.frames:
            frame = self.frames[id]
            if frame.get_visible(): frame.hide()

    def cleanup(self):
        ids = list(self.frames.keys())
        for id in ids: self.frames[id].close()
        self.frames = {}

    @property
    def frame_ids(self) -> List[str]:
        return list(self.frame_settings.keys())
    
    @property
    def active_frame_ids(self) -> List[str]:
        ids: List[str] = []

        for id in self.frames:
            if self.frames[id].get_visible():
                ids.append(id)

        return ids

class InstanceFrameHandler:
    def __init__(self, frame_settings: FrameSettingsDict):
        self.frame_settings = frame_settings.instance_frame_settings
        self.frames: Dict[str, Gtk.Window] = {}
        self.last_frame_indexes: Dict[str, int] = {}

    def count_frame_indexes(self, frame_id: str):
        return sum(1 for key in self.frames if key.startswith(frame_id))

    def new_frame_index(self, frame_id: str):
        if self.count_frame_indexes(frame_id) == 0:
            if frame_id in self.last_frame_indexes:
                del self.last_frame_indexes[frame_id]    
                
        return self.last_frame_indexes.get(frame_id, -1) + 1

    def open(self, frame_id: str) -> (str | None):
        frame_index = self.new_frame_index(frame_id)
        indexed_frame_id = f'{frame_id}_{frame_index}'

        if frame_id in self.frame_settings and not indexed_frame_id in self.frames:
            def process():
                frame = create_frame(self.frame_settings[frame_id])

                def on_delete_event(frame, event):
                    if indexed_frame_id in self.frames:
                        del self.frames[indexed_frame_id]
                        
                    return False

                frame.connect('delete-event', on_delete_event)

                self.last_frame_indexes[frame_id] = frame_index
                self.frames[indexed_frame_id] = frame

            GLib.idle_add(process)
            return indexed_frame_id

    def close(self, id: str):
        if id in self.frames:
            self.frames[id].close()

    def cleanup(self):
        ids = list(self.frames.keys())
        for id in ids: self.frames[id].close()
        self.last_frame_indexes = {}
        self.frames = {}

    @property
    def frame_ids(self):
        return list(self.frame_settings.keys())

    @property
    def active_frame_ids(self):
        return list(self.frames.keys())

class FrameHandler:
    def __init__(self, frame_settings: FrameSettingsDict):
        self.single_frames = SingleFrameHandler(frame_settings)
        self.instance_frames = InstanceFrameHandler(frame_settings)

    def init(self):
        self.single_frames.init()

    def open(self, id: str) -> (str | None):
        if id in self.single_frames.frame_ids:
            self.single_frames.show(id)

        if id in self.instance_frames.frame_ids:
            return self.instance_frames.open(id)

    def close(self, id: str):
        if id in self.single_frames.active_frame_ids:
            self.single_frames.hide(id)
        
        if id in self.instance_frames.active_frame_ids:
            self.instance_frames.close(id)

    def cleanup(self):
        self.single_frames.cleanup()
        self.instance_frames.cleanup()

    @property
    def frame_ids(self) -> List[str]:
        return self.single_frames.frame_ids + self.instance_frames.frame_ids
    
    @property
    def active_frame_ids(self) -> List[str]:
        return self.single_frames.active_frame_ids + self.instance_frames.active_frame_ids