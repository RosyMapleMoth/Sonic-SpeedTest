import requests
import time
import socket
import threading
import json
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import tkinter as tk
from time import gmtime, strftime
from mss import mss

# initalize api variables, these are loaded in from config via load_settings
hostname = None
port = None
mss().compression_level = 5

# initalize Tinker
WINDOW_HIGHT_CLOSED = 200
WINDOW_HIGHT_OPEN = 450
WINDOW_WIDTH = 300
root = tk.Tk()
root.geometry("%dx%d" % (WINDOW_WIDTH,WINDOW_HIGHT_CLOSED))
root.resizable(0, 0)
root.columnconfigure(0, weight=0)
root.columnconfigure(1, weight=100)
root.columnconfigure(2, weight=0)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)
root.rowconfigure(3, weight=3)
root.rowconfigure(4, weight=3)
root.rowconfigure(5, weight=3)
root.rowconfigure(6, weight=3)
root.rowconfigure(7, weight=3)
root.rowconfigure(8, weight=3)

# initalize network status
network_status = tk.BooleanVar()
network_status.set(False)
network_status_label_variable = tk.StringVar()
network_status_label_variable.set("Network Offline")
network_status_dynamic_label = tk.Label(root, textvariable=network_status_label_variable)
network_status_dynamic_label.grid(column=0, row=0, columnspan=3)

# initalize settings variables
username_entry_variable = tk.StringVar()
username_entry_label = tk.Label(root, text="name :", state="active", bg="green")
username_entry = tk.Entry(root, textvariable=username_entry_variable)

apikey_entry_variable = tk.StringVar()
apikey_entry_label = tk.Label(root, text="api key :",bg="green")
apikey_entry = tk.Entry(root, textvariable=apikey_entry_variable)

email_checkbox_variable = tk.BooleanVar()
email_checkbox = tk.Checkbutton(root,
                text='Email',
                variable=email_checkbox_variable)

discord_checkbox_variable = tk.BooleanVar()
discord_checkbox = tk.Checkbutton(root,
                text='Discord',
                variable=discord_checkbox_variable)

pcmag_checkbox_variable = tk.BooleanVar()
pcmag_checkbox = tk.Checkbutton(root,
                text='pcmag',
                variable=pcmag_checkbox_variable)

sonic_checkbox_variable = tk.BooleanVar()
sonic_checkbox = tk.Checkbutton(root,
                text='sonic',
                variable=sonic_checkbox_variable)

broadband_checkbox_variable = tk.BooleanVar()
broadband_checkbox = tk.Checkbutton(root,
                text='broadband',
                variable=broadband_checkbox_variable)

oakla_app_checkbox_variable = tk.BooleanVar()
oakla_app_checkbox = tk.Checkbutton(root,
                text='oakla app',
                variable=oakla_app_checkbox_variable)

oakla_web_checkbox_variable = tk.BooleanVar()
oakla_web_checkbox = tk.Checkbutton(root,
                text='oakla web',
                variable=oakla_web_checkbox_variable)

email_entry_variable = tk.StringVar()
email_entry_label = tk.Label(root, text="email :")
email_entry = tk.Entry(root, 
                       textvariable=email_entry_variable, 
                       state="readonly")

discord_entry_variable = tk.StringVar()
discord_entry_label = tk.Label(root, text="discord @ :")
discord_entry = tk.Entry(root, 
                         textvariable=email_entry_variable, 
                         state="readonly")


def open_new_win():
   top=tk.Toplevel(root)
   canvas1=tk.Canvas(root, height=100, width=100, bg="#aaaffe")
   top.geometry("100x100+%d+%d" % (x, y))
   top.attributes('-alpha',0.5)
   canvas1.pack()


def open_settings():
    root.geometry("%dx%d" % (WINDOW_WIDTH,WINDOW_HIGHT_OPEN))
    settings_button.config(text="close settings", command=close_settings)
    apikey_entry_label.config(state="active")

    email_entry_label.grid(column=0, row=7, sticky=tk.W)
    email_entry.grid(column=1, columnspan=3, row=7, sticky=tk.EW)
    discord_entry_label.grid(column=0, row=8, sticky=tk.W)
    discord_entry.grid(column=1, columnspan=3, row=8, sticky=tk.EW)
    username_entry_label.grid(column=0, row=6, sticky=tk.W)
    username_entry.grid(column=1, columnspan=2, row=6, sticky=tk.EW)
    apikey_entry_label.grid(column=0, row=5, sticky=tk.W)
    apikey_entry.grid(column=1, columnspan=3, row=5, sticky=tk.EW)

    broadband_checkbox.grid(column=0,  row=9)
    pcmag_checkbox.grid(column=1,row=9)
    sonic_checkbox.grid(column=2,  row=9, sticky=tk.W)
    oakla_app_checkbox.grid(column=0, row=10, sticky=tk.W)
    oakla_app_checkbox.config(state="disabled")
    oakla_web_checkbox.grid(column=2, row=10, sticky=tk.W)
    oakla_web_checkbox.config(state="disabled")
    email_checkbox.grid(column=0, row=13, sticky=tk.W)
    email_checkbox.config(state="disabled")
    discord_checkbox.grid(column=2, row=13, sticky=tk.W)
    save_button.grid(column=0, columnspan=3, row=14, pady=5, padx=5)


