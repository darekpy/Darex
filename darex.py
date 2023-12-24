import requests
import json
import re
import tkinter as tk
import threading
from tkinter import messagebox


def change_names():
    url_get = f"http://{ip_address}/api/v1/parent-devices/wtp"

    try:
        response = requests.get(url_get, headers=headers)
    except requests.exceptions.RequestException as e:
        print("Nieprawidłowy adres hosta.")
        input('Naciśnij klawisz "ENTER", aby opuścić aplikację\n')
        exit()

    response_json = response.json()

    if response.status_code != 200:
        print(response_json)
        print("Spróbuj ponownie.")
        input('Naciśnij klawisz "ENTER", aby opuścić aplikację\n')
        exit()

    pd_model_names = [["R-8s+z", "R-8s+", "R-8(b/z)", "R8b+", "R-8x", "R-8b", "R-8b+", "R-8h"], #Regulator0
                    ["WZ-02", "FZ-02", "PPZ-02"], #Roleta1
                    ["STT-869", "GX"]] #Głowica2

    wtp_names = {
        "aq_sensor": "Czujnik jakości powietrza",
        "blind_controller": "Roleta", 
        "button": "Przycisk", 
        "co2_sensor": "Czujnik CO", 
        "humidity_sensor": "Czujnik wilgotności", 
        "iaq_sensor": "Wewnętrzny czujnik jakości powietrza",
        "light_sensor": "Czujnik natężenia światła", 
        "motion_sensor": "Czujnik ruchu", 
        "opening_sensor": "Czujnik otwarcia", 
        "pressure_sensor": "Czujnik ciśnienia", 
        "radiator_actuator": "Głowica", 
        "relay": "Przekaźnik", 
        "smoke_sensor": "Czujnik dymu", 
        "flood_sensor": "Czujnik zalania", 
        "temperature_regulator": "Regulator temperatury", 
        "temperature_sensor": "Czujnik temperatury", 
        "two_state_input_sensor": "Wejście dwustanowe"
    }

    data_length = len(response_json["data"])

    pd_amount = data_length

    pd_count = 0
    for i in range(data_length):
        #Progress bar
        pd_count += 1
        pd_count_percentage = (pd_count / pd_amount) * 100
        print("Zmiana nazw: ", int(pd_count_percentage), "/100%", end="\r")

        parent_device_name = response_json["data"][i]["name"]

        devices_dict_length = len(response_json["data"][i]["devices"])
        
        for k in range(devices_dict_length):
            wtp_device_type = response_json["data"][i]["devices"][k]["type"]

            if wtp_device_type in wtp_names:
                wtp_device_type_pl = wtp_names.get(wtp_device_type)
                if wtp_device_type_pl == "Przekaźnik":
                    wtp_new_name = parent_device_name + " " + wtp_device_type_pl + str(k)
                else:
                    wtp_new_name = parent_device_name + " " + wtp_device_type_pl

                length = len(wtp_new_name)
                if length > 40:
                    wtp_new_name = wtp_new_name[:40]
            else:
                wtp_new_name = parent_device_name + " -"

            wtp_id = response_json["data"][i]["devices"][k]["id"]

            url = f"http://{ip_address}/api/v1/devices/wtp/{wtp_id}"

            payload = json.dumps({
                "name": wtp_new_name
            })

            requests.request("PATCH", url, headers=headers, data=payload)

        parent_device_model = response_json["data"][i]["model"]
        parent_device_id = response_json["data"][i]["id"]

        if parent_device_model in pd_model_names[0]: pd_type = "Regulator "
        elif parent_device_model in pd_model_names[1]: pd_type = "Roleta "
        elif parent_device_model in pd_model_names[2]: pd_type = "Głowica "
        else: pd_type = ""

        new_parent_device_name = pd_type + parent_device_name

        url3 = f"http://{ip_address}/api/v1/parent-devices/wtp/{parent_device_id}"

        payload3 = json.dumps({
            "name": new_parent_device_name
        })

        requests.request("PATCH", url3, headers=headers, data=payload3)    

