import os
import socket
import subprocess
import requests
import fade
from colorama import Fore
import time
# Maintain a set to store queried IP addresses
queried_ips = set()


banner = """
                                   ____ _           _   ____            
                                  / ___| |__   __ _| |_|  _ \  _____  __
                                 | |   | '_ \ / _` | __| | | |/ _ \ \/ /
                                 | |___| | | | (_| | |_| |_| | (_) >  < 
                                  \____|_| |_|\__,_|\__|____/ \___/_/\_\
                                        




"""


w = Fore.WHITE
b = Fore.BLACK
g = Fore.LIGHTGREEN_EX
y = Fore.LIGHTYELLOW_EX
m = Fore.LIGHTMAGENTA_EX
c = Fore.LIGHTCYAN_EX
lr = Fore.LIGHTRED_EX
lb = Fore.LIGHTBLUE_EX
rd = Fore.RED

def clear_screen():
    print("\033[H\033[J")

def print_banner():
    clear_screen()
    faded_banner = fade.water(banner)
    print(faded_banner)

def menu():
    print_banner()
    while True:
        print_banner()
        menu_options = """
                                      
                                ╠══════════════════════════════════════════════╣                 
                                ║        [1] Scan              [2] Exit        ║            
                                ╚                                              ╝    
                         
                         """
        faded_menu = fade.water(menu_options)
        print(faded_menu)
        choice = input(f"\n{lb}Select an option: ").lower()
        if choice == "1" or choice == "scan":
            main()
        elif choice == "2" or choice == "exit":
            exit()
        elif choice == "" or choice == " ":
            pass
        else:
            input("Invalid choice. Press Enter to continue...")



def get_geolocation_info(ip):
    url = f"http://ipapi.co/{ip}/json"
    headers = {"User-Agent": "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        ip_address = data.get("ip", "Unknown")
        country = data.get("country_name", "Unknown")
        region = data.get("region", "Unknown")
        city = data.get("city", "Unknown")
        postal = data.get("postal", "Unknown")
        latitude = data.get("latitude", "Unknown")
        longitude = data.get("longitude", "Unknown")
        return ip_address, country, region, city, postal, latitude, longitude
    else:
        return None

def main():
    clear_screen()
    tshark_path = r"C:\Program Files\Wireshark\tshark.exe"
    if not os.path.exists(tshark_path):
        print("Wireshark (and tshark) is not found on this system.")
        print("Please install Wireshark from the following link:")
        print("https://www.wireshark.org/download.html")
        exit()

    # List available interfaces and prompt user to select one
    print("Available Interfaces:")
    interface_cmd = f'"{tshark_path}" --list-interfaces'
    interface_process = subprocess.Popen(interface_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    interface_output = interface_process.communicate()[0].decode('utf-8')
    interfaces = interface_output.splitlines()[1:]

    for interface in interfaces:
        print(interface)

    # Prompt user to choose an interface
    selected_interface = input("Enter the number of the interface to scan on: ")

    clear_screen()
    print(f"{lb}Scan starting...")
    time.sleep(1.5)
    print(f"{lb}Scan running...")
    cmd = f'"{tshark_path}" -i "{selected_interface}"'

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    my_ip = socket.gethostbyname(socket.gethostname())

    for line in iter(process.stdout.readline, b""):
        columns = str(line).split(" ")

        if "SKYPE" in columns or "UDP" in columns:
        
            # for different tshark versions
            if "->" in columns:
                src_ip = columns[columns.index("->") - 1]
            elif "\\xe2\\x86\\x92" in columns:
                src_ip = columns[columns.index("\\xe2\\x86\\x92") - 1]
            else:
                continue
            
            if src_ip == my_ip or src_ip in queried_ips:
                continue

            try:
                ip_address, country, region, city, postal, latitude, longitude = get_geolocation_info(src_ip)
                if ip_address:
                    print("IP Address:", ip_address)
                    print("Country:", country)
                    print("Region:", region)
                    print("City:", city)
                    print("Postal Code:", postal)
                    print("Latitude:", latitude)
                    print("Longitude:", longitude)
                    ipgeolocation = f'{latitude}+{longitude}'
                    print(f"URL: https://www.google.com/maps/search/{ipgeolocation}")
                    queried_ips.add(src_ip)
                else:
                    print("Not found")
            except:
                print("Not found")


if __name__ == "__main__":
    menu()
