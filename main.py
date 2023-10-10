import threading
import ttkbootstrap as ttk
import ttkbootstrap.dialogs
import datetime as dt
import json
import pyautogui
import pygetwindow
import pytesseract
import cv2
from tkinter import *
from threading import Event, Thread
from time import sleep, time, strftime, gmtime
from datetime import datetime, timedelta
from win32gui import FindWindow, GetWindowRect
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import ToolTip
from ttkbootstrap.tableview import Tableview, TableColumn
from ttkbootstrap.dialogs import Messagebox
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

no_reward_pressed = True
window_visible = True
first = False
firstrun = True
rows = []

BUTTON_IMG_SIZE = 7
ANU_SIZE = BUTTON_IMG_SIZE - 1
GAARD_NYSHA_SIZE = BUTTON_IMG_SIZE - 2
FULL_WIDTH = 8
WIDTH = 10
FONT_SIZE = 15

# WINDOW #

window = ttk.Window(themename="darkly")
window.title("GoW Helper")
window.configure(pady=0, padx=0)
window.resizable(False, False)
window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)
icon_pic = PhotoImage(file="img/magic.png")
window.iconphoto(False, icon_pic)

mainframe = ttk.Frame(window, padding="0 0 0 0", relief=FLAT)
mainframe.grid(column=0, row=0, sticky=W + E)


# DEFAULT SETTINGS #


# FUNCTIONS #

def gaard():
    global no_reward_pressed, first

    if no_reward_pressed and not first:
        current = int(gaardbutton["text"])
        gaardbutton["text"] = str(current + 1)
    check_submit_button()

def yasmine():
    global no_reward_pressed, first

    if no_reward_pressed and not first:
        current = int(yasminebutton["text"])
        yasminebutton["text"] = str(current + 1)
    check_submit_button()

def orpheus():
    global no_reward_pressed, first

    if no_reward_pressed and not first:
        current = int(orpheusbutton["text"])
        orpheusbutton["text"] = str(current + 1)
    check_submit_button()

def aranea():
    global no_reward_pressed, first

    if no_reward_pressed and not first:
        current = int(araneabutton["text"])
        araneabutton["text"] = str(current + 1)
    check_submit_button()

def anu():
    global no_reward_pressed, first

    if no_reward_pressed and not first:
        current = int(anubutton["text"])
        anubutton["text"] = str(current + 1)
    check_submit_button()

def nysha():
    global no_reward_pressed, first

    if no_reward_pressed and not first:
        current = int(nyshabutton["text"])
        nyshabutton["text"] = str(current + 1)
    check_submit_button()

def no_reward(): #DONE
    global no_reward_pressed, first
    first = True

    if no_reward_pressed:
        norewardbutton.configure(bootstyle="danger")
        mimic_regular.configure(state="disabled")
        mimic_mythic.configure(state="disabled")
        gaardbutton.configure(state="disabled")
        yasminebutton.configure(state="disabled")
        orpheusbutton.configure(state="disabled")
        araneabutton.configure(state="disabled")
        anubutton.configure(state="disabled")
        nyshabutton.configure(state="disabled")
        no_reward_pressed = False

    else:
        norewardbutton.configure(bootstyle="info-outline")
        mimic_regular.configure(state="active")
        mimic_mythic.configure(state="active")
        gaardbutton.configure(state="active")
        yasminebutton.configure(state="active")
        orpheusbutton.configure(state="active")
        araneabutton.configure(state="active")
        anubutton.configure(state="active")
        nyshabutton.configure(state="active")

        no_reward_pressed = True
        first = False

    gaardbutton["text"] = "0"
    yasminebutton["text"] = "0"
    orpheusbutton["text"] = "0"
    araneabutton["text"] = "0"
    anubutton["text"] = "0"
    nyshabutton["text"] = "0"

    check_submit_button()

def reset(): #DONE
    global no_reward_pressed, first
    gaardbutton["text"] = "0"
    yasminebutton["text"] = "0"
    orpheusbutton["text"] = "0"
    araneabutton["text"] = "0"
    anubutton["text"] = "0"
    nyshabutton["text"] = "0"
    mimic_regular.configure(state="active")
    mimic_mythic.configure(state="active")
    gaardbutton.configure(state="active")
    yasminebutton.configure(state="active")
    orpheusbutton.configure(state="active")
    araneabutton.configure(state="active")
    anubutton.configure(state="active")
    nyshabutton.configure(state="active")
    mim_var.set(0)
    mythmim_var.set(0)
    norewardbutton.configure(bootstyle="info-outline")
    no_reward_pressed = True
    first = False
    check_submit_button()

def update_alltime_stats():
    if history_var.get() == 1:
        alltime_gaard_tokens["text"] = str(int(alltime_gaard_tokens["text"]) + int(gaardbutton["text"]))
        alltime_yasmine_tokens["text"] = str(int(alltime_yasmine_tokens["text"]) + int(yasminebutton["text"]))
        alltime_orpheus_tokens["text"] = str(int(alltime_orpheus_tokens["text"]) + int(orpheusbutton["text"]))
        alltime_aranea_tokens["text"] = str(int(alltime_aranea_tokens["text"]) + int(araneabutton["text"]))
        alltime_anu_tokens["text"] = str(int(alltime_anu_tokens["text"]) + int(anubutton["text"]))
        alltime_nysha_tokens["text"] = str(int(alltime_nysha_tokens["text"]) + int(nyshabutton["text"]))

        alltime_run_events["text"] = str(int(alltime_run_events["text"]) + 1)

        if mythmim_var.get() == 1:
            alltime_mythic_mimic_events["text"] = str(int(alltime_mythic_mimic_events["text"]) + 1)
            alltime_mimic_events["text"] = str(int(alltime_mimic_events["text"]) + 1)
            alltime_battles["text"] = str(int(alltime_battles["text"]) + 8)
        elif mim_var.get() == 1:
            alltime_mimic_events["text"] = str(int(alltime_mimic_events["text"]) + 1)
            alltime_battles["text"] = str(int(alltime_battles["text"]) + 7)

        if mythmim_var.get() == 0 and mim_var.get() == 0 and no_reward_pressed:
            alltime_battles["text"] = str(int(alltime_battles["text"]) + 6)

        if not no_reward_pressed:
            alltime_noreward_events["text"] = str(int(alltime_noreward_events["text"]) + 1)
            alltime_battles["text"] = str(int(alltime_battles["text"]) + 5)

        calculate_alltime_percentages()

def drop_perc(tokens, division):
    try:
        result = approx((tokens / division) * 100)
    except ZeroDivisionError:
        return "0%"
    else:
        return f"{result}%"

def check_submit_button(): #DONE
    if int(gaardbutton["text"]) == 0 and int(yasminebutton["text"]) == 0 and int(orpheusbutton["text"]) == 0 and int(araneabutton["text"]) == 0 and int(anubutton["text"]) == 0 and int(nyshabutton["text"]) == 0 and no_reward_pressed and not first:
        submit_button.configure(state="disabled")
    else:
        submit_button.configure(state="active")