def close_settings():
    root.geometry("%dx%d" % (WINDOW_WIDTH,WINDOW_HIGHT_CLOSED))
    settings_button.config(text="open settings",
                           command=open_settings)

    email_entry_label.grid_forget()
    email_entry.grid_forget()
    discord_entry_label.grid_forget()
    discord_entry.grid_forget()
    username_entry_label.grid_forget()
    username_entry.grid_forget()
    apikey_entry_label.grid_forget()
    apikey_entry.grid_forget()
    broadband_checkbox.grid_forget()
    pcmag_checkbox.grid_forget()
    sonic_checkbox.grid_forget()
    oakla_app_checkbox.grid_forget()
    oakla_web_checkbox.grid_forget()
    save_button.grid_forget()
    email_checkbox.grid_forget()
    discord_checkbox.grid_forget()


# Checks if computer is connected to network and modifies network status appropriately
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
        except:
            network_status.set(False)
            network_status_label_variable.set("Network Offline")
            network_status_dynamic_label.config(bg="red")


# FIXME upload will throw an exception if you do not have all a sonic.png, broadband.png, and pcmag.png
# this is becuase of a limitation in the restful API. A new endpoint or dramatic changes to 
# existing endpoint are needed to accomidate special cases that use less then all three required images
def upload_images_to_backend():
    image_one_name = "sonic.png"
    image_two_name = "pcmag.png"
    iamge_three_name = "broadband.png"
    try:
        print("uploading")
        with open(image_one_name, "rb") as fileOne, open(image_two_name, "rb") as fileTwo, open(iamge_three_name, "rb") as fileThree:
            files = {'img_1': fileOne, 'img_2': fileTwo, 'img_3': fileThree}
            print("files " + str(len(files)))
            responce = requests.post(url=url+"/upload_speeds", 
                                     files=files, 
                                     data={'speed': 0, 'username':username_entry_variable.get()})
            print(responce)
    except Exception as e:
        requests.post(url=url+"/error_with_test", 
                      data={'username':username_entry_variable.get()})
        print(e)


# Runs speedtests based on what tests are selected in the settings.
def test_internet_speeds():

    chrome_options = Options()
    chrome_options.add_argument("--window-size=640,1080")
    driver = webdriver.Chrome(chrome_options)

    if (sonic_checkbox_variable.get()):
        sonic_speedtest(driver)

    if (pcmag_checkbox_variable.get()):
        pcmag_speedtest(driver)

    if (broadband_checkbox_variable.get()):
        broadbandnow_speedtest(driver)

    if (oakla_app_checkbox_variable.get()):
        oakla_app_speedtest(driver)

    if (oakla_web_checkbox_variable.get()):
        oakla_web_speedtest(driver)


# runs speedtest when ready then uploads images, sends abort request if an execption is raised
def test_and_upload_when_ready():
    try:
        speed_test_when_ready()
        upload_images_to_backend()
        test_and_upload_when_ready_button.config(state=tk.ACTIVE, 
                                             bg="red",
                                             text="Test when ready")
    except Exception as e:
        abort_speed_test()


# starts a thread running speed_test_when_ready
def start_speed_test_and_upload_as_thread():
    test_and_upload_when_ready_button.config(state=tk.DISABLED, 
                                             bg="grey",
                                             text="awaiting network")
    test_and_upload_daemon = threading.Thread(target=test_and_upload_when_ready)
    test_and_upload_daemon.daemon = True
    test_and_upload_daemon.start()


# runs a speed test on https://sonic.speedtestcustom.com and 
# saves a screenshot as sonic.png when done 
def sonic_speedtest(driver):
    driver.get("https://sonic.speedtestcustom.com")
    btn = driver.find_element(by=By.CSS_SELECTOR, value="button")
    time.sleep(1)
    btn.click()
    try:
        WebDriverWait(driver, 60).until(lambda x: x.find_element(By.XPATH, 
                "/html/body/div[1]/div/span/div[2]/div[1]/main/div/button/span")) 
    except:
        abort_speed_test()
    with mss() as sct:
        for filename in sct.save(output="sonic.png"):
            print(filename)
    print("sonic speed test done")


# runs a speed test on https://pcmag.speedtestcustom.com and 
# saves a screenshot as pcmag.png when done 
def pcmag_speedtest(driver):
    driver.get("https://pcmag.speedtestcustom.com")
    time.sleep(1)
    btn = driver.find_element(by=By.CSS_SELECTOR, value="button")
    btn.click()
    try:
        WebDriverWait(driver, 60).until(lambda x: x.find_element(By.XPATH, 
                "/html/body/div[1]/div/span/div[2]/div[1]/main/div/button/span")) 
    except:
        abort_speed_test()
    with mss() as sct:
        for filename in sct.save(output="pcmag.png"):
            print(filename)
    print("PC mag test Done")


# TODO implament speedtest for oakla's web speed test, 
# this should be almost identical to the sonic and pcmag speedtests
def oakla_web_speedtest(driver):
    raise NotImplementedError


