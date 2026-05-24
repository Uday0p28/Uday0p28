import subprocess
import platform
import re
import shutil
import sys

def get_windows_profiles():
    if shutil.which('netsh') is None:
        return None
    out = subprocess.check_output(['netsh','wlan','show','profile']).decode('utf-8', errors='ignore').splitlines()
    profiles = [i.split(":",1)[1].strip() for i in out if "All User Profile" in i]
    results = []
    for p in profiles:
        try:
            res = subprocess.check_output(['netsh','wlan','show','profile',p,'key=clear']).decode('utf-8', errors='ignore').splitlines()
        except subprocess.CalledProcessError:
            res = []
        pw = [b.split(":",1)[1].strip() for b in res if "Key Content" in b]
        results.append((p, pw[0] if pw else ""))
    return results

def get_macos_interface():
    try:
        out = subprocess.check_output(['networksetup','-listallhardwareports']).decode(errors='ignore')
    except Exception:
        return 'en0'
    matches = re.findall(r'Hardware Port: (.+?)\nDevice: (en\d+)', out)
    iface = None
    for port, dev in matches:
        if port.lower() in ('wi-fi', 'wifi', 'airport'):
            iface = dev
            break
    if not iface and matches:
        iface = matches[0][1]
    return iface or 'en0'

def get_macos_profiles(iface):
    try:
        out = subprocess.check_output(['networksetup','-listpreferredwirelessnetworks', iface], stderr=subprocess.DEVNULL).decode(errors='ignore').splitlines()
    except subprocess.CalledProcessError:
        return []
    ssids = []
    for line in out[1:]:
        ssid = line.strip()
        if ssid:
            ssids.append(ssid)
    return ssids

def get_password_for_ssid_macos(ssid):
    try:
        proc = subprocess.run(['security','find-generic-password','-D','AirPort network password','-ga', ssid], capture_output=True, text=True)
        text = (proc.stderr or '') + '\n' + (proc.stdout or '')
        m = re.search(r'password: "([^"]+)"', text)
        if m:
            return m.group(1)
        m2 = re.search(r'password: (.+)', text)
        if m2:
            return m2.group(1).strip()
    except Exception:
        pass
    return ""

def main():
    if platform.system() == 'Windows' or shutil.which('netsh'):
        results = get_windows_profiles()
        if results is None:
            print("No netsh available")
            sys.exit(1)
        for ssid, pw in results:
            print("{:<30}| {:<}".format(ssid, pw))
    elif platform.system() == 'Darwin':
        iface = get_macos_interface()
        ssids = get_macos_profiles(iface)
        for ssid in ssids:
            pw = get_password_for_ssid_macos(ssid)
            print("{:<30}| {:<}".format(ssid, pw))
    else:
        print("Unsupported OS")
        sys.exit(1)

if __name__ == '__main__':
    main()