def submit():
    if int(gaardbutton["text"]) == 0 and int(yasminebutton["text"]) == 0 and int(orpheusbutton["text"]) == 0 and int(araneabutton["text"]) == 0 and int(anubutton["text"]) == 0 and int(nyshabutton["text"]) == 0 and no_reward_pressed and not first:
        return

    update_alltime_stats()

    if mythmim_var.get() == 1:
        session_mythic_mimic_events["text"] = str(int(session_mythic_mimic_events["text"]) + 1)
        session_mimic_events["text"] = str(int(session_mimic_events["text"]) + 1)
        session_battles["text"] = str(int(session_battles["text"]) + 8)
    elif mim_var.get() == 1:
        session_mimic_events["text"] = str(int(session_mimic_events["text"]) + 1)
        session_battles["text"] = str(int(session_battles["text"]) + 7)

    if mythmim_var.get() == 0 and mim_var.get() == 0 and no_reward_pressed:
        session_battles["text"] = str(int(session_battles["text"]) + 6)

    if not no_reward_pressed:
        session_noreward_events["text"] = str(int(session_noreward_events["text"]) + 1)
        session_battles["text"] = str(int(session_battles["text"]) + 5)
        gaardbutton.configure(state="active")
        yasminebutton.configure(state="active")
        orpheusbutton.configure(state="active")
        araneabutton.configure(state="active")
        anubutton.configure(state="active")
        nyshabutton.configure(state="active")
        no_reward()

    session_gaard_tokens["text"] = str(int(session_gaard_tokens["text"]) + int(gaardbutton["text"]))
    session_yasmine_tokens["text"] = str(int(session_yasmine_tokens["text"]) + int(yasminebutton["text"]))
    session_orpheus_tokens["text"] = str(int(session_orpheus_tokens["text"]) + int(orpheusbutton["text"]))
    session_aranea_tokens["text"] = str(int(session_aranea_tokens["text"]) + int(araneabutton["text"]))
    session_anu_tokens["text"] = str(int(session_anu_tokens["text"]) + int(anubutton["text"]))
    session_nysha_tokens["text"] = str(int(session_nysha_tokens["text"]) + int(nyshabutton["text"]))

    session_run_events["text"] = str(int(session_run_events["text"]) + 1)

    gaardbutton["text"] = "0"
    yasminebutton["text"] = "0"
    orpheusbutton["text"] = "0"
    araneabutton["text"] = "0"
    anubutton["text"] = "0"
    nyshabutton["text"] = "0"

    check_save_reset_buttons()
    save_session()
    save_alltime()
    calculate_percentages()
    reset()

def approx(num):
    multiplier = 10 ** 2
    return int(num * multiplier) / multiplier

def calculate_percentages():
    g = int(session_gaard_tokens["text"])
    y = int(session_yasmine_tokens["text"])
    o = int(session_orpheus_tokens["text"])
    ar = int(session_aranea_tokens["text"])
    an = int(session_anu_tokens["text"])
    n = int(session_nysha_tokens["text"])
    total_tokens = g + y + o + ar + an + n

    runs = int(session_run_events["text"])
    mim = int(session_mimic_events["text"])
    hoa = int(session_mythic_mimic_events["text"])
    nor = int(session_noreward_events["text"])

    session_noreward_percent["text"] = drop_perc(nor, runs)
    session_mimic_percent["text"] = drop_perc(mim, runs)
    session_mythic_mimic_percent["text"] = drop_perc(hoa, runs)
    session_gaard_drop["text"] = drop_perc(g, total_tokens)
    session_yasmine_drop["text"] = drop_perc(y, total_tokens)
    session_orpheus_drop["text"] = drop_perc(o, total_tokens)
    session_aranea_drop["text"] = drop_perc(ar, total_tokens)
    session_anu_drop["text"] = drop_perc(an, total_tokens)
    session_nysha_drop["text"] = drop_perc(n, total_tokens)

def calculate_alltime_percentages():

    g = int(alltime_gaard_tokens["text"])
    y = int(alltime_yasmine_tokens["text"])
    o = int(alltime_orpheus_tokens["text"])
    ar = int(alltime_aranea_tokens["text"])
    an = int(alltime_anu_tokens["text"])
    n = int(alltime_nysha_tokens["text"])
    total_tokens = g + y + o + ar + an + n

    runs = int(alltime_run_events["text"])
    mim = int(alltime_mimic_events["text"])
    hoa = int(alltime_mythic_mimic_events["text"])
    nor = int(alltime_noreward_events["text"])

    alltime_noreward_percent["text"] = drop_perc(nor, runs)
    alltime_mimic_percent["text"] = drop_perc(mim, runs)
    alltime_mythic_mimic_percent["text"] = drop_perc(hoa, runs)
    alltime_gaard_drop["text"] = drop_perc(g, total_tokens)
    alltime_yasmine_drop["text"] = drop_perc(y, total_tokens)
    alltime_orpheus_drop["text"] = drop_perc(o, total_tokens)
    alltime_aranea_drop["text"] = drop_perc(ar, total_tokens)
    alltime_anu_drop["text"] = drop_perc(an, total_tokens)
    alltime_nysha_drop["text"] = drop_perc(n, total_tokens)

def history_tooltip():
    if history_var.get() == 1:
        ToolTip(submit_button, text="Submit run to Session Stats and All-Time Stats.", bootstyle=(INFO, INVERSE), wraplength=200)
    else:
        ToolTip(submit_button, text="Submit run to Session Stats only.", bootstyle=(INFO, INVERSE), wraplength=200)

def mimic_toggle():
    mim_var.set(1)

def mimic_mythic_toggle():
    mim_var.set(0)
    if mythmim_var.get() == 1:
        mythmim_var.set(1)
        mimic_regular.configure(state="disabled")
        mim_var.set(0)
    else:
        mythmim_var.set(0)
        mimic_regular.configure(state="active")

def reset_session():
    popup =  Messagebox.okcancel(title="Session Stats Reset", message="Are you sure you want to reset all your Session Stats?", parent=window, alert=True)
    if popup == "OK":
        session_gaard_tokens["text"] = "0"
        session_yasmine_tokens["text"] = "0"
        session_orpheus_tokens["text"] = "0"
        session_aranea_tokens["text"] = "0"
        session_anu_tokens["text"] = "0"
        session_nysha_tokens["text"] = "0"
        session_run_events["text"] = "0"
        session_mimic_events["text"] = "0"
        session_mythic_mimic_events["text"] = "0"
        session_noreward_events["text"] = "0"
        session_noreward_percent["text"] = "0%"
        session_mimic_percent["text"] = "0%"
        session_mythic_mimic_percent["text"] = "0%"
        session_gaard_drop["text"] = "0%"
        session_yasmine_drop["text"] = "0%"
        session_orpheus_drop["text"] = "0%"
        session_aranea_drop["text"] = "0%"
        session_anu_drop["text"] = "0%"
        session_nysha_drop["text"] = "0%"
        session_battles["text"] = "0"
        save_session()
        check_save_reset_buttons()