# TODO implament speedtest for oakla's application
# look in to moving application windows and preform a 
# click where we know the button would be on the app.
def oakla_app_speedtest(driver):
    raise NotImplementedError


# runs a speed test on https://broadbandnow.com/speedtest and 
# saves a screenshot as broadband.png when done 
def broadbandnow_speedtest(driver):
    driver.get("https://broadbandnow.com/speedtest")
    btns = driver.find_elements(by=By.CSS_SELECTOR, value="button")
    time.sleep(1)
    btns[3].click()
    try:
        WebDriverWait(driver, 60).until(lambda x: x.find_element(By.XPATH, 
                "/html/body/div[8]/div[2]/div/div[2]/div/div/div[2]/div/div/div[3]/div[1]/div[3]/div[3]/h3").text == "Speed Test Completed") 
    except:
        abort_speed_test()
    with mss() as sct:
        for filename in sct.save(output="broadband.png"):
            print(filename)
    print("broadband speed test done")


def load_settings():
    with open("settings.json", "r") as f:
        global hostname 
        global port
        settingsJson = json.load(f)

        # this will throw an eeception if we don't have a hostname or port.
        # this exception is intended 
        # TODO make a popup explaining this error rather then just crashing out
        hostname = settingsJson.get("hostname")
        port = settingsJson.get("port")

        # Account information
        apikey_entry_variable.set(settingsJson.get("apiKey") or "")
        username_entry_variable.set(settingsJson.get("name") or "")

        # speedtest options
        sonic_checkbox_variable.set(settingsJson.get("runSonicSpeedTest") or False)
        pcmag_checkbox_variable.set(settingsJson.get("runPcmagSpeedTest") or False)
        broadband_checkbox_variable.set(settingsJson.get("runBroadbandSpeedTest") or False)
        oakla_app_checkbox_variable.set(settingsJson.get("runOaklaAppSpeedTest") or False)
        oakla_web_checkbox_variable.set(settingsJson.get("runOaklaWebSpeedTest") or False)

        # image delivery options
        email_entry_variable.set(settingsJson.get("email") or "")
        discord_entry_variable.set(settingsJson.get("sendDiscordMessage") or "")
        email_checkbox_variable.set(settingsJson.get("sendEmail") or False)
        discord_checkbox_variable.set(settingsJson.get("sendDiscordMessage") or False)


def save_settings():
    with open("settings.json", "w") as f:
        global hostname
        global port
        settingsJson = {}

        # Account information
        settingsJson["apiKey"] = apikey_entry_variable.get()
        settingsJson["name"] = username_entry_variable.get()
        settingsJson["hostname"] = hostname
        settingsJson["port"] = port

        # speedtest options
        settingsJson["runSonicSpeedTest"] = sonic_checkbox_variable.get()
        settingsJson["runPcmagSpeedTest"] = pcmag_checkbox_variable.get()
        settingsJson["runBroadbandSpeedTest"] = broadband_checkbox_variable.get()
        settingsJson["runOaklaAppSpeedTest"] = oakla_app_checkbox_variable.get()
        settingsJson["runOaklaWebSpeedTest"] = oakla_web_checkbox_variable.get()

        # image delivery options
        settingsJson["email"] = email_entry_variable.get()
        settingsJson["discordId"] = discord_entry_variable.get()
        settingsJson["sendEmail"] = email_checkbox_variable.get()
        settingsJson["sendDiscordMessage"] = discord_checkbox_variable.get()

        outjson = json.dumps(settingsJson)
        print(outjson)
        f.write(outjson)


# attempts to conncet with backend, starts speedtests when connection is made
def speed_test_when_ready():
    while (True):
        if (network_status.get()):
            print("network up requesting session")
            if (not request_new_session()):
                print("internal server error please contact Seaney")
                return
            print("new session requested starting speed test")
            test_internet_speeds()
            return


# Request session from API currently just to astablish that we can connect to api
# TODO have sessions saved on the back end for easy lookup if needed
def request_new_session():
    response = requests.get(url=url+"/init_session", 
                            data={'username':username_entry_variable.get()})
    print(response)
    return True


# reset UI to standby, and request backend to notify user via disorcd
def abort_speed_test():
    response = requests.post(url=url+"/error_with_test", 
                             data={'username':username_entry_variable.get()})
    test_and_upload_when_ready_button.config(state=tk.ACTIVE, 
                                             bg="red",
                                             text="Test when ready")
    return response.json()['message_sent']

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
test_and_upload_when_ready_button.grid(column=0,row=1, columnspan=3)

settings_button = tk.Button(root, 
                   text="open settings", 
                   command=open_settings,
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
                   wraplength=80)
settings_button.grid(row=2,column=0, columnspan=3)

save_button = tk.Button(root, 
                   text="save", 
                   command=save_settings,
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
                   wraplength=80,
                   state="active")

load_settings()
url = 'http://' + hostname
print("test url " + url)

network_daemon = threading.Thread(target=check_internet_connection)
network_daemon.daemon = True
network_daemon.start()  

root.mainloop()


