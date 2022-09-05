from ppadb.client import Client as AdbClient
import time, tempfile, shutil

def run(NEW_SSID, NEW_PSK):
    dirpath = tempfile.mkdtemp()
    # print(dirpath)

    client = AdbClient(host="127.0.0.1", port=5037)
    device = client.devices()[0]
    device.shell("su -c 'svc wifi disable'")
    device.pull("/data/misc/wifi/wpa_supplicant.conf", dirpath+"/wpa_supplicant.conf")

    lines = []
    with open(dirpath+"/wpa_supplicant.conf", "r") as f:
        while True:
            line = f.readline()
            if line != "":
                if 'ssid="' in line:
                    lines.append('	ssid="'+NEW_SSID+'"\n')
                elif 'psk="' in line:
                    lines.append('	psk="'+NEW_PSK+'"\n')
                else:
                    lines.append(line)
            else:
                break
    with open(dirpath+"/wpa_supplicant.conf", "w") as f:
        for l in lines:
            f.write(l)
         
    time.sleep(1)
    device.push(dirpath+"/wpa_supplicant.conf", "/data/misc/wifi/wpa_supplicant.conf")
    time.sleep(1)
    device.shell("su -c 'svc wifi enable'")

    shutil.rmtree(dirpath)
    print("Done.")
    
if __name__ == "__main__":
    run(login, password)