def reset_alltime():
    popup = Messagebox.okcancel(title="All-Time Stats Reset", message="Are you sure you want to reset all your All-Time Stats?", parent=window, alert=True)
    if popup == "OK":
        alltime_gaard_tokens["text"] = "0"
        alltime_yasmine_tokens["text"] = "0"
        alltime_orpheus_tokens["text"] = "0"
        alltime_aranea_tokens["text"] = "0"
        alltime_anu_tokens["text"] = "0"
        alltime_nysha_tokens["text"] = "0"
        alltime_run_events["text"] = "0"
        alltime_mimic_events["text"] = "0"
        alltime_mythic_mimic_events["text"] = "0"
        alltime_noreward_events["text"] = "0"
        alltime_noreward_percent["text"] = "0%"
        alltime_mimic_percent["text"] = "0%"
        alltime_mythic_mimic_percent["text"] = "0%"
        alltime_gaard_drop["text"] = "0%"
        alltime_yasmine_drop["text"] = "0%"
        alltime_orpheus_drop["text"] = "0%"
        alltime_aranea_drop["text"] = "0%"
        alltime_anu_drop["text"] = "0%"
        alltime_nysha_drop["text"] = "0%"
        alltime_battles["text"] = "0"
        save_alltime()
        check_save_reset_buttons()

def load_session():
    try:
        with open("sessiondata.json", "r") as data_file:
            session_data = json.load(data_file)
    except FileNotFoundError:
        return
    session_gaard_tokens["text"] = session_data["session"]["gaard"]
    session_yasmine_tokens["text"] = session_data["session"]["yasmine"]
    session_orpheus_tokens["text"] = session_data["session"]["orpheus"]
    session_aranea_tokens["text"] = session_data["session"]["aranea"]
    session_anu_tokens["text"] = session_data["session"]["anu"]
    session_nysha_tokens["text"] = session_data["session"]["nysha"]
    session_run_events["text"] = session_data["session"]["runs"]
    session_mimic_events["text"] = session_data["session"]["mimic"]
    session_mythic_mimic_events["text"] = session_data["session"]["hoard"]
    session_noreward_events["text"] = session_data["session"]["noreward"]
    session_battles["text"] = session_data["session"]["battles"]
    calculate_percentages()

def load_alltime():
    try:
        with open("atdata.json", "r") as data_file:
            alltime_data = json.load(data_file)
    except FileNotFoundError:
        return
    alltime_gaard_tokens["text"] = alltime_data["alltime"]["gaard"]
    alltime_yasmine_tokens["text"] = alltime_data["alltime"]["yasmine"]
    alltime_orpheus_tokens["text"] = alltime_data["alltime"]["orpheus"]
    alltime_aranea_tokens["text"] = alltime_data["alltime"]["aranea"]
    alltime_anu_tokens["text"] = alltime_data["alltime"]["anu"]
    alltime_nysha_tokens["text"] = alltime_data["alltime"]["nysha"]
    alltime_run_events["text"] = alltime_data["alltime"]["runs"]
    alltime_mimic_events["text"] = alltime_data["alltime"]["mimic"]
    alltime_mythic_mimic_events["text"] = alltime_data["alltime"]["hoard"]
    alltime_noreward_events["text"] = alltime_data["alltime"]["noreward"]
    alltime_battles["text"] = alltime_data["alltime"]["battles"]

    calculate_alltime_percentages()

def save_session():
    session_data = {
        "session": {
            "gaard": session_gaard_tokens["text"],
            "yasmine": session_yasmine_tokens["text"],
            "orpheus": session_orpheus_tokens["text"],
            "aranea": session_aranea_tokens["text"],
            "anu": session_anu_tokens["text"],
            "nysha": session_nysha_tokens["text"],
            "runs": session_run_events["text"],
            "mimic": session_mimic_events["text"],
            "hoard": session_mythic_mimic_events["text"],
            "noreward": session_noreward_events["text"],
            "battles": session_battles["text"],
        }
    }
    try:
        with open("sessiondata.json", "r") as data_file:
            jsondata = json.load(data_file)
    except FileNotFoundError:
        with open("sessiondata.json", "w") as data_file:
            json.dump(session_data, data_file, indent=4)
    else:
        jsondata.update(session_data)
        with open("sessiondata.json", "w") as data_file:
            json.dump(jsondata, data_file, indent=4)

def save_alltime():
    alltime_data = {
        "alltime": {
            "gaard": alltime_gaard_tokens["text"],
            "yasmine": alltime_yasmine_tokens["text"],
            "orpheus": alltime_orpheus_tokens["text"],
            "aranea": alltime_aranea_tokens["text"],
            "anu": alltime_anu_tokens["text"],
            "nysha": alltime_nysha_tokens["text"],
            "runs": alltime_run_events["text"],
            "mimic": alltime_mimic_events["text"],
            "hoard": alltime_mythic_mimic_events["text"],
            "noreward": alltime_noreward_events["text"],
            "battles": alltime_battles["text"],
        }
    }
    try:
        with open("atdata.json", "r") as data_file:
            jsondata = json.load(data_file)
    except FileNotFoundError:
        with open("atdata.json", "w") as data_file:
            json.dump(alltime_data, data_file, indent=4)
    else:
        jsondata.update(alltime_data)
        with open("atdata.json", "w") as data_file:
            json.dump(jsondata, data_file, indent=4)

def save_session_history(): # UNFINISHED, DO I EVEN NEED THIS??????
    session_data = {
         {
            "gaard": session_gaard_tokens["text"],
            "yasmine": session_yasmine_tokens["text"],
            "orpheus": session_orpheus_tokens["text"],
            "aranea": session_aranea_tokens["text"],
            "anu": session_anu_tokens["text"],
            "nysha": session_nysha_tokens["text"],
            "runs": session_run_events["text"],
            "mimic": session_mimic_events["text"],
            "hoard": session_mythic_mimic_events["text"],
            "noreward": session_noreward_events["text"],
            "battles": session_battles["text"],
        }
    }
    try:
        with open("shdata.json", "r") as data_file:
            jsondata = json.load(data_file)
    except FileNotFoundError:
        with open("shdata.json", "w") as data_file:
            json.dump(session_data, data_file, indent=4, default=str)
    else:
        jsondata.update(session_data)
        with open("shdata.json", "w") as data_file:
            json.dump(jsondata, data_file, indent=4)