#--------------------------------------------------------------------------------------------------------------------------------------   

def create_thermostat():
    url2 = f"http://{ip_address}/api/v1/devices/virtual"

    url_get2 = f"http://{ip_address}/api/v1/parent-devices/wtp"


    try:
        response = requests.get(url_get2, headers=headers)
    except requests.exceptions.RequestException as e:
        print("Nieprawidłowy adres hosta.")
        input('Naciśnij klawisz "ENTER", aby opuścić aplikację\n')
        exit()

    response_json = response.json()

    if response.status_code != 200:
        print(response_json)
        print("Spróbuj ponownie.")
        input('Naciśnij klawisz "ENTER", aby opuścić aplikację\n')
        exit()


    data = {  #
        "type": "thermostat",
        "variant": "generic",
        "class": "virtual",
        "name": "My thermostat1",
        "icon": "",
        "messages": [],
        "labels": [],
        "tags": [],
        "room_id": None,
        "state": False,
        "temperature": 0,
        "floor_temperature": 0,
        "humidity": 0,
        "target_temperature": 210,
        "target_temperature_mode": {
            "current": "constant",
            "remaining_time": 0
        },
        "target_temperature_minimum": 50,
        "target_temperature_maximum": 350,
        "hysteresis": 2,
        "mode": "heating",
        "overheat_protection": {
            "active": False,
            "enabled": False,
            "range": 30
        },
        "sigma_control": {
            "enabled": True,
            "range": 10,
            "opening_factor": 0
        },
        "floor_control": {
            "enabled": False,
            "lower_target_temperature": 50,
            "upper_target_temperature": 400,
            "hysteresis": 2,
            "condition": "optimal"
        },
        "associations": {
            "room_temperature_sensor": {
                "id": 0,
                "class": ""
            },
            "floor_temperature_sensor": {
                "id": 0,
                "class": ""
            },
            "humidity_sensor": {
                "id": 0,
                "class": ""
            },
            "temperature_regulator": {
                "id": 0,
                "class": ""
            },
            "radiator_actuators": [],
            "relays": [],
            "opening_sensors": []
        },
        "antifrost_protection": False,
        "opening_sensors_delay": 0,
        "software_status": "up_to_date",
        "visible": True,
        "color": "#0072c3",
        "voice_assistant_device_type": "thermostat",
        "is_window_open": False,
        "confirm_time_mode": True
    }


    associations_list = ["temperature_sensor", "humidity_sensor", "temperature_regulator", "radiator_actuator", "relay", "opening_sensor"]


    data_length = len(response_json["data"])
    thermostat_names = []

    for d in range(data_length):
        pd_name = response_json["data"][d]["name"]

        pattern= r'\b(?:[A-Za-z]+\s*)?(\d+)(?:[A-Za-z]+\s*)?\b'
        matches = re.findall(pattern, pd_name)
        if matches:
            parent_device_name = matches[0]
        thermostat_names.append(parent_device_name)

    thermostat_names_noduplicates = list(dict.fromkeys(thermostat_names))
    
    thermostat_amount = len(thermostat_names_noduplicates) #Zliczanie termostatów

    thermostat_count = 0
    for o in range(len(thermostat_names_noduplicates)):
        #Progress bar
        thermostat_count += 1
        thermostat_count_percentage = (thermostat_count / thermostat_amount) * 100
        print("Tworzenie termostatów: ", int(thermostat_count_percentage), "/100%", end="\r")

        thermostat_name = thermostat_names_noduplicates[o]
        data["name"] = f"Termostat {thermostat_name}"

        for i in range(data_length):
            devices_dict_length = len(response_json["data"][i]["devices"])

            for k in range(devices_dict_length):
                wtp_device_name = response_json["data"][i]["devices"][k]["name"]

                pattern= r'\b(?:[A-Za-z]+\s*)?(\d+)(?:[A-Za-z]+\s*)?\b'
                matches = re.findall(pattern, wtp_device_name)
                if matches:
                    room_number = matches[0]
                    if room_number == thermostat_name:
                        wtp_device_type = response_json["data"][i]["devices"][k]["type"]
                        if wtp_device_type in associations_list:
                            wtp_device_id = response_json["data"][i]["devices"][k]["id"]
                            if wtp_device_type == associations_list[0]:
                                data["associations"]["room_temperature_sensor"]["id"] = wtp_device_id
                                data["associations"]["room_temperature_sensor"]["class"] = "wtp"
                            elif wtp_device_type == associations_list[1]:
                                data["associations"]["humidity_sensor"]["id"] = wtp_device_id
                                data["associations"]["humidity_sensor"]["class"] = "wtp"
                            elif wtp_device_type == associations_list[2]:
                                data["associations"]["temperature_regulator"]["id"] = wtp_device_id
                                data["associations"]["temperature_regulator"]["class"] = "wtp"
                            elif wtp_device_type == associations_list[3]:
                                upd_dict1 = {"id": wtp_device_id, "class": "wtp"}
                                data["associations"]["radiator_actuators"].append(upd_dict1)
                            elif wtp_device_type == associations_list[4]:
                                upd_dict2 = {"id": wtp_device_id, "class": "wtp"}
                                data["associations"]["relays"].append(upd_dict2)
                            elif wtp_device_type == associations_list[5]:
                                upd_dict3 = {"id": wtp_device_id, "class": "wtp"}
                                data["associations"]["opening_sensors"].append(upd_dict3)


        payload = json.dumps(data)

        requests.request("POST", url2, headers=headers, data=payload)

        data["associations"]["room_temperature_sensor"]["id"] = 0
        data["associations"]["room_temperature_sensor"]["class"] = ""

        data["associations"]["humidity_sensor"]["id"] = 0
        data["associations"]["humidity_sensor"]["class"] = ""

        data["associations"]["temperature_regulator"]["id"] = 0
        data["associations"]["temperature_regulator"]["class"] = ""

        data["associations"]["radiator_actuators"] = []

        data["associations"]["relays"] = []

        data["associations"]["opening_sensors"] = []

