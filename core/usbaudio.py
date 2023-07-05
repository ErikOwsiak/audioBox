
import os, sys, re
import configparser as cp


class usbAudio(object):

   def __init__(self, hub_id: str, *card_ids):
      self.hub_id = hub_id
      self.card_ids = card_ids
      self.usb_hub: str = ""
      self.usb_cards: [] = []

   def prob_usb_cards(self) -> int:
      try:
         lns: [] = os.popen("lsusb").readlines()
         arr: [] = [ln for ln in lns if self.hub_id in ln]
         # -- --
         if len(arr) == 0:
            print("[ SoundCardUsbHubNotFound ]\n[ Connect: iotech.systems 7 port sound card ]")
            sys.exit(1)
         elif len(arr) == 1:
            self.usb_hub = arr[0].strip()
         else:
            print("WrongSoundCardUsbHubCountFound")
            sys.exit(2)
         # -- --
         print(f"[ hub: {self.usb_hub} ]")
         for card_id in self.card_ids:
            self.usb_cards.extend([ln.strip() for ln in lns if card_id in ln])
         [print(f"[ card: {c} ]") for c in self.usb_cards]
         # -- --
         return 0
      except Exception as e:
         print(e)

   def probe_sys_class_sound(self):
      arr: [] = []
      cmd = "cd /sys/class/sound && ls -la"
      lns = os.popen(cmd).readlines()
      flr0 = "usb1"; flr1 = "sound"; s = "->"
      [arr.append(ln.split(s)[1].strip()) for ln in lns if (flr0 in ln) and (flr1 in ln)]
      # [print(ln.strip()) for ln in arr]

   def probe_proc_asound_cards(self) -> []:
      _key: str = ""
      tmp: {} = {}
      # -- --
      def __proc_ln(ln: str):
         nonlocal _key
         if ": USB-Audio -" in ln:
            found = re.findall(r"\[(.*)\]", ln)
            if len(found) > 0:
               _key = found[0].strip()
         else:
            _s: str = ln.strip()
            if _s.startswith("BurrBrown") or _s.startswith("Burr-Brown"):
               val: str = ln.split("DAC at")[1].strip()
               tmp[_key] = val.split(",")[0].strip()
            else:
               pass
      # -- --
      arr: [] = []
      cmd = "cat /proc/asound/cards"
      lns = os.popen(cmd).readlines()
      [arr.append(ln) for ln in lns]
      [__proc_ln(ln) for ln in arr]
      ordered: {} = dict(sorted(tmp.items()))
      [print(f"{k}: {ordered[k]}") for k in ordered]
      # -- --
      return ordered
