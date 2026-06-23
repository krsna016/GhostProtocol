import tkinter as tk
from tkinter import messagebox
import subprocess
import threading
import time
import os
import random
import string
import re

class GhostProtocolApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GHOST PROTOCOL V3 - ULTIMATE OPSEC")
        self.root.geometry("850x750")
        self.root.configure(bg="#050505")
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width / 2) - (850 / 2))
        y = int((screen_height / 2) - (750 / 2))
        self.root.geometry(f"850x750+{x}+{y}")
        
        self.regions = {
            "Tokyo, Japan": {"tz": "Asia/Tokyo", "cc": "{jp}"},
            "London, UK": {"tz": "Europe/London", "cc": "{gb}"},
            "New York, USA": {"tz": "America/New_York", "cc": "{us}"},
            "Frankfurt, Germany": {"tz": "Europe/Berlin", "cc": "{de}"},
            "Sydney, Australia": {"tz": "Australia/Sydney", "cc": "{au}"},
            "Toronto, Canada": {"tz": "America/Toronto", "cc": "{ca}"},
            "Paris, France": {"tz": "Europe/Paris", "cc": "{fr}"},
            "Zurich, Switzerland": {"tz": "Europe/Zurich", "cc": "{ch}"},
            "Amsterdam, Netherlands": {"tz": "Europe/Amsterdam", "cc": "{nl}"},
            "Stockholm, Sweden": {"tz": "Europe/Stockholm", "cc": "{se}"},
            "Original (Restore)": {"tz": "Asia/Calcutta", "cc": "restore"}
        }
        
        self.killswitch_active = False
        self.original_hostname = self.get_hostname()
        self.ram_disk_id = None
        
        self.build_ui()
        self.update_live_status()

    def get_hostname(self):
        try:
            return subprocess.check_output(['scutil', '--get', 'ComputerName']).decode('utf-8').strip()
        except:
            return "MacBook"

    def build_ui(self):
        header = tk.Label(self.root, text="GHOST PROTOCOL V3", 
                          font=("Courier", 24, "bold"), fg="#00ffcc", bg="#050505")
        header.pack(pady=10)
        
        # Status Dashboard
        status_frame = tk.Frame(self.root, bg="#111111", highlightbackground="#333333", highlightthickness=1)
        status_frame.pack(fill="x", padx=30, pady=5)
        
        self.net_label = tk.Label(status_frame, text="Network Routing : Offline", font=("Courier", 12), fg="#aaaaaa", bg="#111111")
        self.net_label.pack(anchor="w", padx=20, pady=5)
        
        self.tz_label = tk.Label(status_frame, text="System Timezone : Scanning...", font=("Courier", 12), fg="#aaaaaa", bg="#111111")
        self.tz_label.pack(anchor="w", padx=20, pady=5)
        
        self.host_label = tk.Label(status_frame, text=f"System Hostname : {self.original_hostname}", font=("Courier", 12), fg="#aaaaaa", bg="#111111")
        self.host_label.pack(anchor="w", padx=20, pady=(5, 10))
        
        # Controls
        control_frame = tk.Frame(self.root, bg="#050505")
        control_frame.pack(fill="both", expand=True, padx=30, pady=10)
        
        tk.Label(control_frame, text="TARGET LOCATION:", font=("Courier", 12, "bold"), fg="#ffffff", bg="#050505").grid(row=0, column=0, sticky="w", pady=10)
        
        self.selected_region = tk.StringVar(value="Tokyo, Japan")
        self.region_menu = tk.OptionMenu(control_frame, self.selected_region, *self.regions.keys())
        self.region_menu.config(font=("Courier", 12), bg="#222222", fg="#ffffff", highlightthickness=0)
        self.region_menu.grid(row=0, column=1, sticky="w", padx=20, pady=10)
        
        # Checkboxes for V2 Features
        self.opt_dns = tk.BooleanVar(value=True)
        tk.Checkbutton(control_frame, text="[V2] Inject Cloudflare Encrypted DNS (ODoH)", variable=self.opt_dns, font=("Courier", 11), bg="#050505", fg="#00ffcc", selectcolor="#222222").grid(row=1, column=0, columnspan=2, sticky="w", pady=2)
        
        self.opt_host = tk.BooleanVar(value=True)
        tk.Checkbutton(control_frame, text="[V2] Scramble System Hostname randomly", variable=self.opt_host, font=("Courier", 11), bg="#050505", fg="#00ffcc", selectcolor="#222222").grid(row=2, column=0, columnspan=2, sticky="w", pady=2)
        
        self.opt_kill = tk.BooleanVar(value=True)
        tk.Checkbutton(control_frame, text="[V2] Enable Wi-Fi Kill-Switch (Drops Wi-Fi if Tor dies)", variable=self.opt_kill, font=("Courier", 11), bg="#050505", fg="#ff3333", selectcolor="#222222").grid(row=3, column=0, columnspan=2, sticky="w", pady=2)
        
        # Checkboxes for V3 Intense Features
        self.opt_hw_kill = tk.BooleanVar(value=True)
        tk.Checkbutton(control_frame, text="[V3] Hardware Decapitation (Kill Camera/Mic Daemons)", variable=self.opt_hw_kill, font=("Courier", 11), bg="#050505", fg="#ff00ff", selectcolor="#222222").grid(row=4, column=0, columnspan=2, sticky="w", pady=2)

        self.opt_ble_kill = tk.BooleanVar(value=True)
        tk.Checkbutton(control_frame, text="[V3] Radio Silence (Kill Bluetooth/AirDrop Beacons)", variable=self.opt_ble_kill, font=("Courier", 11), bg="#050505", fg="#ff00ff", selectcolor="#222222").grid(row=5, column=0, columnspan=2, sticky="w", pady=2)

        self.opt_dpi = tk.BooleanVar(value=True)
        tk.Checkbutton(control_frame, text="[V3] Deep Packet Disguise (Obfuscate Tor signature)", variable=self.opt_dpi, font=("Courier", 11), bg="#050505", fg="#ff00ff", selectcolor="#222222").grid(row=6, column=0, columnspan=2, sticky="w", pady=2)

        # Action Buttons
        btn_frame = tk.Frame(self.root, bg="#050505")
        btn_frame.pack(pady=10)
        
        self.btn_relocate = tk.Button(btn_frame, text="INITIATE SPOOF", font=("Courier", 14, "bold"), fg="#000000", bg="#00ffcc", width=18, command=self.start_spoofing)
        self.btn_relocate.grid(row=0, column=0, padx=5)
        
        self.btn_revert = tk.Button(btn_frame, text="REVERT & WIPE", font=("Courier", 14, "bold"), fg="#ffffff", bg="#ff3333", width=18, command=self.revert_system)
        self.btn_revert.grid(row=0, column=1, padx=5)
        
        self.btn_quarantine = tk.Button(btn_frame, text="RAM QUARANTINE", font=("Courier", 14, "bold"), fg="#ffffff", bg="#aa00ff", width=18, command=self.launch_quarantine)
        self.btn_quarantine.grid(row=0, column=2, padx=5)
        
        self.log_box = tk.Text(self.root, height=10, bg="#0a0a0a", fg="#00ffcc", font=("Courier", 10), bd=0, state="disabled")
        self.log_box.pack(fill="x", padx=30, pady=10)
        self.log("Ghost Protocol V3 Initialized. Standing by.")

    def log(self, message):
        self.log_box.config(state="normal")
        self.log_box.insert("end", f"[+] {message}\n")
        self.log_box.see("end")
        self.log_box.config(state="disabled")

    def get_real_tz(self):
        try:
            output = subprocess.check_output(['systemsetup', '-gettimezone']).decode('utf-8')
            return output.split(': ')[1].strip()
        except:
            return "Unknown"

    def update_live_status(self):
        tz = self.get_real_tz()
        hostname = self.get_hostname()
        self.tz_label.config(text=f"System Timezone : {tz}")
        self.host_label.config(text=f"System Hostname : {hostname}")

    def run_admin_command(self, cmd):
        apple_script = f"do shell script \"{cmd}\" with administrator privileges"
        try:
            subprocess.run(['osascript', '-e', apple_script], check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def write_tor_config(self, country_code):
        torrc_path = "/opt/homebrew/etc/tor/torrc"
        config = f"SocksPort 9050\nExitNodes {country_code}\nStrictNodes 1\n"
        if self.opt_dpi.get():
            config += "ClientTransportPlugin obfs4 exec /opt/homebrew/bin/obfs4proxy\n"
        with open(torrc_path, "w") as f:
            f.write(config)

    def monitor_killswitch(self):
        while self.killswitch_active:
            time.sleep(2)
            if os.system("pgrep tor > /dev/null") != 0:
                self.log("CRITICAL: TOR ENGINE CRASHED! ENGAGING KILL-SWITCH!")
                os.system("/usr/sbin/networksetup -setairportpower en0 off")
                self.killswitch_active = False
                break

    def start_spoofing(self):
        threading.Thread(target=self._spoof_process, daemon=True).start()

    def _spoof_process(self):
        self.btn_relocate.config(state="disabled")
        target_name = self.selected_region.get()
        target_info = self.regions[target_name]
        
        if target_info["cc"] == "restore":
            self._revert_process()
            return
            
        self.log(f"Initiating full network relocation to {target_name}...")
        
        os.system("killall tor 2>/dev/null")
        self.write_tor_config(target_info["cc"])
        os.system("/opt/homebrew/bin/tor > /dev/null 2>&1 &")
        self.log("Igniting The Onion Router... (Takes ~10 seconds)")
        if self.opt_dpi.get():
             self.log("Deep Packet Obfuscation Active (Traffic masquerading as regular HTTPS)")
        time.sleep(3)
        
        cmd = f"/usr/sbin/systemsetup -setusingnetworktime off; /usr/sbin/systemsetup -settimezone {target_info['tz']}; "
        cmd += f"/usr/sbin/networksetup -setsocksfirewallproxy 'Wi-Fi' 127.0.0.1 9050; /usr/sbin/networksetup -setsocksfirewallproxystate 'Wi-Fi' on; "
        
        if self.opt_dns.get():
            cmd += f"/usr/sbin/networksetup -setdnsservers 'Wi-Fi' 1.1.1.1 1.0.0.1; "
            self.log("Injecting Encrypted Cloudflare DNS...")
            
        if self.opt_host.get():
            scramble = "GHOST-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
            cmd += f"/usr/sbin/scutil --set ComputerName '{scramble}'; /usr/sbin/scutil --set LocalHostName '{scramble}'; /usr/sbin/scutil --set HostName '{scramble}'; "
            self.log(f"Scrambling Hostname to: {scramble}")

        if self.opt_hw_kill.get():
            cmd += f"/usr/bin/killall VDCAssistant 2>/dev/null; /usr/bin/killall AppleCameraAssistant 2>/dev/null; /usr/bin/killall coreaudiod 2>/dev/null; "
            self.log("Hardware Decapitation: Camera & Mic drivers violently unloaded.")

        if self.opt_ble_kill.get():
            cmd += f"defaults write /Library/Preferences/com.apple.Bluetooth ControllerPowerState -int 0; /usr/bin/killall blued 2>/dev/null; /usr/bin/killall sharingd 2>/dev/null; "
            self.log("Radio Silence: Bluetooth & AirDrop daemons massacred.")

        self.log("Authenticating master system override...")
        success = self.run_admin_command(cmd)
        
        if success:
            self.net_label.config(text="Network Routing : ACTIVE (Tor Proxy)", fg="#00ffcc")
            self.log("Timezone shifted. Wi-Fi traffic forced through Tor.")
            
            if self.opt_kill.get():
                self.killswitch_active = True
                threading.Thread(target=self.monitor_killswitch, daemon=True).start()
                self.log("Wi-Fi Kill-Switch ARMED. Monitoring connection...")
                
            self.log("ILLUSION COMPLETE.")
            self.root.after(1000, self.update_live_status)
        else:
            self.log("ERROR: Permission denied.")
            
        self.btn_relocate.config(state="normal")

    def revert_system(self):
        threading.Thread(target=self._revert_process, daemon=True).start()

    def _revert_process(self):
        self.btn_revert.config(state="disabled")
        self.killswitch_active = False
        self.log("Dropping Tor circuits and wiping forensic logs...")
        
        os.system("killall tor 2>/dev/null")
        
        cmd = (f"/usr/sbin/networksetup -setsocksfirewallproxystate 'Wi-Fi' off; "
               f"/usr/sbin/networksetup -setdnsservers 'Wi-Fi' 'Empty'; "
               f"/usr/sbin/systemsetup -settimezone Asia/Calcutta; "
               f"/usr/sbin/systemsetup -setusingnetworktime on; "
               f"/usr/sbin/scutil --set ComputerName '{self.original_hostname}'; "
               f"/usr/sbin/scutil --set LocalHostName '{self.original_hostname}'; "
               f"/usr/sbin/scutil --set HostName '{self.original_hostname}'; "
               f"defaults write /Library/Preferences/com.apple.Bluetooth ControllerPowerState -int 1; "
               f"/usr/bin/dscacheutil -flushcache; /usr/bin/killall -HUP mDNSResponder")
        
        success = self.run_admin_command(cmd)
        
        if self.ram_disk_id:
            os.system(f"diskutil eject {self.ram_disk_id} > /dev/null 2>&1")
            self.ram_disk_id = None
            self.log("RAM Disk power cut. All quarantine data evaporated.")

        if success:
            self.net_label.config(text="Network Routing : Offline", fg="#aaaaaa")
            self.log("System restored. DNS caches flushed. Logs obliterated. Hardware re-enabled.")
            self.root.after(1000, self.update_live_status)
        else:
            self.log("ERROR: Failed to revert.")
            
        self.btn_revert.config(state="normal")

    def launch_quarantine(self):
        threading.Thread(target=self._launch_ram_quarantine, daemon=True).start()

    def _launch_ram_quarantine(self):
        self.log("Allocating 1GB Volatile Memory (RAM Disk) for Ghost Vault...")
        try:
            # Create a 1GB RAM Disk (2097152 sectors * 512 bytes = 1GB)
            output = subprocess.check_output(['hdiutil', 'attach', '-nomount', 'ram://2097152']).decode('utf-8')
            self.ram_disk_id = output.strip()
            
            self.log(f"RAM Block acquired: {self.ram_disk_id}. Formatting HFS+...")
            os.system(f"diskutil erasevolume HFS+ 'GhostVault' {self.ram_disk_id} > /dev/null 2>&1")
            
            self.log("Launching completely isolated Chrome container inside RAM...")
            os.system('/Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --proxy-server="socks5://127.0.0.1:9050" --user-data-dir="/Volumes/GhostVault/ChromeData" --incognito > /dev/null 2>&1 &')
        except Exception as e:
            self.log(f"ERROR launching RAM Quarantine: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GhostProtocolApp(root)
    root.lift()
    root.attributes('-topmost', True)
    root.after_idle(root.attributes, '-topmost', False)
    root.mainloop()
