from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import AppOpener
from mss import mss
import pywinauto
import tkinter as tk
import paramiko
from time import gmtime, strftime
import socket
import threading
from selenium.webdriver.chrome.options import Options
import json



# load in git unsafe secreats 
with open("secrets.json") as f:
    secretsJson = json.load(f)
    hostname = secretsJson["hostname"]
    username = secretsJson["username"]
    port = secretsJson["port"]



ssh_client = paramiko.SSHClient()
sftp_client = None
root = tk.Tk()
root.geometry("400x400")
root.resizable(0, 0)
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)


network_status = tk.BooleanVar()
network_status.set(False)
sftp_status = tk.BooleanVar()
sftp_status.set(False)



# labels vals
connection_status_labal_variable = tk.StringVar()
connection_status_labal_variable.set("booting up")
upload_status_label_variable = tk.StringVar()
upload_status_label_variable.set("-1/3")
username_entry_variable = tk.StringVar()
network_status_label_variable = tk.StringVar()
network_status_label_variable.set("Network Offline")



# lables
sftp_status_dynamic_label = tk.Label(root, textvariable=connection_status_labal_variable)
network_status_dynamic_label = tk.Label(root, textvariable=network_status_label_variable)
network_status_dynamic_label.grid(column=1, row=0, sticky=tk.W)
sftp_status_static_label = tk.Label(root, text="connection : ")
sftp_status_static_label.grid(column=0, row=0, sticky=tk.W)
sftp_status_dynamic_label.grid(column=2, row=0, sticky=tk.W)
upload_status_dynamic_label = tk.Label(root, textvariable=upload_status_label_variable)
upload_status_static_label = tk.Label(root, text="progress : ")
upload_status_static_label.grid(column=0, row=1, sticky=tk.W)
upload_status_dynamic_label.grid(column=2, row=1, sticky=tk.W)
username_static_label = tk.Label(root, text="name :")
username_static_label.grid(column=0, row=2, sticky=tk.W)



username_entry = tk.Entry(root,width=10, textvariable=username_entry_variable)
username_entry.grid(column=2, row=2, sticky=tk.W)

## am connected to network test
def check_internet_connection():
    while (True):
        time.sleep(1)
        network_status_dynamic_label.config(bg="grey")
        try:
            # connect to the host -- tells us if the host is actually
            # reachable
            socket.create_connection(("1.1.1.1", 53))
            network_status_label_variable.set("Network Online")
            network_status_dynamic_label.config(bg="green")
            network_status.set(True)
        except OSError:
            pass
            network_status.set(False)
            network_status_label_variable.set("Network Offline")
            network_status_dynamic_label.config(bg="red")

def check_sftp_connection():
    connect_to_sftp()
    while (True):
        time.sleep(1)
        print("attempt SFTP connect")
        try:
            transport = ssh_client.get_transport()
            transport.send_ignore()

            connection_status_labal_variable.set("SFTP Connected")
            sftp_status_dynamic_label.config(bg="green")
            sftp_status.set(True)
        except EOFError as e:
            print(e)
            connection_status_labal_variable.set("SFTP Failed")
            sftp_status_dynamic_label.config(bg="red")
            sftp_status.set(False)
            connect_to_sftp()


def connect_to_sftp():
    connection_status_labal_variable.set("attempting to connect")
    global ssh_client
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh_client.connect(hostname=hostname,
                        port=port,
                        username=username)
        global sftp_client 
        sftp_client = ssh_client.open_sftp()
        connection_status_labal_variable.set("SFTP Connected")
        sftp_status_dynamic_label.config(bg="green")
        print("SFTP connect Succeeded")
    except Exception as e :
        print("SFTP connect FAILED")
        print(e)
        connection_status_labal_variable.set("SFTP Failed")
        sftp_status_dynamic_label.config(bg="red")

def upload_images():
    dirName = username_entry_variable.get() + " " + strftime("%d %b %Y %H:%M:%S", gmtime())
    
    print(f"attempting to make {dirName}")
    try: 
        sftp_client.mkdir("speedtest/"+dirName)
        upload_status_label_variable.set("0/3")
    except FileNotFoundError as err:
        print(f"Could not make {dirName} could not be made")
    except Exception as e:
        print("unhandled exception")
        print(e)

    print("attempting to upload broadband.png")
    localFilePath = "broadband.png"
    remoteFilePath = "speedtest/"+dirName+"/broadband.png"
    try:
        sftp_client.put(localFilePath, remoteFilePath)
        upload_status_label_variable.set("1/3")
    except FileNotFoundError as err:
        print(f"File {localFilePath} was not found on the local system")
    except Exception as e:
        print("unhandled exception")
        print(e)


    print("attempting to upload sonic.png")
    localFilePath = "sonic.png"
    remoteFilePath = "speedtest/"+dirName+"/sonic.png"
    try:
        sftp_client.put(localFilePath, remoteFilePath)
        upload_status_label_variable.set("2/3")
    except FileNotFoundError as err:
        print(f"File {localFilePath} was not found on the local system")
    except Exception as e:
        print("unhandled exception")
        print(e)


    print("attempting to upload pcmag.png")
    localFilePath = "pcmag.png"
    remoteFilePath = "speedtest/"+dirName+"/pcmag.png"
    try:
        sftp_client.put(localFilePath, remoteFilePath)
        upload_status_label_variable.set("3/3")
    except FileNotFoundError as err:
        print(f"File {localFilePath} was not found on the local system")
    except Exception as e:
        print("unhandled exception")
        print(e)

