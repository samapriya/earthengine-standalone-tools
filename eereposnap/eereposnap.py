from __future__ import print_function
import os
import sys
import getpass
import pendulum
import platform
import json
import subprocess
import requests
import re
import shutil
import lxml
from bs4 import BeautifulSoup
os.chdir(os.path.dirname(os.path.realpath(__file__)))
path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path)

print("Today is " + str(pendulum.now()).split("T")[0])

from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time, os, getpass, subprocess

lp = os.path.dirname(os.path.realpath(__file__))
sys.path.append(lp)

reader = []
owner = []
writer = []


def eereposnap(destination, mode):
    options = Options()
    if mode == "active":
        print("Trying this in live browser")
    elif mode is None:
        options.add_argument("-headless")
    authorization_url = "https://code.earthengine.google.com/"
    try:
        uname = str(raw_input("Enter your Username:  "))
    except Exception as e:
        uname = str(input("Enter your Username:  "))
    passw = str(getpass.getpass("Enter your password: "))
    driver = Firefox(
        executable_path=os.path.join(lp, "geckodriver.exe"), firefox_options=options
    )
    driver.get(authorization_url)
    username = driver.find_element_by_xpath('//*[@id="identifierId"]')
    username.send_keys(uname)
    driver.find_element_by_id("identifierNext").click()
    time.sleep(5)
    passw = driver.find_element_by_name("password").send_keys(passw)
    driver.find_element_by_id("passwordNext").click()
    time.sleep(5)
    try:
        driver.find_element_by_xpath(
            "//div[@id='view_container']/form/div[2]/div/div/div/ul/li/div/div[2]/p"
        ).click()
        time.sleep(5)
        driver.find_element_by_xpath(
            "//div[@id='submit_approve_access']/content/span"
        ).click()
        time.sleep(10)
    except Exception as e:
        pass
    source = driver.page_source
    soup = BeautifulSoup(source, "lxml")
    source = soup.find("script", text=re.compile("window._ee_flag_initialData"))
    try:
        json_data = json.loads(
            source.text.replace("window._ee_flag_initialData = ", "")
            .replace(";", "")
            .strip()
        )
        for items in json_data["preferences"]["FAST_REPO_LISTS"]:
            if items["access"] == "owner":
                owner.append("https://earthengine.googlesource.com/" + items["name"])
            if items["access"] == "reader":
                reader.append("https://earthengine.googlesource.com/" + items["name"])
            if items["access"] == "writer":
                writer.append("https://earthengine.googlesource.com/" + items["name"])
    except Exception as e:
        print(e)
    driver.get("https://earthengine.googlesource.com/")
    driver.find_element_by_link_text("Sign in").click()
    time.sleep(3)
    driver.find_element_by_xpath(
        "//div[@id='view_container']/div/div/div[2]/div/div/div/form/span/section/div/div/div/div/ul/li/div/div/div/div[2]/div"
    ).click()
    time.sleep(10)
    cookies = driver.get_cookies()
    session = requests.Session()
    for cookie in cookies:
        session.cookies.set(cookie["name"], cookie["value"])
    driver.close()
    if not len(writer) == 0:
        for items in writer:
            base_path = os.path.join(
                destination, "writer_" + str(pendulum.now()).split("T")[0]
            )
            if not os.path.exists(base_path):
                os.makedirs(base_path)
                base_path = os.path.join(
                    destination, "writer_" + str(pendulum.now()).split("T")[0]
                )
            r = session.get(items + str("/+archive/refs/heads/master.tar.gz"))
            if r.status_code == 200:
                filename = (
                    r.headers["Content-Disposition"].split("filename=")[1].split("/")[0]
                )
                local_path = os.path.join(base_path, filename + ".tar.gz")
                if not os.path.exists(local_path):
                    try:
                        print("Downloading to: " + str(local_path))
                        f = open(local_path, "wb")
                        for chunk in r.iter_content(chunk_size=512 * 1024):
                            if chunk:
                                f.write(chunk)
                        f.close()
                        shutil.unpack_archive(
                            local_path, local_path.replace("-refs.tar.gz", "")
                        )
                        os.remove(local_path)
                    except Exception as e:
                        print(e)
                else:
                    print("File already exists: " + str(local_path))
            else:
                sys.exit("Failed with " + r.status_code)
    if not len(reader) == 0:
        for items in reader:
            base_path = os.path.join(
                destination, "reader_" + str(pendulum.now()).split("T")[0]
            )
            if not os.path.exists(base_path):
                os.makedirs(base_path)
            r = session.get(items + str("/+archive/refs/heads/master.tar.gz"))
            if r.status_code == 200:
                filename = (
                    r.headers["Content-Disposition"].split("filename=")[1].split("/")[0]
                )
                local_path = os.path.join(base_path, filename + ".tar.gz")
                if not os.path.exists(local_path):
                    try:
                        print("Downloading to: " + str(local_path))
                        f = open(local_path, "wb")
                        for chunk in r.iter_content(chunk_size=512 * 1024):
                            if chunk:
                                f.write(chunk)
                        f.close()
                        shutil.unpack_archive(
                            local_path, local_path.replace("-refs.tar.gz", "")
                        )
                        os.remove(local_path)
                    except Exception as e:
                        print(e)
                else:
                    print("File already exists: " + str(local_path))
            else:
                sys.exit("Failed with " + r.status_code)
    if not len(owner) == 0:
        for items in owner:
            base_path = os.path.join(
                destination, "owner_" + str(pendulum.now()).split("T")[0]
            )
            if not os.path.exists(base_path):
                os.makedirs(base_path)
            r = session.get(items + str("/+archive/refs/heads/master.tar.gz"))
            if r.status_code == 200:
                filename = (
                    r.headers["Content-Disposition"].split("filename=")[1].split("/")[0]
                )
                local_path = os.path.join(base_path, filename + ".tar.gz")
                if not os.path.exists(local_path):
                    try:
                        print("Downloading to: " + str(local_path))
                        f = open(local_path, "wb")
                        for chunk in r.iter_content(chunk_size=512 * 1024):
                            if chunk:
                                f.write(chunk)
                        f.close()
                        shutil.unpack_archive(
                            local_path, local_path.replace("-refs.tar.gz", "")
                        )
                        os.remove(local_path)
                    except Exception as e:
                        print(e)
                else:
                    print("File already exists: " + str(local_path))
            else:
                sys.exit("Failed with " + r.status_code)


if len(sys.argv) == 3:
    eereposnap(destination=sys.argv[1], mode=sys.argv[2])
elif len(sys.argv) == 2:
    eereposnap(destination=sys.argv[1], mode=None)
elif len(sys.argv) == 1:
    if str(platform.system().lower()) == "windows":
        os.system("python sel-latest-win.py")
    elif str(platform.system().lower()) == "linux":
        os.system("python sel-latest-linux.py")
    elif str(platform.system().lower()) == "darwin":
        os.system("python sel-latest-mac.py")
    else:
        sys.exit("Architecture not recognized")
else:
    print('Invalid arguments passed')