def load_session_history(): # UNFINISHED
    try:
        with open("historydata.json", "r") as data_file:
            history = json.load(data_file)
    except FileNotFoundError:
        return

    global rows

    for row in history:
        session_table.insert_row(0, row)
        rows.append(row)

    session_table.load_table_data()

def submit_session():
    new_row = [ dt.date.today(),
                session_run_events["text"],
                session_gaard_tokens["text"],
                session_yasmine_tokens["text"],
                session_orpheus_tokens["text"],
                session_aranea_tokens["text"],
                session_anu_tokens["text"],
                session_nysha_tokens["text"],
                session_noreward_events["text"],
                session_mimic_events["text"],
                session_mythic_mimic_events["text"]]

    session_table.insert_row("end", new_row)
    global rows
    rows.append(new_row)

    try:
        with open("historydata.json", "r") as data_file:
            jsondata = json.load(data_file)
    except FileNotFoundError:
        with open("historydata.json", "w") as data_file:
            json.dump(rows, data_file, indent=4, default=str)
    else:
        with open("historydata.json", "w") as data_file:
            json.dump(rows, data_file, indent=4, default=str)

    session_table.load_table_data()

    session_gaard_tokens["text"] = "0"
    session_yasmine_tokens["text"] = "0"
    session_orpheus_tokens["text"] = "0"
    session_aranea_tokens["text"] = "0"
    session_anu_tokens["text"] = "0"
    session_nysha_tokens["text"] = "0"
    session_run_events["text"] = "0"
    session_mimic_events["text"] = "0"
    session_mythic_mimic_events["text"] = "0"
    session_noreward_events["text"] = "0"
    session_noreward_percent["text"] = "0%"
    session_mimic_percent["text"] = "0%"
    session_mythic_mimic_percent["text"] = "0%"
    session_gaard_drop["text"] = "0%"
    session_yasmine_drop["text"] = "0%"
    session_orpheus_drop["text"] = "0%"
    session_aranea_drop["text"] = "0%"
    session_anu_drop["text"] = "0%"
    session_nysha_drop["text"] = "0%"
    session_battles["text"] = "0"
    save_session()
    check_save_reset_buttons()

def check_save_reset_buttons():

    if session_battles["text"] == "0":
        save_session_button.configure(state="disabled")
        reset_session_button.configure(state="disabled")
    else:
        save_session_button.configure(state="active")
        reset_session_button.configure(state="active")
    if alltime_battles["text"] == "0":
        reset_alltime_button.configure(state="disabled")
    else:
        reset_alltime_button.configure(state="active")

def tooltips_toggle():
    if tooltip_var.get() == 1:
        ToolTip(norewardbutton, text="No reward gained this run. Only shards gained.", bootstyle=(INFO, INVERSE),
                wraplength=200)
        ToolTip(resetbutton, text="Reset all selections.", bootstyle=(INFO, INVERSE), wraplength=200)
    else:
        del submit_tooltip

def start_thread():
    def create_thread():
        return Thread(target=wait_for_event)

    # if threading.active_count() > 1: threading.enumerate()[1].join() Trying to close down thread
    now = datetime.now()
    timenow = now.strftime("%H:%M")

    if autotoggle_var.get() == 1:
        t1 = create_thread()
        t1.start()
        auto_log.configure(state="normal")
        auto_log.insert(END, f"{timenow}: Auto-detection ON\n")
        auto_log.configure(state="disabled")
        auto_log.see("end -2 lines")
    else:
        auto_log.configure(state="normal")
        auto_log.insert(END, f"{timenow}: Auto-detection OFF\n")
        auto_log.configure(state="disabled")
        auto_log.see("end -2 lines")
        auto_info["text"] = "STATUS: Inactive"

def find_medal_rewards(string):
    medals = {"Gaard": 0, "Yasmine": 0, "Orpheus": 0, "Aranaea": 0, "Anu": 0, "Nysha": 0}
    temp = string.splitlines()
    num = ""

    for medal in medals:
        for item in temp:
            if item.find(medal) != -1:
                for char in item:
                    if char.isnumeric():
                        num += char
                medals[medal] = int(num)
                num = ""
    return medals

def auto_detect_rewards():
    # TAKE TIME FOR HOW LONG FUNCTION TAKES TO COMPLETE #
    start = time()
    sleep(0.4)
    # GET WINDOW COORDINATES #
    window_handle = FindWindow(None, "GemsofWar")
    window_rect = GetWindowRect(window_handle)

    # GET WINDOW AND RESIZE IT #
    win = pygetwindow.getWindowsWithTitle('GemsofWar')[0]
    win.activate()
    win.restore()

    win.size = (1200, 800)

    # CALCULATE PROPER TOP-LEFT CORNER COORDS #
    x = GetWindowRect(window_handle)[0] + 10
    y = GetWindowRect(window_handle)[1]

    # TAKE SCREENSHOT OF GAME WINDOW AND PARSE IT FOR TEXT, AND REWARDS #
    screenshot = pyautogui.screenshot("img/screenshot.png", region=(x+430, y+160, 571, 370))
    img = cv2.imread("img/screenshot.png")
    img = cv2.bilateralFilter(img, 9, 75, 75)
    cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    tess_result = pytesseract.image_to_string(img, config="--psm 6")

    player_rewards = find_medal_rewards(tess_result)

    now = datetime.now()
    luck = 0
    timenow = now.strftime("%H:%M")
    message = f"{timenow}: Tokens looted: "

    # CALCULATE DROP LUCK VALUE #

    for key, value in player_rewards.items():
        if key == "Gaard":
            luck += value * 5.55
        if key == "Yasmine":
            luck += value * 4.35
        if key == "Orpheus":
            luck += value * 2.5
        if key == "Aranaea":
            luck += value * 8.33
        if key == "Anu":
            luck += value * 20
        if key == "Nysha":
            luck += value * 50

    # SUBMIT THE REWARDS TO THE TOKEN BUTTONS #
    try:
        if player_rewards["Gaard"] > 0:
            gaardbutton["text"] = str(int(gaardbutton["text"]) + player_rewards["Gaard"])
            message += f"{player_rewards['Gaard']} Gaard. "
        if player_rewards["Yasmine"] > 0:
            yasminebutton["text"] = str(int(yasminebutton["text"]) + player_rewards["Yasmine"])
            message += f"{player_rewards['Yasmine']} Yasmine. "
        if player_rewards["Orpheus"] > 0:
            orpheusbutton["text"] = str(int(orpheusbutton["text"]) + player_rewards["Orpheus"])
            message += f"{player_rewards['Orpheus']} Orpheus. "
        if player_rewards["Aranaea"] > 0:
            araneabutton["text"] = str(int(araneabutton["text"]) + player_rewards["Aranaea"])
            message += f"{player_rewards['Aranaea']} Aranaea. "
        if player_rewards["Anu"] > 0:
            anubutton["text"] = str(int(anubutton["text"]) + player_rewards["Anu"])
            message += f"{player_rewards['Anu']} Anu. "
        if player_rewards["Nysha"] > 0:
            nyshabutton["text"] = str(int(nyshabutton["text"]) + player_rewards["Nysha"])
            message += f"{player_rewards['Nysha']} Nysha. "
    except IndexError:
        auto_log.configure(state="normal")
        auto_log.insert(END, "Index Error. Could not properly detect rewards.\n")
        auto_log.insert(END, f"Tesseract findings: {tess_result}")
        auto_log.configure(state="disabled")
        auto_log.see("end -2 lines")

    total = 0
    for item, value in player_rewards.items(): total += value

    if total == 0:
        auto_log.configure(state="normal")
        auto_log.insert(END, "Error. No rewards logged.\n")
        auto_log.insert(END, f"Tesseract findings: {tess_result}")
        auto_log.configure(state="disabled")
        auto_log.see("end -2 lines")

    if total > 6:
        mythmim_var.set(1)
        mimic_regular.configure(state="disabled")
        message += " Battled a Mimic and a Hoard Mimic."
    elif total < 4:
        pass
    else:
        mimic_toggle()
        message += " Battled a Mimic."

    if luck > 0: message += f" Luck: {approx(luck)}"
    message += "\n"

    if tess_result.find("x1") != -1: message += f"{timenow}: Congratulations! You received a Hoard Mimic troop!\n"

    end = time()
    if auto_submission_var.get() == 1: submit()

    auto_log.configure(state="normal")
    auto_log.insert(END, message)
    auto_log.configure(state="disabled")
    auto_log.see("end -2 lines")

    check_submit_button()