#---------------------------------------------------------------------------------------------------------------------------------------------

def create_rooms():
    url_get_pd = f"http://{ip_address}/api/v1/parent-devices/wtp"
    url_get_vt = f"http://{ip_address}/api/v1/devices/virtual"
    
    url_rooms = f"http://{ip_address}/api/v1/rooms"

    room_data = {
        "name": "My room",
        "icon": "button",
        "color": "blue",
        "scenes": [],
        "devices": [],
        "has_error": False,
        "has_warning": False,
        "is_heating": False,
        "is_cooling": False,
        "labels": [],
        "floor_id": None,
        "is_window_open": False
    }

    #Request dla parent device
    response_pd = requests.get(url_get_pd, headers=headers)
    response_json_pd = response_pd.json()

    data_length = len(response_json_pd["data"])
    room_names = []

    for d in range(data_length):
        pd_name = response_json_pd["data"][d]["name"]

        pattern= r'\b(?:[A-Za-z]+\s*)?(\d+)(?:[A-Za-z]+\s*)?\b'
        matches = re.findall(pattern, pd_name)
        if matches:
            parent_device_name = matches[0]
        room_names.append(parent_device_name)

    room_names_noduplicates = list(dict.fromkeys(room_names))
    
    #Request dla urządzeń virtualnych
    response_vt = requests.get(url_get_vt, headers=headers)
    response_json_vt = response_vt.json()

    vt_dict = {}
    for i in range(len(response_json_vt["data"])):
        for v in range(len(response_json_vt["data"][i])):
            vt_name = response_json_vt["data"][i]["name"]
            vt_id = response_json_vt["data"][i]["id"]
            upd_dict_vt = {vt_name: vt_id}
            vt_dict.update(upd_dict_vt)


    room_count = 0
    for o in range(len(room_names_noduplicates)):
        #Progress bar
        room_count += 1
        room_count_percentage = (room_count / len(room_names_noduplicates)) * 100
        print("Tworzenie pomieszczeń: ", int(room_count_percentage), "/100%", end="\r")

        room_name = room_names_noduplicates[o]
        room_data["name"] = room_name

        #Dodawanie urządzeń wtp do pokojów
        for i in range(data_length):
            devices_dict_length = len(response_json_pd["data"][i]["devices"])
            
            for k in range(devices_dict_length):
                wtp_device_name = response_json_pd["data"][i]["devices"][k]["name"]
                wtp_device_id = response_json_pd["data"][i]["devices"][k]["id"]

                pattern= r'\b(?:[A-Za-z]+\s*)?(\d+)(?:[A-Za-z]+\s*)?\b'
                matches = re.findall(pattern, wtp_device_name)
                if matches:
                    room_number = matches[0]
                    if room_number == room_name:
                        upd_dict_room = {"class": "wtp", "id": wtp_device_id}
                        room_data["devices"].append(upd_dict_room)

        
        #Dodawanie termostatów do pokojów
        thermostat_room_string = f"Termostat {room_name}"
        if thermostat_room_string in vt_dict:
            upd_dict_room_vt = {"class": "virtual", "id": vt_dict.get(thermostat_room_string)}
            room_data["devices"].append(upd_dict_room_vt)


        #Tworzenie pokojów
        payload_room = json.dumps(room_data)
            
        if room_data["name"] != "Test":
            requests.request("POST", url_rooms, headers=headers, data=payload_room)
        room_data["devices"] = []


