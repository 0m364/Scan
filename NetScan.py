import subprocess
import time

def get_devices():
    """Returns a list of all devices on the network."""
    output = subprocess.check_output(["arp", "-a"]).decode("utf-8")
    devices = {}
    for line in output.splitlines():
        if "dynamic" in line:
            ip = line.split()[1].strip('()')
            mac = line.split()[3]
            devices[mac] = ip
    return devices

def write_to_log(device, ip, connection_time):
    """Writes the device, its IP, and connection time to a log file."""
    with open("devices.log", "a") as f:
        f.write(f"Device {device} with IP {ip} connected at {connection_time}\n")

if __name__ == "__main__":
    known_devices = get_devices()
    while True:
        devices = get_devices()
        for device, ip in devices.items():
            if device not in known_devices:
                print(f"New device {device} with IP {ip} connected.")
                write_to_log(device, ip, time.ctime())
                known_devices[device] = ip
        time.sleep(60)  # wait a minute before scanning the network again