def locate(image, x, y, xx, yy):
    global window_visible
    try:
        if pyautogui.locateOnScreen(image, grayscale=True, confidence=0.8, region=(x, y, xx, yy)) != None:
            window_visible = True
            return True
        else:
            window_visible = True
            return False
    except ValueError:
        window_visible = False

def wait_for_event():
    win = pygetwindow.getWindowsWithTitle('GemsofWar')[0]
    window_handle = FindWindow(None, "GemsofWar")
    win.size = (1200, 800)
    start, end = time(), 0
    new_run = False

    def status(string):
        if window_visible:
            auto_info["text"] = "STATUS: " + string
        else:
            auto_info["text"] = "ERROR: Could not find game window. Make sure it is visible on your primary monitor."

    def add(text):
        now = datetime.now()
        timenow = now.strftime("%H:%M")
        auto_log.configure(state="normal")
        auto_log.insert(END, f"{timenow}: {text}\n")
        auto_log.configure(state="disabled")
        auto_log.see("end -2 lines")

    def setup_window():
        coords = []
        window_rect = GetWindowRect(window_handle)
        winx = window_rect[2] - window_rect[0]
        winy = window_rect[3] - window_rect[1]
        if winx != 1200 or winy != 800: win.size = (1200, 800)

        coords.append(GetWindowRect(window_handle)[0] + 10)
        coords.append(GetWindowRect(window_handle)[1])

        return coords

    def wait_for_reset():
        reset = True
        while reset and autotoggle_var.get() == 1:
            xy = setup_window()
            if locate('img/explorereset2020.png', xy[0]+128, xy[1]+630, 40, 40):
                reset = False
                new_run = True
            else:
                status("Waiting for a new run to start.")
                sleep(0.5)

    while autotoggle_var.get() == 1:
        if new_run:
            m = ""
            end = time()
            if start != 0:
                ty_res = gmtime(end - start)
                res = strftime("%H:%M:%S", ty_res)
                m = f" Finished run took: {res}"
            add(f"New run started.{m}")
            new_run = False
            start = time()

        xy = setup_window()
        if locate('img/youreceived2020.png', xy[0]+570, xy[1]+60, 70, 40):
            auto_detect_rewards()
            wait_for_reset()
        elif locate('img/miniboss2020.png', xy[0]+575, xy[1]+245, 50, 50):
            add("Mini Boss detected.")
            miniboss = True
            while miniboss and autotoggle_var.get() == 1:
                xy = setup_window()
                if locate('img/youreceived2020.png', xy[0]+570, xy[1]+60, 70, 40):
                    miniboss = False
                    new_run = True

                    auto_detect_rewards()
                    wait_for_reset()
                elif locate('img/noexplore2020.png', xy[0]+180, xy[1]+630, 40, 40):
                    xy = setup_window()
                    if locate('img/noexplore2020.png', xy[0]+180, xy[1]+630, 40, 40):
                        miniboss = False
                        new_run = True
                        add("Run finished with no token rewards. Only Mythstones gained.")
                        no_reward()
                        if auto_submission_var.get() == 1: submit()
                else:
                    status("Waiting for run to finish or No Reward run.")
        else:
            status("Waiting for mini boss/first reward run")
    auto_info["text"] = "STATUS: Inactive"

# IMAGE MATERIAL #

anu_pic = PhotoImage(file="img/anu.png")
aranea_pic = PhotoImage(file="img/aranea.png")
gaard_pic = PhotoImage(file="img/gaard.png")
nysha_pic = PhotoImage(file="img/nysha.png")
orpheus_pic = PhotoImage(file="img/orpheus.png")
yasmine_pic = PhotoImage(file="img/yasmine.png")
mimic_pic = PhotoImage(file="img/mimic.png")
mythic_mimic_pic = PhotoImage(file="img/mythicmimic.png")
fragments_pic = PhotoImage(file="img/bossfragments.png")
reset_pic = PhotoImage(file="img/reset.png")
runs_pic = PhotoImage(file="img/runs.png")

anu_pic = anu_pic.subsample(ANU_SIZE, ANU_SIZE)
aranea_pic = aranea_pic.subsample(BUTTON_IMG_SIZE, BUTTON_IMG_SIZE)
gaard_pic = gaard_pic.subsample(GAARD_NYSHA_SIZE, GAARD_NYSHA_SIZE)
nysha_pic = nysha_pic.subsample(GAARD_NYSHA_SIZE, GAARD_NYSHA_SIZE)
orpheus_pic = orpheus_pic.subsample(BUTTON_IMG_SIZE, BUTTON_IMG_SIZE)
yasmine_pic = yasmine_pic.subsample(BUTTON_IMG_SIZE, BUTTON_IMG_SIZE)
fragments_pic = fragments_pic.subsample(5, 5)
mimic_pic = mimic_pic.subsample(BUTTON_IMG_SIZE)
mythic_mimic_pic = mythic_mimic_pic.subsample(BUTTON_IMG_SIZE)
reset_pic = reset_pic.subsample(12, 12)
runs_pic = runs_pic.subsample(10, 10)

# TOP TEXT LABELS #