def option1():
    text_output.delete(1.0, tk.END)
    thread = threading.Thread(target=change_names)
    thread.start()

def option2():
    text_output.delete(1.0, tk.END)
    thread = threading.Thread(target=create_thermostat)
    thread.start()

def option3():
    text_output.delete(1.0, tk.END)
    thread = threading.Thread(target=create_rooms)
    thread.start()

def openOptionWindow(ip_entry, token_entry):
    global ip_address
    ip_address = ip_entry.get()
    global token
    token = token_entry.get()

    url_check = f"http://{ip_address}/api/v1/parent-devices/wtp"

    global headers
    headers={
        "Content-Type": "application/json",
        "Authorization": token
    }

    try:
        response_entry = requests.get(url_check, headers=headers)
        response_entry.raise_for_status()

        input_window.destroy()

        root = tk.Tk()
        root.geometry("700x400")
        root.title("Darex")
        root.configure(bg="#012749")

        menu_item1 = tk.Button(root, text="Zmiana nazw", command=option1, width=20)
        menu_item1.grid(row=0, column=0, padx=5, pady=2, sticky=tk.W)

        menu_item2 = tk.Button(root, text="Tworzenie termostatów", command=option2, width=20)
        menu_item2.grid(row=1, column=0, padx=5, pady=2, sticky=tk.W)

        menu_item3 = tk.Button(root, text="Tworzenie pomieszczeń", command=option3, width=20)
        menu_item3.grid(row=2, column=0, padx=5, pady=2, sticky=tk.W)

        global text_output #Text field
        text_output = tk.Text(root, wrap=tk.WORD, height=20, width=60)
        text_output.grid(row=0, column=1, rowspan=10, padx=5, pady=10, sticky=tk.W + tk.E + tk.N + tk.S)

        root.mainloop()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", "Błędny adres lub token.")


input_window = tk.Tk()
input_window.geometry("700x400")
input_window.title("Start")
input_window.configure(bg="#012749")

ip_label = tk.Label(input_window, text="Wprowadź adres IP (np. 10.42.0.1):")
ip_entry = tk.Entry(input_window, width=75)

token_label = tk.Label(input_window, text="Wklej token:")
token_entry = tk.Entry(input_window, width=75)

submit_button = tk.Button(input_window, text="ENTER", command=lambda: openOptionWindow(ip_entry, token_entry))

ip_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
ip_entry.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

token_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
token_entry.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)

submit_button.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)

input_window.mainloop()