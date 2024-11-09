from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import subprocess
import time
import pyautogui
import AppOpener
from mss import mss
import comtypes.stream 
import comtypes
import pywinauto
import tkinter as tk
import os
from twilio.rest import Client
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



SSH_Client = paramiko.SSHClient()
sftp_client = None
root = tk.Tk()
root.geometry("400x400")
root.resizable(0, 0)
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)


networkConnectedVar = tk.BooleanVar()
networkConnectedVar.set(False)
sftpConnectedVar = tk.BooleanVar()
sftpConnectedVar.set(False)



# labels vals
connectionStatusVal = tk.StringVar()
connectionStatusVal.set("booting up")
ImageStatusVal = tk.StringVar()
ImageStatusVal.set("-1/3")
nameVal = tk.StringVar()
networkStatusLabelVal = tk.StringVar()
networkStatusLabelVal.set("Network Offline")



# lables
connectionStatusLabelDyno = tk.Label(root, textvariable=connectionStatusVal)
networkStatusLabelDyno = tk.Label(root, textvariable=networkStatusLabelVal)
networkStatusLabelDyno.grid(column=1, row=0, sticky=tk.W)
connectionStatusLabel = tk.Label(root, text="connection : ")
connectionStatusLabel.grid(column=0, row=0, sticky=tk.W)
connectionStatusLabelDyno.grid(column=2, row=0, sticky=tk.W)
imageStatusLabelDyno = tk.Label(root, textvariable=ImageStatusVal)
imageStatusLabel = tk.Label(root, text="progress : ")
imageStatusLabel.grid(column=0, row=1, sticky=tk.W)
imageStatusLabelDyno.grid(column=2, row=1, sticky=tk.W)
NameLabel = tk.Label(root, text="name :")
NameLabel.grid(column=0, row=2, sticky=tk.W)



nameEntry = tk.Entry(root,width=10, textvariable=nameVal)
nameEntry.grid(column=2, row=2, sticky=tk.W)

## am connected to network test
def isConnectedToNetwork():
    while (True):
        time.sleep(1)
        networkStatusLabelDyno.config(bg="grey")
        try:
            # connect to the host -- tells us if the host is actually
            # reachable
            socket.create_connection(("1.1.1.1", 53))
            networkStatusLabelVal.set("Network Online")
            networkStatusLabelDyno.config(bg="green")
            networkConnectedVar.set(True)
        except OSError:
            pass
            networkConnectedVar.set(False)
            networkStatusLabelVal.set("Network Offline")
            networkStatusLabelDyno.config(bg="red")

def isConnectedToSFTP():
    while (True):
        time.sleep(1)
        global sftp_client
        try:
            sftp_client.listdir()
            connectionStatusVal.set("SFTP Connected")
            connectionStatusLabelDyno.config(bg="green")
            sftpConnectedVar.set(True)
        except Exception as e:
            print(e)
            connectionStatusVal.set("SFTP Failed")
            connectionStatusLabelDyno.config(bg="red")
            sftpConnectedVar.set(False)
            connectToSftp()


def connectToSftp():
    print("attempt SFTP connect")
    connectionStatusVal.set("attempting to connect")
    global SSH_Client
    SSH_Client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        SSH_Client.connect(hostname=hostname,
                        port=port,
                        username=username)
        global sftp_client 
        sftp_client = SSH_Client.open_sftp()
        connectionStatusVal.set("SFTP Connected")
        connectionStatusLabelDyno.config(bg="green")
        print("SFTP connect Succeeded")
    except Exception as e :
        print("SFTP connect FAILED")
        print(e)
        connectionStatusVal.set("SFTP Failed")
        connectionStatusLabelDyno.config(bg="red")

def uploadFiles():
    dirName = nameVal.get() + " " + strftime("%d %b %Y %H:%M:%S", gmtime())
    
    print(f"attempting to make {dirName}")
    try: 
        sftp_client.mkdir("speedtest/"+dirName)
        ImageStatusVal.set("0/3")
    except FileNotFoundError as err:
        print(f"Could not make {dirName} could not be made")
    except Exception as e:
        print("unhandled exception")
        print(e)

    print(f"attempting to upload broadband.png")
    localFilePath = "broadband.png"
    remoteFilePath = "speedtest/"+dirName+"/broadband.png"
    try:
        sftp_client.put(localFilePath, remoteFilePath)
        ImageStatusVal.set("1/3")
    except FileNotFoundError as err:
        print(f"File {localFilePath} was not found on the local system")
    except Exception as e:
        print("unhandled exception")
        print(e)


    print(f"attempting to upload sonic.png")
    localFilePath = "sonic.png"
    remoteFilePath = "speedtest/"+dirName+"/sonic.png"
    try:
        sftp_client.put(localFilePath, remoteFilePath)
        ImageStatusVal.set("2/3")
    except FileNotFoundError as err:
        print(f"File {localFilePath} was not found on the local system")
    except Exception as e:
        print("unhandled exception")
        print(e)


    print(f"attempting to upload pcmag.png")
    localFilePath = "pcmag.png"
    remoteFilePath = "speedtest/"+dirName+"/pcmag.png"
    try:
        sftp_client.put(localFilePath, remoteFilePath)
        ImageStatusVal.set("3/3")
    except FileNotFoundError as err:
        print(f"File {localFilePath} was not found on the local system")
    except Exception as e:
        print("unhandled exception")
        print(e)

def button_clicked():
    speedTest()
    connect()
    uploadFiles()

def speedTest():


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


def testAndUploadWhenReady():
    speedTestWhenReady()
    upploadWhenReady()

def startTestAndUploadThread():
    fullbtn.config(state=tk.DISABLED, bg="grey",text="awaiting network")
    fullbtn.config()
    testAndUploadDaemon = threading.Thread(target=testAndUploadWhenReady)
    testAndUploadDaemon.daemon = True
    testAndUploadDaemon.start()  


def speedTestWhenReady():
    while (True):
        if (networkConnectedVar.get()):
            print("network up starting speedtest")
            speedTest()
            return
    
def upploadWhenReady():
    while (True):
        if (sftpConnectedVar.get()):
            print("sftp up starting speedtest")
            uploadFiles()
            return

# Creating a button with specified options
fullbtn = tk.Button(root, 
                   text="Test when ready", 
                   command=startTestAndUploadThread,
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
fullbtn.grid(column=0,row=3, columnspan=3, pady=10)

speedTestBtn = tk.Button(root, 
                   text="Test speed", 
                   command=speedTest,
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
speedTestBtn.grid(row=4,column=0)

uploadbtn = tk.Button(root, 
                   text="upload", 
                   command=uploadFiles,
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
uploadbtn.grid(row=4,column=2)


connectbtn = tk.Button(root, 
                   text="connect", 
                   command=connectToSftp,
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
connectbtn.grid(row=4,column=1)

connectionStatusVal.set("SFTP offline")
connectionStatusLabelDyno.config(bg="red")
# Start the event loop.


networkDaemon = threading.Thread(target=isConnectedToNetwork)
networkDaemon.daemon = True
networkDaemon.start()  

sftpDaemon = threading.Thread(target=isConnectedToSFTP)
sftpDaemon.daemon = True
sftpDaemon.start() 


testAndUploadWhenReady

root.mainloop()