ttk.Label(mainframe, text="Gaard").grid(column=0, row=0, sticky="NS")
ttk.Label(mainframe, text="Yasmine").grid(column=1, row=0, sticky="NS")
ttk.Label(mainframe, text="Orpheus").grid(column=2, row=0, sticky="NS")
ttk.Label(mainframe, text="Aranaea").grid(column=3, row=0, sticky="NS")
ttk.Label(mainframe, text="Anu").grid(column=4, row=0, sticky="NS")
ttk.Label(mainframe, text="Nysha").grid(column=5, row=0, sticky="NS")

# TOKEN BUTTONS #

gaardbutton = ttk.Button(mainframe, bootstyle="info-outline", text="0", image=gaard_pic,
                        compound=TOP, command=gaard, width=WIDTH)
gaardbutton.grid(column=0, row=1, sticky="NS", padx=2)
yasminebutton = ttk.Button(mainframe, bootstyle="info-outline", text="0", image=yasmine_pic, compound=TOP,
                           command=yasmine, width=WIDTH)
yasminebutton.grid(column=1, row=1, sticky="NS", padx=2)
orpheusbutton = ttk.Button(mainframe, bootstyle="info-outline", text="0", image=orpheus_pic, compound=TOP,
                           command=orpheus, width=WIDTH)
orpheusbutton.grid(column=2, row=1, sticky="NS", padx=2)
araneabutton = ttk.Button(mainframe, bootstyle="info-outline", text="0", image=aranea_pic, compound=TOP,
                          command=aranea, width=WIDTH)
araneabutton.grid(column=3, row=1, sticky="NS", padx=2)
anubutton = ttk.Button(mainframe, bootstyle="info-outline", text="0", image=anu_pic, compound=TOP,
                       command=anu, width=WIDTH)
anubutton.grid(column=4, row=1, sticky="NS", padx=2)
nyshabutton = ttk.Button(mainframe, bootstyle="info-outline", text="0", image=nysha_pic, compound=TOP,
                         command=nysha, width=WIDTH)
nyshabutton.grid(column=5, row=1, sticky="NS", padx=2)

# CHECKBOXES AND COMMAND BUTTONS #

mim_var = IntVar()
mim_var.set(0)
mimic_regular = ttk.Checkbutton(mainframe, bootstyle="info-square-toggle", variable=mim_var,
                                onvalue=1, offvalue=0, state="active", text="Mimic", command=mimic_toggle)
mimic_regular.grid(column=0, row=2, sticky="W", padx=3, pady=10)
mythmim_var = IntVar()
mythmim_var.set(0)
mimic_mythic = ttk.Checkbutton(mainframe, bootstyle="info-square-toggle", variable=mythmim_var,
                               onvalue=1, offvalue=0, state="active", text="Hoard Mimic", command=mimic_mythic_toggle)
mimic_mythic.grid(column=1, row=2, sticky="W", padx=3, pady=10, columnspan=2)
norewardbutton = ttk.Button(mainframe, bootstyle="info-outline", compound=LEFT,
                            command=no_reward, width=WIDTH, text="No Reward")
norewardbutton.grid(column=4, row=2, sticky=EW, padx=2)
ToolTip(norewardbutton, text="No reward gained this run. Only shards gained.", bootstyle=(INFO, INVERSE), wraplength=200)
resetbutton = ttk.Button(mainframe, bootstyle="info-outline", compound=LEFT,
                         command=reset, width=WIDTH, text="Reset")
resetbutton.grid(column=3, row=2, sticky=EW, padx=2)
ToolTip(resetbutton, text="Reset all selections.", bootstyle=(INFO, INVERSE), wraplength=200)
submit_button = ttk.Button(mainframe, bootstyle="info-outline", text="Done", command=submit, width=5)
submit_button.grid(column=5, row=2, sticky=W, padx=2, pady=10)
if firstrun:
    submit_tooltip = ToolTip(submit_button, text="Submit run to Session Stats and All-Time Stats.", bootstyle=(INFO, INVERSE), wraplength=200)
    firstrun = False
history_var = IntVar()
history_var.set(1)
log_history = ttk.Checkbutton(mainframe, bootstyle="info-square-toggle", variable=history_var,
                                onvalue=1, offvalue=0, state="active", command=history_tooltip)
log_history.grid(column=5, row=2, sticky=E, padx=0, pady=10)
ToolTip(log_history, "Check this box to submit run stats to All-Time Stats as well.", bootstyle=(INFO, INVERSE), wraplength=200, delay=0)

# NOTEBOOK INITIALIZATION #

stats_notebook = ttk.Notebook(mainframe, bootstyle="info")
stats_notebook.grid(column=0, row=3, columnspan=6, sticky=EW, padx=0, pady=0)

session_stats = ttk.Frame(stats_notebook, width=500, height=300)
alltime_stats = ttk.Frame(stats_notebook, width=500, height=300)
session_history = ttk.Frame(stats_notebook, width=500, height=300)
auto_detection = ttk.Frame(stats_notebook, width=500, height=300)

stats_notebook.add(session_stats, text="Session Stats")
stats_notebook.add(alltime_stats, text="All-Time Stats")
stats_notebook.add(session_history, text="Session History")
stats_notebook.add(auto_detection, text="Auto-Detection")

# STATS NOTEBOOK SESSIONSTATS TAB #

session_stats.columnconfigure(7, weight=1)
ttk.Label(session_stats, image=gaard_pic).grid(column=1, row=0, sticky="NS", padx=10)
ttk.Label(session_stats, image=yasmine_pic).grid(column=2, row=0, sticky="NS", padx=10)
ttk.Label(session_stats, image=orpheus_pic).grid(column=3, row=0, sticky="NS", padx=10)
ttk.Label(session_stats, image=aranea_pic).grid(column=4, row=0, sticky="NS", padx=10)
ttk.Label(session_stats, image=anu_pic).grid(column=5, row=0, sticky="NS", padx=10)
ttk.Label(session_stats, image=nysha_pic).grid(column=6, row=0, sticky="NS", padx=10)

ttk.Label(session_stats, text="Tokens:").grid(column=0, row=1, sticky="W", pady=5)
ttk.Label(session_stats, text="Drop %:").grid(column=0, row=2, sticky="W", pady=5)

session_gaard_tokens = ttk.Label(session_stats, text="0", font=("Arial", FONT_SIZE))
session_gaard_tokens.grid(column=1, row=1, sticky=NS)
session_yasmine_tokens = ttk.Label(session_stats, text="0", font=("Arial", FONT_SIZE))
session_yasmine_tokens.grid(column=2, row=1, sticky=NS)
session_orpheus_tokens = ttk.Label(session_stats, text="0", font=("Arial", FONT_SIZE))
session_orpheus_tokens.grid(column=3, row=1, sticky=NS)
session_aranea_tokens = ttk.Label(session_stats, text="0", font=("Arial", FONT_SIZE))
session_aranea_tokens.grid(column=4, row=1, sticky=NS)
session_anu_tokens = ttk.Label(session_stats, text="0", font=("Arial", FONT_SIZE))
session_anu_tokens.grid(column=5, row=1, sticky=NS)
session_nysha_tokens = ttk.Label(session_stats, text="0", font=("Arial", FONT_SIZE))
session_nysha_tokens.grid(column=6, row=1, sticky=NS)

