# backend/agents.py
import datetime
import json
import os
import shutil
import subprocess
import time
import uuid

import requests
from huggingface_hub import snapshot_download


class LlmCoderAgent:
    def __init__(self, ollama_base_url="http://localhost:11434"):
        self.agent_id = str(uuid.uuid4())
        self.ollama_base_url = ollama_base_url
        self.model = "mistral"  # Default model
        self.status = "Idle"
        self.last_activity = datetime.datetime.now()

    def get_suggestion(self, prompt):
        """Gets an LLM suggestion from Ollama."""
        self.status = "Getting suggestion"
        self.last_activity = datetime.datetime.now()
        try:
            response = requests.post(
                f"{self.ollama_base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                },
                timeout=30,
            )
            response.raise_for_status()
            suggestion = ""
            for line in response.iter_lines():
                if line:
                    decoded_line = json.loads(line)
                    if "response" in decoded_line:
                        suggestion += decoded_line["response"]
                    elif "error" in decoded_line:
                        print(decoded_line["error"])
            self.status = "Idle"
            self.last_activity = datetime.datetime.now()
            return suggestion.strip()
        except requests.exceptions.RequestException as e:
            print(f"Error communicating with Ollama: {e}")
            self.status = "Error"
            self.last_activity = datetime.datetime.now()
            return "Error: Could not get suggestion from LLM."

    def fine_tune(self, data):
        """Initiates fine-tuning with the given data."""
        self.status = "Fine-tuning"
        self.last_activity = datetime.datetime.now()
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        fine_tuning_dir = os.path.join(
            "/app/projects", self.agent_id, f"fine_tuning_{timestamp}"
        )
        os.makedirs(fine_tuning_dir, exist_ok=True)
        # Save the fine-tuning data to a file
        data_file_path = os.path.join(fine_tuning_dir, "fine_tuning_data.json")
        with open(data_file_path, "w", encoding="utf-8") as f:
            json.dump(data, f)
        # Construct the command to run the fine-tuning script
        # Assuming 'finetune.py' is in the same directory as 'agents.py'
        finetune_script_path = os.path.join(os.path.dirname(__file__), "finetune.py")
        # Construct the command to run the fine-tuning script
        fine_tune_command = [
            "python",
            finetune_script_path,
            "--data_file",
            data_file_path,
            "--output_dir",
            fine_tuning_dir,
            "--agent_id",
            self.agent_id,
        ]
        # Start the fine-tuning process
        try:
            subprocess.run(
                fine_tune_command,
                cwd=os.path.dirname(finetune_script_path),
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            self.status = "Idle"
            self.last_activity = datetime.datetime.now()
            return f"Fine-tuning completed for agent {self.agent_id}."
        except subprocess.CalledProcessError as e:
            self.status = "Error"
            self.last_activity = datetime.datetime.now()
            print(f"Error during fine-tuning: {e}")
            print(f"Stdout: {e.stdout.decode()}")
            print(f"Stderr: {e.stderr.decode()}")
            return f"Error during fine-tuning for agent {self.agent_id}: {e.stderr.decode()}"

    def convert_to_ollama(self, base_model, ollama_name):
        """Converts a Hugging Face model to an Ollama model."""
        self.status = "Converting to Ollama"
        self.last_activity = datetime.datetime.now()
        h = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        if not h:
            return {"status": "OLLAMA_HOST not set"}
        t_dir = f"/tmp/{ollama_name}"
        os.makedirs(t_dir, exist_ok=True)
        try:
            snapshot_download(
                base_model,
                local_dir=t_dir,
                local_dir_use_symlinks=False,
                token=os.getenv("HF_TOKEN"),
            )
            modelfile_content = f"""
            FROM scratch
            FROM {base_model}
            TEMPLATE \"\"\"{{{{ if .System }}}}{{{{ .System }}}}{{{{ end }}{{{{ .Prompt }}}}\"\"\"
            SYSTEM \"\"\"You are a highly capable and versatile AI assistant. Your primary goal is to provide helpful, informative, and comprehensive responses to user queries. You are designed to be broadly knowledgeable and are adept at understanding and answering questions across a wide range of topics. Strive to be clear, concise, and insightful in your responses. When appropriate, provide examples or elaborate on your answers to ensure clarity and thoroughness. You are an AI Assistant.\"\"\"
            PARAMETER stop \\"<s>\\"
            PARAMETER stop \\"<|endoftext|>\\"
            PARAMETER stop \\"<filename>\\"
            PARAMETER stop \\"<file_separator>\\"
            PARAMETER stop \\"[/INST]\\"[[:space:]]
            """.strip()
            modelfile_path = os.path.join(t_dir, "Modelfile")
            with open(modelfile_path, "w", encoding="utf-8") as f:
                f.write(modelfile_content)
            cmd = ["ollama", "create", ollama_name, "-f", modelfile_path]
            process = subprocess.Popen(
                cmd,
                env={"OLLAMA_HOST": h},
                cwd=t_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            process.wait()
            if process.returncode == 0:
                shutil.rmtree(t_dir)
                self.status = "Idle"
                self.last_activity = datetime.datetime.now()
                return {
                    "status": "exported",
                    "ollama_model": ollama_name,
                    "target": h,
                }
            else:
                err_msg = process.stderr.read().decode()
                shutil.rmtree(t_dir)
                self.status = "Error"
                self.last_activity = datetime.datetime.now()
                return {
                    "status": "failed",
                    "ollama_model": ollama_name,
                    "target": h,
                    "error": err_msg,
                }
        except Exception as e:
            shutil.rmtree(t_dir)
            self.status = "Error"
            self.last_activity = datetime.datetime.now()
            return {
                "status": "error",
                "ollama_model": ollama_name,
                "error": str(e),
            }

    def get_status(self):
        """Returns the current status of the agent."""
        return self.status

    def get_last_activity(self):
        """Returns the last activity time of the agent."""
        return self.last_activity.strftime("%Y-%m-%d %H:%M:%S")
