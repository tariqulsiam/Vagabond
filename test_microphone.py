#! /usr/bin/python3
import argparse
import os
import queue
import re
import sounddevice as sd
import vosk
import sys
import pyttsx3
import json
import time
from chatgui import *
import subprocess


def send_interrupt():

    string = subprocess.check_output(
        "pidof python3", shell=True, executable="/bin/bash"
    )
    string = string.decode("utf-8").split()

    cmdline = []

    for i in string:
        cmdline.append("cat /proc/" + i + "/cmdline")
    for i in cmdline:
        tmp = subprocess.check_output(i, shell=True, executable="/bin/bash")
        tmp = tmp.decode("utf-8")
        if "walk.py" in tmp:
            for j in i.split("/"):
                if j.isdigit():
                    cmd = "kill -SIGINT " + str(j)

    subprocess.run(cmd, shell=True, executable="/bin/bash")


engine = pyttsx3.init()





def speak(sentence):
    engine.say(sentence)
    engine.runAndWait()


q = queue.Queue()


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))


parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    "-l",
    "--list-devices",
    action="store_true",
    help="show list of audio devices and exit",
)
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser],
)
parser.add_argument(
    "-f",
    "--filename",
    type=str,
    metavar="FILENAME",
    help="audio file to store recording to",
)
parser.add_argument(
    "-m", "--model", type=str, metavar="MODEL_PATH", help="Path to the model"
)
parser.add_argument(
    "-d", "--device", type=int_or_str, help="input device (numeric ID or substring)"
)
parser.add_argument("-r", "--samplerate", type=int, help="sampling rate")
args = parser.parse_args(remaining)


def reminder(param_messsage):
    expected_hours = {
        "one": "01",
        "two": "02",
        "three": "03",
        "four": "04",
        "five": "05",
        "six": "06",
        "seven": "07",
        "eight": "08",
        "nine": "09",
        "ten": "10",
        "eleven": "11",
        "twelve": "12",
    }
    expected_minutes = {
        "five": "05",
        "ten": "10",
        "fifteen": "15",
        "twenty": "20",
        "twenty five": "25",
        "thirty": "30",
        "thirty five": "35",
        "forty": "40",
        "forty five": "45",
        "fifty": "50",
        "fifty five": "55",
    }
    tokens = [
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
        "ten",
        "eleven",
        "twelve",
        "fifteen",
        "twenty",
        "thirty",
        "forty",
        "fifty",
        "am",
        "pm",
    ]
    expected_time = ["am", "pm"]
    param_messsage = param_messsage.split(" ")
    print(param_messsage)
    detected_time = ""
    detected_period_of_time = ""
    refined_message = []
    for word in param_messsage:
        word = word.lower()
        if word in tokens:
            refined_message.append(word)
    print(refined_message)
    for word in refined_message:
        if word in expected_hours.keys():
            detected_time += expected_hours[word] + ":"
    detected_period_of_time += refined_message[-1]
    print(refined_message[-1])
    del refined_message[-1]
    if len(refined_message) == 1:
        tmp = refined_message[0]
        detected_time += expected_minutes[tmp] + " " + detected_period_of_time
    elif len(refined_message) == 2:
        tmp = refined_message[0] + " " + refined_message[1]
        detected_time = expected_minutes[tmp] + " " + detected_period_of_time

    print(detected_time)


try:
    if args.model is None:
        args.model = "model"
    if not os.path.exists(args.model):
        print(
            "Please download a model for your language from https://alphacephei.com/vosk/models"
        )
        print("and unpack as 'model' in the current folder.")
        parser.exit(0)
    if args.samplerate is None:
        device_info = sd.query_devices(args.device, "input")
        # soundfile expects an int, sounddevice provides a float:
        args.samplerate = int(device_info["default_samplerate"])

    model = vosk.Model(args.model)

    if args.filename:
        dump_fn = open(args.filename, "wb")
    else:
        dump_fn = None

    with sd.RawInputStream(
        samplerate=args.samplerate,
        blocksize=2000,
        device=args.device,
        dtype="int16",
        channels=1,
        callback=callback,
    ):
        print("#" * 80)
        print("Press Ctrl+C to stop the recording")
        print("#" * 80)

        rec = vosk.KaldiRecognizer(model, args.samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                tmp = rec.Result()
                raw_json = json.loads(tmp)
                message = raw_json["text"]  # result that is what I need
                if message != "":
                    bot_response_list = chatbot_response(message)
                    bot_message = bot_response_list[1]
                    bot_message = str(bot_message)
                    if bot_response_list[0] == 1:
                        speak(bot_message)
                        exit()
                    # elif not bot_response_list[0]:
                    #     speak(bot_message)
                    elif bot_response_list[0] == 2:
                        reminder(message)
                        speak(bot_message)
                    elif bot_response_list[0] == 3:
                        speak(message)
                        process = subprocess.Popen(
                            "/usr/bin/python3 /home/pi/walk/walk.py", shell=True, executable="/bin/bash")
                        speak("Walk function initialized successfully!")
                    elif bot_response_list[0] == 4:
                        speak(message)
                        send_interrupt()
                    else:
                        speak(bot_message)

                else:
                    print("text: " + message)

            else:
                tmp = rec.PartialResult()
                raw_json = json.loads(tmp)
                message = str("partial: " + raw_json["partial"])
                print(message)
            if dump_fn is not None:
                dump_fn.write(data)


except KeyboardInterrupt:
    print("\nDone")
    parser.exit(0)
except Exception as e:
    parser.exit(type(e).__name__ + ": " + str(e))
