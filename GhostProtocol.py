import tkinter as tk
from tkinter import messagebox
import subprocess
import threading
import time
import os

class GhostProtocolApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GHOST PROTOCOL (TOR ENABLED)")
        self.root.geometry("700x550")
        self.root.configure(bg="#050505")
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width / 2) - (700 / 2))
        y = int((screen_height / 2) - (550 / 2))
        self.root.geometry(f"700x550+{x}+{y}")
        
        self.regions = {
            "Tokyo, Japan": {"tz": "Asia/Tokyo", "cc": "{jp}"},
            "London, UK": {"tz": "Europe/London", "cc": "{gb}"},
            "New York, USA": {"tz": "America/New_York", "cc": "{us}"},
            "Frankfurt, Germany": {"tz": "Europe/Berlin", "cc": "{de}"},
            "Sydney, Australia": {"tz": "Australia/Sydney", "cc": "{au}"},
            "Original (Restore)": {"tz": "Asia/Calcutta", "cc": "restore"}
        }
        
        self.build_ui()
        self.update_live_status()

    def build_ui(self):
        header = tk.Label(self.root, text="GHOST PROTOCOL : DIGITAL RELOCATION", 
                          font=("Courier", 18, "bold"), fg="#00ffcc", bg="#050505")
        header.pack(pady=20)
        
        status_frame = tk.Frame(self.root, bg="#111111", highlightbackground="#333333", highlightthickness=1)
        status_frame.pack(fill="x", padx=30, pady=10)
        
        self.mac_label = tk.Label(status_frame, text="Network Spoofing: Offline", font=("Courier", 12), fg="#aaaaaa", bg="#111111")
        self.mac_label.pack(anchor="w", padx=20, pady=10)
        
        self.tz_label = tk.Label(status_frame, text="Current Timezone: Scanning...", font=("Courier", 12), fg="#aaaaaa", bg="#111111")
        self.tz_label.pack(anchor="w", padx=20, pady=(0, 10))
        
        control_frame = tk.Frame(self.root, bg="#050505")
        control_frame.pack(fill="both", expand=True, padx=30, pady=10)
        
        tk.Label(control_frame, text="TARGET LOCATION:", font=("Courier", 12), fg="#ffffff", bg="#050505").grid(row=0, column=0, sticky="w", pady=10)
        
        self.selected_region = tk.StringVar(value="Tokyo, Japan")
        self.region_menu = tk.OptionMenu(control_frame, self.selected_region, *self.regions.keys())
        self.region_menu.config(font=("Courier", 12), bg="#222222", fg="#ffffff", highlightthickness=0)
        self.region_menu.grid(row=0, column=1, sticky="w", padx=20, pady=10)
        
        btn_frame = tk.Frame(self.root, bg="#050505")
        btn_frame.pack(pady=20)
        
        self.btn_relocate = tk.Button(btn_frame, text="INITIATE SPOOFING", font=("Courier", 14, "bold"), fg="#000000", bg="#00ffcc", 
                                      activebackground="#00ccaa", width=20, command=self.start_spoofing)
        self.btn_relocate.grid(row=0, column=0, padx=10)
        
        self.btn_revert = tk.Button(btn_frame, text="REVERT TO NORMAL", font=("Courier", 14, "bold"), fg="#ffffff", bg="#ff3333", 
                                    activebackground="#cc0000", width=20, command=self.revert_system)
        self.btn_revert.grid(row=0, column=1, padx=10)
        
        self.log_box = tk.Text(self.root, height=8, bg="#0a0a0a", fg="#00ffcc", font=("Courier", 10), bd=0, state="disabled")
        self.log_box.pack(fill="x", padx=30, pady=10)
        self.log("System initialized. Tor SOCKS5 Proxy Ready.")

    def log(self, message):
        self.log_box.config(state="normal")
        self.log_box.insert("end", f"[+] {message}\\n")
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
        self.tz_label.config(text=f"Current Timezone     : {tz}")

    def run_admin_command(self, cmd):
        apple_script = f'do shell script "{cmd}" with administrator privileges'
        try:
            subprocess.run(['osascript', '-e', apple_script], check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def write_tor_config(self, country_code):
        torrc_path = "/opt/homebrew/etc/tor/torrc"
        config = f"SocksPort 9050\nExitNodes {country_code}\nStrictNodes 1\n"
        with open(torrc_path, "w") as f:
            f.write(config)

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
        
        # 1. Kill any existing Tor
        os.system("killall tor 2>/dev/null")
        
        # 2. Configure Tor for strict exit node
        self.log(f"Programming Tor routing circuits for {target_info['cc']} exit...")
        self.write_tor_config(target_info["cc"])
        
        # 3. Start Tor in background
        os.system("/opt/homebrew/bin/tor > /dev/null 2>&1 &")
        self.log("Igniting The Onion Router. Circuit building... (Takes ~10 seconds)")
        time.sleep(3)
        
        # 4. Hijack System Timezone and proxy settings
        cmd = (f"/usr/sbin/systemsetup -setusingnetworktime off; "
               f"/usr/sbin/systemsetup -settimezone {target_info['tz']}; "
               f"/usr/sbin/networksetup -setsocksfirewallproxy \\\"Wi-Fi\\\" 127.0.0.1 9050; "
               f"/usr/sbin/networksetup -setsocksfirewallproxystate \\\"Wi-Fi\\\" on")
        
        self.log("Authenticating master system override...")
        success = self.run_admin_command(cmd)
        
        if success:
            self.mac_label.config(text="Network Spoofing: ACTIVE (Tor Proxy)", fg="#00ffcc")
            self.log(f"Timezone shifted. Wi-Fi traffic forced through Tor.")
            self.log("ILLUSION COMPLETE: Open your browser to test.")
            self.root.after(1000, self.update_live_status)
        else:
            self.log("ERROR: Permission denied.")
            
        self.btn_relocate.config(state="normal")

    def revert_system(self):
        threading.Thread(target=self._revert_process, daemon=True).start()

    def _revert_process(self):
        self.btn_revert.config(state="disabled")
        self.log("Dropping Tor circuits and reverting systems...")
        
        os.system("killall tor 2>/dev/null")
        
        cmd = (f"/usr/sbin/networksetup -setsocksfirewallproxystate \\\"Wi-Fi\\\" off; "
               f"/usr/sbin/systemsetup -settimezone Asia/Calcutta; "
               f"/usr/sbin/systemsetup -setusingnetworktime on")
        
        success = self.run_admin_command(cmd)
        
        if success:
            self.mac_label.config(text="Network Spoofing: Offline", fg="#aaaaaa")
            self.log("Proxy deactivated. Timezone synchronized to local.")
            self.root.after(1000, self.update_live_status)
        else:
            self.log("ERROR: Failed to revert.")
            
        self.btn_revert.config(state="normal")

if __name__ == "__main__":
    root = tk.Tk()
    app = GhostProtocolApp(root)
    root.lift()
    root.attributes('-topmost', True)
    root.after_idle(root.attributes, '-topmost', False)
    root.mainloop()
