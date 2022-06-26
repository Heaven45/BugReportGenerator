import PySimpleGUI as sg
import pyperclip

sg.theme('dark grey 8')

devices_conf = "devices.conf"
android_v_conf = "android_v.conf"

devices = {}
android_versions = {}
branches = {"Live": False, "Dev": False, "Release": False}
repro_rates = {"1/4": False, "2/4": False, "3/4": False, "4/4": False}
dev_ver = {}

device = ""
android_version = ""
branch = ""
repro_rate = ""

with open(devices_conf, "r") as f:
    for line in f:
        line = line.replace("\n", "")
        if not (line == " " or line == ""):
            if not line[0] == "#":
                devices.update({line: False})

with open(android_v_conf, "r") as f:
    for line in f:
        line = line.replace("\n", "")
        if not (line == " " or line == ""):
            if not line[0] == "#":
                android_versions.update({line: False})


def get_devices_list():
    list = ""
    for device in dev_ver:
        list += device[:-12] + "\n"
    return list


def generate_layout():
    layout = [[
        sg.Frame('Parameters',
                 [[sg.Text("Repro rate:", font=('Arial', 15))],
                  [sg.Checkbox("1/4", key="1/4", enable_events=True, font=('Arial', 12))],
                  [sg.Checkbox("2/4", key="2/4", enable_events=True, font=('Arial', 12))],
                  [sg.Checkbox("3/4", key="3/4", enable_events=True, font=('Arial', 12))],
                  [sg.Checkbox("4/4", key="4/4", enable_events=True, font=('Arial', 12))],
                  [sg.Text("Build used:", font=('Arial', 15))],
                  [sg.Input(key="build_version", size=(5, None))],
                  [sg.Text("Device: ", size=(5, 1), font=('Arial', 15))],
                  [sg.Combo(list(devices.keys()), key='device', size=(21, 1))],
                  [sg.Text("Branch:", font=('Arial', 15))],
                  [sg.Checkbox("Live", key="Live", enable_events=True, font=('Arial', 12))],
                  [sg.Checkbox("Dev", key="Dev", enable_events=True, font=('Arial', 12))],
                  [sg.Checkbox("Release", key="Release", enable_events=True, font=('Arial', 12))],
                  [sg.Text("", size=(5, 4))]
                  ], font=('Arial', 15),
                 vertical_alignment='top'),

        sg.Frame('Devices added', [[sg.Text(get_devices_list(), key="device_list", font=('Arial', 12), size=(20, 19))]],
                 font=('Arial', 15), vertical_alignment='top')
    ],
        [sg.Frame('Report', [[sg.Multiline(generate_message(), key="report", size=(42, 10), font=('Arial', 12))]],
                  font=('Arial', 15))],
        [sg.OK(button_text="Commit", font=('Arial', 15)), sg.Button(button_text="Copy", key="Copy", font=('Arial', 15)),
         sg.Cancel(font=('Arial', 15)), sg.Button(button_text="Clear", key="Clear", font=('Arial', 15))]]

    return layout


def parse_window_data(values):
    device = ""
    android_v = ""
    if "device" in values:
        device = values["device"]
    if "build_version" in values:
        build_v = values["build_version"]

    if not (device == "" and android_v == ""):
        if device in dev_ver:
            if not android_v in dev_ver[device]:
                dev_ver[device].append(android_v)
        else:
            dev_ver.update({device: [android_v]})
    for branch in branches:
        branches[branch] = values[branch]
    for rate in repro_rates:
        repro_rates[rate] = values[rate]
    return build_v


def clear_fields():
    lists_to_clear = [devices, android_versions, dev_ver]
    for list in lists_to_clear:
        list.clear()

    keys_to_clear = ["build_version", "device", "device_list", "report"]
    for key in keys_to_clear:
        window[key]('')

    window["Dev"].update(False)
    window["Release"].update(False)


def generate_message():
    device = ""
    for device_item in dev_ver:
        device += " %s," % (device_item)
    device = device[:-1]
    branch = ""
    for branch_item in branches:
        if branches[branch_item]:
            branch += branch_item + ", "
    branch = branch[:-2]
    rate = ''
    for repro_item in repro_rates:
        if repro_rates[repro_item]:
            rate += repro_item + ", "
    rate = rate[:-2]

    message = "**Steps to reproduce:**\n\n1.\n1.\n\n**Observed result:** \n\n\n**Expected result:**\n\n\n**Repro rate:**\n%s\n\n**Devices used:**\n%s\n\n**Branch:**\n%s\n\n**Build used:**\n%s" % (
        rate, device, branch, build_v)
    return message


if __name__ == '__main__':
    release_v = ""
    build_v = ""
    layout = generate_layout()
    window = sg.Window('Bug Report Generator', layout, finalize=True)
    while True:
        event, values = window.read()
        if event in (sg.OK(), "Commit"):
            build_v = parse_window_data(values)
            window["device_list"].update(get_devices_list())
            window["report"].update(generate_message())
        if event in (sg.Button, "Copy"):
            report = generate_message()
            pyperclip.copy(report)
        if event in (sg.Button, "Clear"):
            clear_fields()
        if event in (sg.WIN_CLOSED, 'Cancel'):
            break
    report = generate_message()
    print(report)
    window.close()
    pyperclip.copy(report)
