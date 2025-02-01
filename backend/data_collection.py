# backend/data_collection.py
import atexit
import datetime
import json
import os
import random
import subprocess
import sys
import threading
import time

import pynput
from pynput.keyboard import Key, KeyCode, Listener

DATA_DIR = "data_collection"
os.makedirs(DATA_DIR, exist_ok=True)


class DataCollector:
    def __init__(self, agent_id):
        self.agent_id = agent_id
        self.start_time = time.time()
        self.data = []
        self.current_entry = {}
        self.modifier_pressed = False
        self.recording = False
        self.stop_event = threading.Event()
        self.last_batch_end_time = None
        self.lock = threading.Lock()

    def get_active_window_title(self):
        try:
            if sys.platform == "win32":
                import win32gui

                window = win32gui.GetForegroundWindow()
                return win32gui.GetWindowText(window)
            elif sys.platform == "darwin":
                # Requires 'appscript' to be installed
                from appscript import app, mactypes

                return (
                    app("System Events")
                    .processes.where(its.frontmost == True)
                    .first.windows.first.name()
                )
            elif sys.platform.startswith("linux"):
                # Requires 'xprop' and 'xdotool' to be installed
                process = subprocess.Popen(
                    [
                        "xprop",
                        "-id",
                        subprocess.check_output(["xdotool", "getactivewindow"])
                        .decode()
                        .strip(),
                        "WM_NAME",
                    ],
                    stdout=subprocess.PIPE,
                )
                stdout, _ = process.communicate()
                return stdout.decode().strip().split("= ")[-1].strip('"')
        except Exception as e:
            print(f"Error getting active window title: {e}")
        return "Unknown Window"

    def on_press(self, key):
        if key == Key.ctrl_r:
            self.modifier_pressed = True
        elif self.modifier_pressed and key == KeyCode.from_char("r"):
            if not self.recording:
                self.start_recording()
            else:
                self.stop_recording_and_trigger_finetuning()
        elif key == Key.esc:
            print("esc detected - stopping listener")
            self.stop_event.set()
            return False
        else:
            self.modifier_pressed = False
        if self.recording:
            timestamp = time.time()
            active_window = self.get_active_window_title()
            self.current_entry = {
                "timestamp": timestamp,
                "event": "keypress",
                "key": str(key),
                "active_window": active_window,
            }
            self.data.append(self.current_entry)

    def on_release(self, key):
        if key == Key.ctrl_r:
            self.modifier_pressed = False

    def start_recording(self):
        with self.lock:
            if not self.recording:
                print("Starting data collection...")
                self.recording = True
                self.start_time = time.time()
                self.data = []  # Reset data

    def stop_recording_and_trigger_finetuning(self):
        with self.lock:
            if self.recording:
                self.recording = False
                print("Stopping data collection...")
                self.last_batch_end_time = time.time()
                self.save_data()
                self.trigger_fine_tuning()

    def save_data(self):
        if not self.data:
            return
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        data_file_path = os.path.join(
            DATA_DIR, f"data_{self.agent_id}_{timestamp}.json"
        )
        with open(data_file_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4)
        print(f"Data collected and saved to {data_file_path}")
        self.data = []  # Reset data after saving

    def trigger_fine_tuning(self):
        """Triggers fine-tuning for the specified agent using the collected data."""
        print(
            f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Triggering fine-tuning for agent {self.agent_id}..."
        )
        try:
            # Here, instead of reading from a file, we're using the collected data directly
            fine_tuning_data = self.data
            # Ensure fine_tuning_data is not empty
            if not fine_tuning_data:
                print("No data to fine-tune with.")
                return
            response = requests.post(
                f"http://localhost:5000/api/agents/{self.agent_id}/fine_tune",
                json={"data": fine_tuning_data},
                timeout=30,
            )
            response.raise_for_status()
            print(
                f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Fine-tuning triggered successfully."
            )
        except requests.exceptions.RequestException as e:
            print(f"Error triggering fine-tuning: {e}")
        except Exception as e:
            print(f"An unexpected error occurred during fine-tuning: {e}")

    def run(self):
        with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            print("Press Ctrl+R to start/stop recording, Esc to quit.")
            listener.join()
            if not self.stop_event.is_set():
                print("Stopping data collection process...")
                self.stop_recording_and_trigger_finetuning()


def start_data_collection(agent_id):
    collector = DataCollector(agent_id)
    collector.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run data collection for fine-tuning.")
    parser.add_argument(
        "--agent_id",
        type=str,
        required=True,
        help="ID of the agent for which data is being collected.",
    )
    args = parser.parse_args()
    start_data_collection(args.agent_id)