session_gaard_drop = ttk.Label(session_stats, text="0%", font=("Arial", FONT_SIZE))
session_gaard_drop.grid(column=1, row=2, sticky=NS)
session_yasmine_drop = ttk.Label(session_stats, text="0%", font=("Arial", FONT_SIZE))
session_yasmine_drop.grid(column=2, row=2, sticky=NS)
session_orpheus_drop = ttk.Label(session_stats, text="0%", font=("Arial", FONT_SIZE))
session_orpheus_drop.grid(column=3, row=2, sticky=NS)
session_aranea_drop = ttk.Label(session_stats, text="0%", font=("Arial", FONT_SIZE))
session_aranea_drop.grid(column=4, row=2, sticky=NS)
session_anu_drop = ttk.Label(session_stats, text="0%", font=("Arial", FONT_SIZE))
session_anu_drop.grid(column=5, row=2, sticky=NS)
session_nysha_drop = ttk.Label(session_stats, text="0%", font=("Arial", FONT_SIZE))
session_nysha_drop.grid(column=6, row=2, sticky=NS)

ttk.Label(session_stats, image=runs_pic).grid(column=1, row=3, sticky="NS", padx=10)
ttk.Label(session_stats, image=mimic_pic).grid(column=2, row=3, sticky="NS", padx=10)
ttk.Label(session_stats, image=mythic_mimic_pic).grid(column=3, row=3, sticky="NS", padx=10)
ttk.Label(session_stats, image=fragments_pic).grid(column=4, row=3, sticky="NS", padx=10)

ttk.Label(session_stats, text="Event:").grid(column=0, row=4, sticky="W", pady=5)
ttk.Label(session_stats, text="Event %:").grid(column=0, row=5, sticky="W", pady=5)

session_run_events = ttk.Label(session_stats, text="0", font=("Arial", FONT_SIZE))
session_run_events.grid(column=1, row=4, sticky=NS)
session_mimic_events = ttk.Label(session_stats, text="0", font=("Arial", FONT_SIZE))
session_mimic_events.grid(column=2, row=4, sticky=NS)
session_mythic_mimic_events = ttk.Label(session_stats, text="0", font=("Arial", FONT_SIZE))
session_mythic_mimic_events.grid(column=3, row=4, sticky=NS)
session_noreward_events = ttk.Label(session_stats, text="0", font=("Arial", FONT_SIZE))
session_noreward_events.grid(column=4, row=4, sticky=NS)

session_mimic_percent = ttk.Label(session_stats, text="0%", font=("Arial", FONT_SIZE))
session_mimic_percent.grid(column=2, row=5, sticky=NS)
session_mythic_mimic_percent = ttk.Label(session_stats, text="0%", font=("Arial", FONT_SIZE))
session_mythic_mimic_percent.grid(column=3, row=5, sticky=NS)
session_noreward_percent = ttk.Label(session_stats, text="0%", font=("Arial", FONT_SIZE))
session_noreward_percent.grid(column=4, row=5, sticky=NS)

ttk.Label(session_stats, text="Battles:").grid(column=5, row=4, sticky="E", pady=5)
session_battles = ttk.Label(session_stats, text="0")
session_battles.grid(column=6, row=4, sticky=N+S+W)

reset_session_button = ttk.Button(session_stats, text="Reset", bootstyle="info-outline", width=5, command=reset_session)
reset_session_button.grid(column=6, row=5, sticky=W, pady=2, padx=2)
ToolTip(reset_session_button, text="Reset all session stats.", bootstyle=(INFO, INVERSE), wraplength=200)

save_session_button = ttk.Button(session_stats, text="Save", bootstyle="info-outline", width=5, command=submit_session)
save_session_button.grid(column=5, row=5, sticky=E, pady=2, padx=2)
ToolTip(save_session_button, text="Save this session to Session History.", bootstyle=(INFO, INVERSE), wraplength=200)

# STATS NOTEBOOK ALLTIME STATS TAB #

alltime_stats.columnconfigure(7, weight=1)
ttk.Label(alltime_stats, image=gaard_pic).grid(column=1, row=0, sticky="NS", padx=10)
ttk.Label(alltime_stats, image=yasmine_pic).grid(column=2, row=0, sticky="NS", padx=10)
ttk.Label(alltime_stats, image=orpheus_pic).grid(column=3, row=0, sticky="NS", padx=10)
ttk.Label(alltime_stats, image=aranea_pic).grid(column=4, row=0, sticky="NS", padx=10)
ttk.Label(alltime_stats, image=anu_pic).grid(column=5, row=0, sticky="NS", padx=10)
ttk.Label(alltime_stats, image=nysha_pic).grid(column=6, row=0, sticky="NS", padx=10)

ttk.Label(alltime_stats, text="Tokens:").grid(column=0, row=1, sticky="W", pady=5)
ttk.Label(alltime_stats, text="Drop %:").grid(column=0, row=2, sticky="W", pady=5)

alltime_gaard_tokens = ttk.Label(alltime_stats, text="0", font=("Arial", FONT_SIZE))
alltime_gaard_tokens.grid(column=1, row=1, sticky=NS)
alltime_yasmine_tokens = ttk.Label(alltime_stats, text="0", font=("Arial", FONT_SIZE))
alltime_yasmine_tokens.grid(column=2, row=1, sticky=NS)
alltime_orpheus_tokens = ttk.Label(alltime_stats, text="0", font=("Arial", FONT_SIZE))
alltime_orpheus_tokens.grid(column=3, row=1, sticky=NS)
alltime_aranea_tokens = ttk.Label(alltime_stats, text="0", font=("Arial", FONT_SIZE))
alltime_aranea_tokens.grid(column=4, row=1, sticky=NS)
alltime_anu_tokens = ttk.Label(alltime_stats, text="0", font=("Arial", FONT_SIZE))
alltime_anu_tokens.grid(column=5, row=1, sticky=NS)
alltime_nysha_tokens = ttk.Label(alltime_stats, text="0", font=("Arial", FONT_SIZE))
alltime_nysha_tokens.grid(column=6, row=1, sticky=NS)

