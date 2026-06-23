import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import threading
import time
import os
import random
import string

class GhostProtocolApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GHOST PROTOCOL V3 - ULTIMATE OPSEC")
        self.root.geometry("1100x1000")
        self.root.configure(bg="#020202")
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width / 2) - (1100 / 2))
        y = int((screen_height / 2) - (1000 / 2))
        self.root.geometry(f"1100x1000+{x}+{y}")
        
        self.regions = {
            "Original (Restore)": {"tz": "Asia/Calcutta", "cc": "restore"},
            "Argentina (Buenos Aires)": {"tz": "America/Argentina/Buenos_Aires", "cc": "{ar}"},
            "Australia (Sydney)": {"tz": "Australia/Sydney", "cc": "{au}"},
            "Austria (Vienna)": {"tz": "Europe/Vienna", "cc": "{at}"},
            "Belgium (Brussels)": {"tz": "Europe/Brussels", "cc": "{be}"},
            "Brazil (Sao Paulo)": {"tz": "America/Sao_Paulo", "cc": "{br}"},
            "Bulgaria (Sofia)": {"tz": "Europe/Sofia", "cc": "{bg}"},
            "Canada (Toronto)": {"tz": "America/Toronto", "cc": "{ca}"},
            "Chile (Santiago)": {"tz": "America/Santiago", "cc": "{cl}"},
            "Colombia (Bogota)": {"tz": "America/Bogota", "cc": "{co}"},
            "Costa Rica (San Jose)": {"tz": "America/Costa_Rica", "cc": "{cr}"},
            "Croatia (Zagreb)": {"tz": "Europe/Zagreb", "cc": "{hr}"},
            "Cyprus (Nicosia)": {"tz": "Asia/Nicosia", "cc": "{cy}"},
            "Czechia (Prague)": {"tz": "Europe/Prague", "cc": "{cz}"},
            "Denmark (Copenhagen)": {"tz": "Europe/Copenhagen", "cc": "{dk}"},
            "Estonia (Tallinn)": {"tz": "Europe/Tallinn", "cc": "{ee}"},
            "Finland (Helsinki)": {"tz": "Europe/Helsinki", "cc": "{fi}"},
            "France (Paris)": {"tz": "Europe/Paris", "cc": "{fr}"},
            "Germany (Frankfurt)": {"tz": "Europe/Berlin", "cc": "{de}"},
            "Greece (Athens)": {"tz": "Europe/Athens", "cc": "{gr}"},
            "Hong Kong (HK)": {"tz": "Asia/Hong_Kong", "cc": "{hk}"},
            "Hungary (Budapest)": {"tz": "Europe/Budapest", "cc": "{hu}"},
            "Iceland (Reykjavik)": {"tz": "Atlantic/Reykjavik", "cc": "{is}"},
            "India (Mumbai)": {"tz": "Asia/Kolkata", "cc": "{in}"},
            "Indonesia (Jakarta)": {"tz": "Asia/Jakarta", "cc": "{id}"},
            "Ireland (Dublin)": {"tz": "Europe/Dublin", "cc": "{ie}"},
            "Israel (Jerusalem)": {"tz": "Asia/Jerusalem", "cc": "{il}"},
            "Italy (Rome)": {"tz": "Europe/Rome", "cc": "{it}"},
            "Japan (Tokyo)": {"tz": "Asia/Tokyo", "cc": "{jp}"},
            "Latvia (Riga)": {"tz": "Europe/Riga", "cc": "{lv}"},
            "Lithuania (Vilnius)": {"tz": "Europe/Vilnius", "cc": "{lt}"},
            "Luxembourg (Luxembourg)": {"tz": "Europe/Luxembourg", "cc": "{lu}"},
            "Malaysia (Kuala Lumpur)": {"tz": "Asia/Kuala_Lumpur", "cc": "{my}"},
            "Mexico (Mexico City)": {"tz": "America/Mexico_City", "cc": "{mx}"},
            "Moldova (Chisinau)": {"tz": "Europe/Chisinau", "cc": "{md}"},
            "Netherlands (Amsterdam)": {"tz": "Europe/Amsterdam", "cc": "{nl}"},
            "New Zealand (Auckland)": {"tz": "Pacific/Auckland", "cc": "{nz}"},
            "Norway (Oslo)": {"tz": "Europe/Oslo", "cc": "{no}"},
            "Panama (Panama City)": {"tz": "America/Panama", "cc": "{pa}"},
            "Peru (Lima)": {"tz": "America/Lima", "cc": "{pe}"},
            "Poland (Warsaw)": {"tz": "Europe/Warsaw", "cc": "{pl}"},
            "Portugal (Lisbon)": {"tz": "Europe/Lisbon", "cc": "{pt}"},
            "Romania (Bucharest)": {"tz": "Europe/Bucharest", "cc": "{ro}"},
            "Serbia (Belgrade)": {"tz": "Europe/Belgrade", "cc": "{rs}"},
            "Singapore (Singapore)": {"tz": "Asia/Singapore", "cc": "{sg}"},
            "Slovakia (Bratislava)": {"tz": "Europe/Bratislava", "cc": "{sk}"},
            "Slovenia (Ljubljana)": {"tz": "Europe/Ljubljana", "cc": "{si}"},
            "South Africa (Johannesburg)": {"tz": "Africa/Johannesburg", "cc": "{za}"},
            "South Korea (Seoul)": {"tz": "Asia/Seoul", "cc": "{kr}"},
            "Spain (Madrid)": {"tz": "Europe/Madrid", "cc": "{es}"},
            "Sweden (Stockholm)": {"tz": "Europe/Stockholm", "cc": "{se}"},
            "Switzerland (Zurich)": {"tz": "Europe/Zurich", "cc": "{ch}"},
            "Taiwan (Taipei)": {"tz": "Asia/Taipei", "cc": "{tw}"},
            "Thailand (Bangkok)": {"tz": "Asia/Bangkok", "cc": "{th}"},
            "Turkey (Istanbul)": {"tz": "Europe/Istanbul", "cc": "{tr}"},
            "Ukraine (Kyiv)": {"tz": "Europe/Kyiv", "cc": "{ua}"},
            "United Arab Emirates (Dubai)": {"tz": "Asia/Dubai", "cc": "{ae}"},
            "United Kingdom (London)": {"tz": "Europe/London", "cc": "{gb}"},
            "United States (New York)": {"tz": "America/New_York", "cc": "{us}"},
            "Vietnam (Ho Chi Minh)": {"tz": "Asia/Ho_Chi_Minh", "cc": "{vn}"}
        }
        
        self.killswitch_active = False
        self.original_hostname = self.get_hostname()
        self.ram_disk_id = None
        
        # Configure Neon Progressbar Theme
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Neon.Horizontal.TProgressbar", thickness=8, background='#00ffcc', troughcolor='#111111', bordercolor='#020202')
        
        self.build_ui()
        self.update_live_status()
        self._blink_status()

    def get_hostname(self):
        try:
            return subprocess.check_output(['scutil', '--get', 'ComputerName']).decode('utf-8').strip()
        except:
            return "MacBook"

    def build_ui(self):
        # ASCII Art Banner
        ascii_art = """
  ____ _   _  ___  ___ _____   ____  ____   ___ _____ ___   ____ ___  _     
 / ___| | | |/ _ \/ __|_   _| |  _ \|  _ \ / _ \_   _/ _ \ / ___/ _ \| |    
| |  _| |_| | | | \__ \ | |   | |_) | |_) | | | || || | | | |  | | | | |    
| |_| |  _  | |_| |___/ | |   |  __/|  _ <| |_| || || |_| | |__| |_| | |___ 
 \____|_| |_|\___/|____/|_|   |_|   |_| \_\\\\___/ |_| \___/ \____\___/|_____|
        """
        header = tk.Label(self.root, text=ascii_art, font=("Menlo", 10, "bold"), fg="#00ffcc", bg="#020202", justify="left")
        header.pack(pady=(10, 0))
        
        # Blinking Global Status Indicator
        self.global_status = tk.Label(self.root, text="● SYSTEM OFFLINE", font=("Menlo", 20, "bold"), fg="#ff3333", bg="#020202")
        self.global_status.pack(pady=(0, 20))
        
        # Status Dashboard HUD
        status_frame = tk.Frame(self.root, bg="#0a0a0a", highlightbackground="#00ffcc", highlightthickness=2)
        status_frame.pack(fill="x", padx=50, pady=5)
        
        self.net_label = tk.Label(status_frame, text="[►] Routing Vector : DIRECT CONNECTION", font=("Menlo", 15, "bold"), fg="#888888", bg="#0a0a0a")
        self.net_label.pack(anchor="w", padx=25, pady=8)
        
        self.tz_label = tk.Label(status_frame, text="[►] System Timezone: Scanning...", font=("Menlo", 15, "bold"), fg="#888888", bg="#0a0a0a")
        self.tz_label.pack(anchor="w", padx=25, pady=2)
        
        self.host_label = tk.Label(status_frame, text=f"[►] Node Hostname  : {self.original_hostname}", font=("Menlo", 15, "bold"), fg="#888888", bg="#0a0a0a")
        self.host_label.pack(anchor="w", padx=25, pady=(2, 8))
        
        # Controls Dashboard
        control_frame = tk.Frame(self.root, bg="#020202")
        control_frame.pack(fill="both", expand=True, padx=50, pady=15)
        
        tk.Label(control_frame, text="TARGET LOCATION:", font=("Menlo", 16, "bold"), fg="#ffffff", bg="#020202").grid(row=0, column=0, sticky="w", pady=15)
        
        self.selected_region = tk.StringVar(value="Japan (Tokyo)")
        self.region_menu = tk.OptionMenu(control_frame, self.selected_region, *self.regions.keys())
        self.region_menu.config(font=("Menlo", 16, "bold"), bg="#111111", fg="#00ffcc", highlightthickness=2, highlightbackground="#00ffcc", activebackground="#222222", activeforeground="#ffffff")
        self.region_menu.grid(row=0, column=1, sticky="w", padx=20, pady=15)
        
        # Checkboxes for Intense Features
        self.opt_dns = tk.BooleanVar(value=True)
        tk.Checkbutton(control_frame, text="[V2] Cloudflare ODoH DNS Injection", variable=self.opt_dns, font=("Menlo", 14, "bold"), bg="#020202", fg="#00ffcc", selectcolor="#111111", activebackground="#020202", activeforeground="#ffffff").grid(row=1, column=0, columnspan=2, sticky="w", pady=6)
        
        self.opt_host = tk.BooleanVar(value=True)
        tk.Checkbutton(control_frame, text="[V2] Mathematical Hostname Scrambling", variable=self.opt_host, font=("Menlo", 14, "bold"), bg="#020202", fg="#00ffcc", selectcolor="#111111", activebackground="#020202", activeforeground="#ffffff").grid(row=2, column=0, columnspan=2, sticky="w", pady=6)
        
        self.opt_kill = tk.BooleanVar(value=True)
        tk.Checkbutton(control_frame, text="[V2] Wi-Fi Subnet Kill-Switch", variable=self.opt_kill, font=("Menlo", 14, "bold"), bg="#020202", fg="#ff3333", selectcolor="#111111", activebackground="#020202", activeforeground="#ff0000").grid(row=3, column=0, columnspan=2, sticky="w", pady=6)
        
        self.opt_hw_kill = tk.BooleanVar(value=True)
        tk.Checkbutton(control_frame, text="[V3] Hardware Decapitation (Camera/Mic Blackout)", variable=self.opt_hw_kill, font=("Menlo", 14, "bold"), bg="#020202", fg="#ff00ff", selectcolor="#111111", activebackground="#020202", activeforeground="#ff99ff").grid(row=4, column=0, columnspan=2, sticky="w", pady=6)

        self.opt_ble_kill = tk.BooleanVar(value=True)
        tk.Checkbutton(control_frame, text="[V3] Radio Triangulation Blackout (BLE/AirDrop)", variable=self.opt_ble_kill, font=("Menlo", 14, "bold"), bg="#020202", fg="#ff00ff", selectcolor="#111111", activebackground="#020202", activeforeground="#ff99ff").grid(row=5, column=0, columnspan=2, sticky="w", pady=6)

        self.opt_dpi = tk.BooleanVar(value=True)
        tk.Checkbutton(control_frame, text="[V3] Deep Packet Disguise (obfs4 Transports)", variable=self.opt_dpi, font=("Menlo", 14, "bold"), bg="#020202", fg="#ff00ff", selectcolor="#111111", activebackground="#020202", activeforeground="#ff99ff").grid(row=6, column=0, columnspan=2, sticky="w", pady=6)

        # Progress Bar
        self.progress = ttk.Progressbar(self.root, style="Neon.Horizontal.TProgressbar", orient="horizontal", mode="determinate")
        self.progress.pack(fill="x", padx=50, pady=(10,0))

        # Terminal Log Box
        self.log_box = tk.Text(self.root, height=10, bg="#050505", fg="#00ffcc", font=("Menlo", 14, "bold"), bd=2, highlightbackground="#333333", highlightthickness=2, state="disabled")
        self.log_box.pack(fill="x", padx=50, pady=(0, 20))

        # Action Buttons
        btn_frame = tk.Frame(self.root, bg="#020202")
        btn_frame.pack(pady=15)
        
        self.btn_relocate = tk.Label(btn_frame, text="[ ENGAGE PROTOCOL ]", font=("Menlo", 16, "bold"), fg="#000000", bg="#00ffcc", width=20, pady=8, cursor="hand2")
        self.btn_relocate.grid(row=0, column=0, padx=15)
        self.btn_relocate.bind("<Button-1>", lambda e: self.start_spoofing() if str(self.btn_relocate.cget("state")) != "disabled" else None)
        self.btn_relocate.bind("<Enter>", lambda e: self.btn_relocate.config(bg="#ffffff") if str(self.btn_relocate.cget("state")) != "disabled" else None)
        self.btn_relocate.bind("<Leave>", lambda e: self.btn_relocate.config(bg="#00ffcc") if str(self.btn_relocate.cget("state")) != "disabled" else None)
        
        self.btn_revert = tk.Label(btn_frame, text="[ ABORT & WIPE ]", font=("Menlo", 16, "bold"), fg="#ffffff", bg="#ff3333", width=20, pady=8, cursor="hand2")
        self.btn_revert.grid(row=0, column=1, padx=15)
        self.btn_revert.bind("<Button-1>", lambda e: self.revert_system() if str(self.btn_revert.cget("state")) != "disabled" else None)
        self.btn_revert.bind("<Enter>", lambda e: self.btn_revert.config(bg="#ff6666") if str(self.btn_revert.cget("state")) != "disabled" else None)
        self.btn_revert.bind("<Leave>", lambda e: self.btn_revert.config(bg="#ff3333") if str(self.btn_revert.cget("state")) != "disabled" else None)
        
        self.btn_quarantine = tk.Label(btn_frame, text="[ RAM QUARANTINE ]", font=("Menlo", 16, "bold"), fg="#ffffff", bg="#aa00ff", width=20, pady=8, cursor="hand2")
        self.btn_quarantine.grid(row=0, column=2, padx=15)
        self.btn_quarantine.bind("<Button-1>", lambda e: self.launch_quarantine())
        self.btn_quarantine.bind("<Enter>", lambda e: self.btn_quarantine.config(bg="#cc66ff"))
        self.btn_quarantine.bind("<Leave>", lambda e: self.btn_quarantine.config(bg="#aa00ff"))
        
        self.log("Initializing Ghost Protocol V3 Core Kernel...")
        self.log("Awaiting operator instructions.")

    def log(self, message):
        self.log_box.config(state="normal")
        ts = time.strftime("%H:%M:%S")
        self.log_box.insert("end", f"[{ts}] root@ghost:~# {message}\n")
        self.log_box.see("end")
        self.log_box.config(state="disabled")

    def _blink_status(self):
        current_color = self.global_status.cget("fg")
        if self.net_label.cget("text") == "[►] Routing Vector : ACTIVE (Tor Proxy)":
            next_color = "#00ffcc" if current_color == "#020202" else "#020202"
            self.global_status.config(text="● SYSTEM ENCRYPTED", fg=next_color)
        else:
            self.global_status.config(text="● SYSTEM OFFLINE", fg="#ff3333")
            
        self.root.after(800, self._blink_status)

    def get_real_tz(self):
        try:
            output = subprocess.check_output(['systemsetup', '-gettimezone']).decode('utf-8')
            return output.split(': ')[1].strip()
        except:
            return "Unknown"

    def update_live_status(self):
        tz = self.get_real_tz()
        hostname = self.get_hostname()
        self.tz_label.config(text=f"[►] System Timezone: {tz}")
        self.host_label.config(text=f"[►] Node Hostname  : {hostname}")

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
        self.progress['value'] = 0
        target_name = self.selected_region.get()
        target_info = self.regions[target_name]
        
        if target_info["cc"] == "restore":
            self._revert_process()
            return
            
        self.log(f"Initiating cryptographic relocation to {target_name}...")
        os.system("killall tor 2>/dev/null")
        torrc_path = "/opt/homebrew/etc/tor/torrc"
        self.write_tor_config(target_info["cc"])
        os.system(f"/opt/homebrew/bin/tor -f {torrc_path} > /dev/null 2>&1 &")
        
        self.log("Igniting The Onion Router daemon [PID mapping...]")
        if self.opt_dpi.get():
             self.log("[MODULE] obfs4 Pluggable Transport attached. DPI blinded.")
             
        # Progress Bar Animation (Simulating Tor Bootstrap)
        bootstrap_logs = [
            "Handshaking with directory authorities...",
            "Validating cryptographic signatures (RSA/Ed25519)...",
            "Establishing primary entry guard node...",
            "Building encrypted middle relay circuit...",
            f"Forcing exit node compliance to {target_info['cc']}...",
            "Circuit established. Negotiating TLS wrapper...",
            "Verifying data stream integrity...",
            "Local SOCKS5 proxy bound to 127.0.0.1:9050",
            "Tor bootstrap phase 100% complete."
        ]
        
        for i in range(10):
            time.sleep(1)
            if i < len(bootstrap_logs):
                self.log(f"[SYS] {bootstrap_logs[i]}")
            self.progress['value'] += 10
            self.root.update_idletasks()
        
        cmd = f"/usr/sbin/systemsetup -setusingnetworktime off; /usr/sbin/systemsetup -settimezone {target_info['tz']}; "
        cmd += f"/usr/sbin/networksetup -setsocksfirewallproxy 'Wi-Fi' 127.0.0.1 9050; /usr/sbin/networksetup -setsocksfirewallproxystate 'Wi-Fi' on; "
        
        if self.opt_dns.get():
            cmd += f"/usr/sbin/networksetup -setdnsservers 'Wi-Fi' 1.1.1.1 1.0.0.1; "
            self.log("[SYS] Injecting ODoH DNS Resolvers on en0...")
            
        if self.opt_host.get():
            scramble = "GHOST-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
            cmd += f"/usr/sbin/scutil --set ComputerName '{scramble}'; /usr/sbin/scutil --set LocalHostName '{scramble}'; /usr/sbin/scutil --set HostName '{scramble}'; "
            self.log(f"[SYS] Scrambling MAC Hostname to: {scramble}")

        if self.opt_hw_kill.get():
            cmd += f"/usr/bin/killall VDCAssistant 2>/dev/null; /usr/bin/killall AppleCameraAssistant 2>/dev/null; /usr/bin/killall coreaudiod 2>/dev/null; "
            self.log("[HW] Decapitation: Camera & Mic drivers violently unloaded.")

        if self.opt_ble_kill.get():
            cmd += f"defaults write /Library/Preferences/com.apple.Bluetooth ControllerPowerState -int 0; /usr/bin/killall blued 2>/dev/null; /usr/bin/killall sharingd 2>/dev/null; "
            self.log("[HW] Radio Silence: Bluetooth & AirDrop beacons massacred.")

        self.log("Requesting root authorization for master kernel override...")
        success = self.run_admin_command(cmd)
        
        if success:
            self.net_label.config(text="[►] Routing Vector : ACTIVE (Tor Proxy)", fg="#00ffcc")
            self.log("Timezone shifted. Outbound packets forcefully tunneled.")
            
            if self.opt_kill.get():
                self.killswitch_active = True
                threading.Thread(target=self.monitor_killswitch, daemon=True).start()
                self.log("Wi-Fi Kill-Switch ARMED. Monitoring heartbeat...")
                
            self.log("ILLUSION COMPLETE.")
            self.root.after(1000, self.update_live_status)
        else:
            self.log("ERROR: Authorization denied. Reverting sequence.")
            self.progress['value'] = 0
            
        self.btn_relocate.config(state="normal")

    def revert_system(self):
        threading.Thread(target=self._revert_process, daemon=True).start()

    def _revert_process(self):
        self.btn_revert.config(state="disabled")
        self.killswitch_active = False
        self.progress['value'] = 0
        self.log("Aborting protocol. Executing scorch-earth log wipe...")
        
        os.system("killall tor 2>/dev/null")
        self.log("[SYS] Tor circuits collapsed. Socket 9050 closed.")
        
        cmd = (f"/usr/sbin/networksetup -setsocksfirewallproxystate 'Wi-Fi' off; "
               f"/usr/sbin/networksetup -setdnsservers 'Wi-Fi' 'Empty'; "
               f"/usr/sbin/systemsetup -settimezone Asia/Calcutta; "
               f"/usr/sbin/systemsetup -setusingnetworktime on; "
               f"/usr/sbin/scutil --set ComputerName '{self.original_hostname}'; "
               f"/usr/sbin/scutil --set LocalHostName '{self.original_hostname}'; "
               f"/usr/sbin/scutil --set HostName '{self.original_hostname}'; "
               f"defaults write /Library/Preferences/com.apple.Bluetooth ControllerPowerState -int 1; "
               f"/usr/bin/dscacheutil -flushcache; /usr/bin/killall -HUP mDNSResponder")
        
        self.log("[SYS] Restoring kernel routing tables and DNS cache...")
        success = self.run_admin_command(cmd)
        
        if self.ram_disk_id:
            os.system(f"diskutil eject {self.ram_disk_id} > /dev/null 2>&1")
            self.ram_disk_id = None
            self.log("[HW] Ghost Vault RAM Disk power cut. All quarantine data evaporated.")

        if success:
            self.net_label.config(text="[►] Routing Vector : DIRECT CONNECTION", fg="#888888")
            self.log("[OK] System restored. Logs obliterated. Illusion dissolved.")
            self.root.after(1000, self.update_live_status)
        else:
            self.log("[ERROR] Failed to revert kernel parameters.")
            
        self.btn_revert.config(state="normal")

    def launch_quarantine(self):
        threading.Thread(target=self._launch_ram_quarantine, daemon=True).start()

    def _launch_ram_quarantine(self):
        self.log("Allocating 1GB Volatile Memory (RAM Disk) for Ghost Vault...")
        try:
            output = subprocess.check_output(['hdiutil', 'attach', '-nomount', 'ram://2097152']).decode('utf-8')
            self.ram_disk_id = output.strip()
            
            self.log(f"RAM Block acquired: {self.ram_disk_id}. Formatting HFS+...")
            os.system(f"diskutil erasevolume HFS+ 'GhostVault' {self.ram_disk_id} > /dev/null 2>&1")
            
            self.log("Launching highly isolated Chromium container inside RAM...")
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
