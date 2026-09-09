import subprocess, threading, time, os
from app.volume_controller import VolumeController

class Player:
    def __init__(self):
        self.vol_ctrl = VolumeController()

    def play_netease(self, playlist_id_or_song_id, type='playlist'):
        if type == 'playlist':
            uri = f"orpheus://playlist/{playlist_id_or_song_id}"
        else:
            uri = f"orpheus://song/{playlist_id_or_song_id}"
        subprocess.Popen(["start", uri], shell=True)

    def alarm(self, target_id, target_type='playlist', volume=0.5, gradual_duration=30):
        self.vol_ctrl.gradual_increase(volume, gradual_duration)
        time.sleep(gradual_duration)
        self.play_netease(target_id, target_type)

    def shutdown_after(self, minutes):
        seconds = int(minutes * 60)
        os.system(f'shutdown /h /t {seconds}')