alltime_gaard_drop = ttk.Label(alltime_stats, text="0%", font=("Arial", FONT_SIZE))
alltime_gaard_drop.grid(column=1, row=2, sticky=NS)
alltime_yasmine_drop = ttk.Label(alltime_stats, text="0%", font=("Arial", FONT_SIZE))
alltime_yasmine_drop.grid(column=2, row=2, sticky=NS)
alltime_orpheus_drop = ttk.Label(alltime_stats, text="0%", font=("Arial", FONT_SIZE))
alltime_orpheus_drop.grid(column=3, row=2, sticky=NS)
alltime_aranea_drop = ttk.Label(alltime_stats, text="0%", font=("Arial", FONT_SIZE))
alltime_aranea_drop.grid(column=4, row=2, sticky=NS)
alltime_anu_drop = ttk.Label(alltime_stats, text="0%", font=("Arial", FONT_SIZE))
alltime_anu_drop.grid(column=5, row=2, sticky=NS)
alltime_nysha_drop = ttk.Label(alltime_stats, text="0%", font=("Arial", FONT_SIZE))
alltime_nysha_drop.grid(column=6, row=2, sticky=NS)

ttk.Label(alltime_stats, image=runs_pic).grid(column=1, row=3, sticky="NS", padx=10)
ttk.Label(alltime_stats, image=mimic_pic).grid(column=2, row=3, sticky="NS", padx=10)
ttk.Label(alltime_stats, image=mythic_mimic_pic).grid(column=3, row=3, sticky="NS", padx=10)
ttk.Label(alltime_stats, image=fragments_pic).grid(column=4, row=3, sticky="NS", padx=10)

ttk.Label(alltime_stats, text="Event:").grid(column=0, row=4, sticky="W", pady=5)
ttk.Label(alltime_stats, text="Event %:").grid(column=0, row=5, sticky="W", pady=5)

alltime_run_events = ttk.Label(alltime_stats, text="0", font=("Arial", FONT_SIZE))
alltime_run_events.grid(column=1, row=4, sticky=NS)
alltime_mimic_events = ttk.Label(alltime_stats, text="0", font=("Arial", FONT_SIZE))
alltime_mimic_events.grid(column=2, row=4, sticky=NS)
alltime_mythic_mimic_events = ttk.Label(alltime_stats, text="0", font=("Arial", FONT_SIZE))
alltime_mythic_mimic_events.grid(column=3, row=4, sticky=NS)
alltime_noreward_events = ttk.Label(alltime_stats, text="0", font=("Arial", FONT_SIZE))
alltime_noreward_events.grid(column=4, row=4, sticky=NS)

alltime_mimic_percent = ttk.Label(alltime_stats, text="0%", font=("Arial", FONT_SIZE))
alltime_mimic_percent.grid(column=2, row=5, sticky=NS)
alltime_mythic_mimic_percent = ttk.Label(alltime_stats, text="0%", font=("Arial", FONT_SIZE))
alltime_mythic_mimic_percent.grid(column=3, row=5, sticky=NS)
alltime_noreward_percent = ttk.Label(alltime_stats, text="0%", font=("Arial", FONT_SIZE))
alltime_noreward_percent.grid(column=4, row=5, sticky=NS)

ttk.Label(alltime_stats, text="Battles:").grid(column=5, row=4, sticky="E", pady=5)
alltime_battles = ttk.Label(alltime_stats, text="0")
alltime_battles.grid(column=6, row=4, sticky=N+S+W)

reset_alltime_button = ttk.Button(alltime_stats, text="Reset", bootstyle="info-outline", width=5, command=reset_alltime)
reset_alltime_button.grid(column=6, row=5, sticky=W, pady=2, padx=2)
ToolTip(reset_alltime_button, text="Reset All-Time Stats.", bootstyle=(INFO, INVERSE), wraplength=200)

# STATS NOTEBOOK SESSION HISTORY TAB #

colors = window.style.colors
session_table = Tableview(session_history, PRIMARY, [], [], paginated=True, autoalign=False, autofit=True, stripecolor=(colors.dark, None))
session_table.pack(fill=BOTH, expand=YES, padx=0, pady=0)
session_table.insert_column("end", "Date", anchor=CENTER, width=66, minwidth=66)
session_table.insert_column("end", "Runs", anchor=CENTER, width=40, minwidth=40)
session_table.insert_column("end", "Gaard", anchor=CENTER, width=45, minwidth=45)
session_table.insert_column("end", "Yasmine", anchor=CENTER, width=59, minwidth=59)
session_table.insert_column("end", "Orpheus", anchor=CENTER, width=59, minwidth=59)
session_table.insert_column("end", "Aranea", anchor=CENTER, width=51, minwidth=51)
session_table.insert_column("end", "Anu", anchor=CENTER, width=35, minwidth=30)
session_table.insert_column("end", "Nysha", anchor=CENTER, width=47, minwidth=47)
session_table.insert_column("end", "NR", anchor=CENTER, width=30, minwidth=30)
session_table.insert_column("end", "Mimic", anchor=CENTER, width=48, minwidth=48)
session_table.insert_column("end", "Hoard", anchor=CENTER, width=47, minwidth=47)

# STATS NOTEBOOK AUTO-DETECTION TAB #

autotoggle_var = IntVar()
autotoggle_var.set(0)
stop_check_thread = Event()
auto_toggle = ttk.Checkbutton(auto_detection, bootstyle="info-square-toggle", variable=autotoggle_var,
                                onvalue=1, offvalue=0, state="active", text="Auto-detection", command=start_thread)
auto_toggle.grid(column=0, row=0, sticky="W", padx=3, pady=10)
auto_submission_var = IntVar()
auto_submission_var.set(0)
auto_submit_toggle = ttk.Checkbutton(auto_detection, bootstyle="info-square-toggle", variable=auto_submission_var,
                                onvalue=1, offvalue=0, state="active", text="Auto-submit results")
auto_submit_toggle.grid(column=1, row=0, sticky="W", padx=3, pady=10)

auto_info = ttk.Label(auto_detection, text="STATUS: Inactive", font=("Arial", 10))
auto_info.grid(column=0, row=1, sticky="W", padx=3, pady=10, columnspan=3)
auto_log = ttk.Text(auto_detection, width=85, height=10, state="disabled")
auto_log.grid(column=0, row=3, sticky=NSEW, padx=3, pady=3, columnspan=3)

# TESTING # TESTING # TESTING #

# window_handle = FindWindow(None, "GemsofWar")
# window_rect = GetWindowRect(window_handle)
# win = pygetwindow.getWindowsWithTitle('GemsofWar')[0]
# win.activate()
# win.restore()
# sleep(1)
# win.size = (1200, 800)
# x = GetWindowRect(window_handle)[0] + 10
# y = GetWindowRect(window_handle)[1]
#
# screenshot = pyautogui.screenshot("img/test.png", region=(x+580, y+250, 40, 40))
# if locate('img/noexplore2020.png', x+180, y+630, 40, 40):
#     print("found")

"D in Difficulty in yellow to the bottom left: x+128, y+630, 40, 40"
"- in Difficulty in yellow to the bottom left: x+180, y+630, 40, 40"
"Title Mini in Mini Boss Battle popup window:  x+580, y+250, 40, 40"

load_session()
load_alltime()
load_session_history()
check_save_reset_buttons()
check_submit_button()
window.mainloop()