def test_internet_speed_and_upload():
    test_internet_speeds()
    upload_images()

def test_internet_speeds():


    AppOpener.open("Speedtest") # Opens app
    time.sleep(5)
    pywinauto.mouse.click(coords=(1200, 300))
    time.sleep(1)
    pywinauto.mouse.click(coords=(1200, 300))
    time.sleep(40)


    chrome_options = Options()
    chrome_options.add_argument("--window-size=640,1080")
    driver = webdriver.Chrome(chrome_options)
    driver.get("https://pcmag.speedtestcustom.com")
    time.sleep(5)
    btn = driver.find_element(by=By.CSS_SELECTOR, value="button")
    btn.click()

    time.sleep(40)
    with mss() as sct:
        for filename in sct.save(output="pcmag.png"):
            print(filename)

    print("PC mag test Done")
    time.sleep(5)

    driver.get("https://sonic.speedtestcustom.com")
    btn = driver.find_element(by=By.CSS_SELECTOR, value="button")
    btn.click()
    time.sleep(40)
    with mss() as sct:
        for filename in sct.save(output="sonic.png"):
            print(filename)
    print("sonic speed test done")
    time.sleep(5)

    driver.get("https://broadbandnow.com/speedtest")
    btns = driver.find_elements(by=By.CSS_SELECTOR, value="button")
    btns[3].click()
    time.sleep(40)
    with mss() as sct:
        for filename in sct.save(output="broadband.png"):
            print(filename)
    print("broadband speed test done")

def test_and_upload_when_ready():
    speed_test_when_ready()
    upload_images_when_ready()

def start_speed_test_and_upload_as_thread():
    test_and_upload_when_ready_button.config(state=tk.DISABLED, bg="grey",text="awaiting network")
    test_and_upload_when_ready_button.config()
    testAndUploadDaemon = threading.Thread(target=test_and_upload_when_ready)
    testAndUploadDaemon.daemon = True
    testAndUploadDaemon.start()  

def speed_test_when_ready():
    while (True):
        if (network_status.get()):
            print("network up starting speedtest")
            test_internet_speeds()
            return
    
def upload_images_when_ready():
    while (True):
        if (sftp_status.get()):
            print("sftp up starting speedtest")
            upload_images()
            return

# Creating a button with specified options
test_and_upload_when_ready_button = tk.Button(root, 
                   text="Test when ready", 
                   command=start_speed_test_and_upload_as_thread,
                   activebackground="blue", 
                   activeforeground="white",
                   anchor="center",
                   bd=3,
                   bg="red",
                   cursor="hand2",
                   disabledforeground="white",
                   fg="black",
                   font=("Arial", 12),
                   height=2,
                   highlightbackground="black",
                   highlightcolor="green",
                   highlightthickness=2,
                   justify="center",
                   overrelief="raised",
                   pady=5,
                   width=12,
                   wraplength=100)
test_and_upload_when_ready_button.grid(column=0,row=3, columnspan=3, pady=10)

speed_test_button = tk.Button(root, 
                   text="Test speed", 
                   command=test_internet_speeds,
                   activebackground="blue", 
                   activeforeground="white",
                   anchor="center",
                   bd=3,
                   bg="lightgrey",
                   cursor="hand2",
                   disabledforeground="gray",
                   fg="black",
                   font=("Arial", 12),
                   height=2,
                   highlightbackground="black",
                   highlightcolor="green",
                   highlightthickness=2,
                   justify="center",
                   overrelief="raised",
                   pady=5,
                   width=8,
                   wraplength=100)
speed_test_button.grid(row=4,column=0)

upload_button = tk.Button(root, 
                   text="upload", 
                   command=upload_images,
                   activebackground="blue", 
                   activeforeground="white",
                   anchor="center",
                   bd=3,
                   bg="lightgrey",
                   cursor="hand2",
                   disabledforeground="gray",
                   fg="black",
                   font=("Arial", 12),
                   height=2,
                   highlightbackground="black",
                   highlightcolor="green",
                   highlightthickness=2,
                   justify="center",
                   overrelief="raised",
                   pady=5,
                   width=8,
                   wraplength=100)
upload_button.grid(row=4,column=2)


sftp_connect_button = tk.Button(root, 
                   text="connect", 
                   command=connect_to_sftp,
                   activebackground="blue", 
                   activeforeground="white",
                   anchor="center",
                   bd=3,
                   bg="lightgrey",
                   cursor="hand2",
                   disabledforeground="gray",
                   fg="black",
                   font=("Arial", 12),
                   height=2,
                   highlightbackground="black",
                   highlightcolor="green",
                   highlightthickness=2,
                   justify="center",
                   overrelief="raised",
                   pady=5,
                   width=8,
                   wraplength=100)
sftp_connect_button.grid(row=4,column=1)

connection_status_labal_variable.set("SFTP offline")
sftp_status_dynamic_label.config(bg="red")
# Start the event loop.


network_daemon = threading.Thread(target=check_internet_connection)
network_daemon.daemon = True
network_daemon.start()  

sftp_daemon = threading.Thread(target=check_sftp_connection)
sftp_daemon.daemon = True
sftp_daemon.start() 



root.mainloop()


