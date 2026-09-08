from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import time, threading

class VolumeController:
    def __init__(self):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(interface, POINTER(IAudioEndpointVolume))

    def get_current_volume(self):
        return self.volume.GetMasterVolumeLevelScalar()

    def set_volume(self, scalar):
        self.volume.SetMasterVolumeLevelScalar(scalar, None)

    def gradual_increase(self, target_scalar=0.5, duration=30):
        """渐进增大音量"""
        start = self.get_current_volume()
        steps = int(duration * 10)
        if steps <= 0:
            self.set_volume(target_scalar)
            return
        increment = (target_scalar - start) / steps
        def _increase():
            current = start
            for i in range(steps):
                current += increment
                self.set_volume(max(0, min(1, current)))
                time.sleep(0.1)
        threading.Thread(target=_increase, daemon=True).start()
