
import os, configparser as cp
import subprocess as sp


class sysAudio(object):

   def __init__(self, conf: cp.ConfigParser):
      self.conf: cp.ConfigParser = conf
      if self.conf is None:
         raise ValueError("ConfIsNone")
      self.default_soundcard = ""

   def set_default(self):
      self.default_soundcard = self.conf.get("SYSTEM", "DEFAULT_AUDIO")
      cmd: str = f"pactl set-default-sink {self.default_soundcard}"
      proc = sp.Popen(cmd, stdout=sp.PIPE, shell=True)
      return_code = proc.wait(8.0)
      if return_code == 1:
         print(f"SetDefaultSoundCard_Error: {self.default_soundcard}")
      else:
         print(f"SetDefaultSoundCard_OK: {self.default_soundcard}")
