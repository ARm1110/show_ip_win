import sys
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap
import requests
from bs4 import BeautifulSoup
import time
def get_public_ip():
    try:
        response = requests.get('https://httpbin.org/ip')
        public_ip = response.json()['origin']
        return public_ip
    except requests.RequestException:
        return "Error: Could not fetch IP."

def show_ip():
    ip = get_public_ip()
    # Create a message box
    msgBox = QMessageBox()
    msgBox.setWindowTitle("Public IP Address")
    msgBox.setText(f"Your Public IP Address is: {ip}")
    # Set a custom icon
    time.sleep(5)
    prosescustom()
    custom_icon = QPixmap("./image.svg")  # Update the path to your custom image
    msgBox.setIconPixmap(custom_icon.scaled(64, 64))  # Scale the image to a suitable size
    msgBox.exec_()


def get_flag_image_url():
    try:
        response = requests.get('https://2ip.io/')
        soup = BeautifulSoup(response.content, 'html.parser')
        flag_div = soup.find('div', {'id': 'ip-info-country'})  # Assuming this exists
        if flag_div:
            style = flag_div.get('style', '')
            url_start = style.find("url('") + 5
            url_end = style.find("');", url_start)
            flag_url = 'https://2ip.io' + style[url_start:url_end] if style[url_start:url_end].startswith('/') else style[url_start:url_end]
            return flag_url
        else:
            raise ValueError("Flag element not found")
    except Exception as e:
        print(e)
        return None

def download_file(url, filename):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Open the file in binary write mode and write the response content to it
            with open(filename, 'wb') as file:
                file.write(response.content)
            print(f"File downloaded successfully as '{filename}'")
        else:
            print(f"Failed to download file: HTTP status code {response.status_code}")
    except Exception as e:
        print(f"Error downloading file: {e}")

def prosescustom():
    url = get_flag_image_url()  # URL of the file to download
    filename = 'image.svg'  # Name of the file to save locally
    download_file(url, filename)


app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)

# Create the icon (ensure this path correctly points to your icon file)
icon = QIcon("./skull.png")

# Create the tray
tray = QSystemTrayIcon()
tray.setIcon(icon)
tray.setVisible(True)

# Create the menu
menu = QMenu()
action = menu.addAction("Show Public IP")
action.triggered.connect(show_ip)
menu.addSeparator()
quit_action = menu.addAction("Exit")
quit_action.triggered.connect(app.quit)

# Add the menu to the tray
tray.setContextMenu(menu)

app.exec_()
