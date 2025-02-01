# backend/app.py
import json
import logging
import os
import subprocess
import uuid

import requests
from flask import Flask, abort, jsonify, request, send_from_directory
from flask_cors import CORS
from huggingface_hub import snapshot_download
from werkzeug.exceptions import HTTPException

from .agents import LlmCoderAgent
from .knowledge_graph import KnowledgeGraph

app = Flask(__name__)
CORS(app)
# Logging setup with file handler
LOG_FILE = "app.log"
logging.basicConfig(
    level=logging.INFO,
    filename=LOG_FILE,
    filemode="a+",
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)
# Ensure project directories exist
PROJECTS_DIR = "projects"
os.makedirs(PROJECTS_DIR, exist_ok=True)
# Initialize a Knowledge Graph
knowledge_graph = KnowledgeGraph()
# Dictionary to store agents
agents = {}


def get_agent_or_404(agent_id):
    agent = agents.get(agent_id)
    if not agent:
        abort(404, description="Agent not found")
    return agent


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    response = e.get_response()
    response.data = json.dumps(
        {
            "code": e.code,
            "name": e.name,
            "description": e.description,
        }
    )
    response.content_type = "application/json"
    return response


@app.route("/api/lint", methods=["POST"])
def lint_code():
    try:
        data = request.get_json()
        code_snippet = data.get("code", "")
        if not code_snippet:
            return jsonify({"error": "No code snippet provided"}), 400
        project_id = data.get("projectId", str(uuid.uuid4()))
        project_path = os.path.join(PROJECTS_DIR, project_id)
        os.makedirs(project_path, exist_ok=True)
        code_file_path = os.path.join(project_path, "temp_code.py")
        with open(code_file_path, "w", encoding="utf-8") as f:
            f.write(code_snippet)
        # Run pylint
        lint_process = subprocess.run(
            ["pylint", code_file_path],
            capture_output=True,
            text=True,
            cwd=project_path,
            check=False,
        )
        lint_output = lint_process.stdout
        lint_error = lint_process.stderr
        if lint_error:
            logger.error(f"Pylint error: {lint_error}")
            return (
                jsonify({"error": "Pylint execution error", "details": lint_error}),
                500,
            )
        return jsonify({"lint_output": lint_output, "projectId": project_id})
    except Exception as e:
        logger.exception("Error during linting:")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@app.route("/api/agents/create", methods=["POST"])
def create_agent():
    """Creates a new agent and returns its ID."""
    agent = LlmCoderAgent()
    agents[agent.agent_id] = agent
    return jsonify({"agent_id": agent.agent_id})


@app.route("/api/agents/<agent_id>/suggest", methods=["POST"])
def get_llm_suggestion(agent_id):
    """Gets an LLM suggestion from a specific agent."""
    agent = get_agent_or_404(agent_id)
    try:
        data = request.get_json()
        prompt = data.get("prompt", "")
        if not prompt:
            return jsonify({"error": "No prompt provided"}), 400
        suggestion = agent.get_suggestion(prompt)
        return jsonify({"suggestion": suggestion})
    except Exception as e:
        logger.exception(f"Error getting LLM suggestion for agent {agent_id}:")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@app.route("/api/agents/<agent_id>/fine_tune", methods=["POST"])
def fine_tune_agent(agent_id):
    """Initiates fine-tuning for a specific agent."""
    agent = get_agent_or_404(agent_id)
    try:
        data = request.get_json()
        fine_tuning_data = data.get("data", "")
        if not fine_tuning_data:
            return jsonify({"error": "No fine-tuning data provided"}), 400
        result = agent.fine_tune(fine_tuning_data)
        return jsonify({"message": result})
    except Exception as e:
        logger.exception(f"Error during fine-tuning for agent {agent_id}:")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@app.route("/api/agents/<agent_id>/convert_to_ollama", methods=["POST"])
def convert_to_ollama(agent_id):
    """Converts a Hugging Face model to an Ollama model."""
    agent = get_agent_or_404(agent_id)
    try:
        data = request.get_json()
        base_model = data.get("base_model")
        ollama_name = data.get("ollama_name")
        if not base_model or not ollama_name:
            return jsonify({"error": "Missing base_model or ollama_name"}), 400
        result = agent.convert_to_ollama(base_model, ollama_name)
        return jsonify(result)
    except Exception as e:
        logger.exception(f"Error converting model to Ollama for agent {agent_id}:")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@app.route("/api/projects/create", methods=["POST"])
def create_project():
    """Creates a new project and returns its ID."""
    project_id = str(uuid.uuid4())
    project_path = os.path.join(PROJECTS_DIR, project_id)
    os.makedirs(project_path, exist_ok=True)
    return jsonify({"project_id": project_id})


@app.route("/api/projects/<project_id>/load", methods=["GET"])
def load_project(project_id):
    """Loads a project's data."""
    project_path = os.path.join(PROJECTS_DIR, project_id)
    if not os.path.exists(project_path):
        return jsonify({"error": "Project not found"}), 404
    # Load project data (e.g., from a JSON file)
    try:
        with open(
            os.path.join(project_path, "project_data.json"), "r", encoding="utf-8"
        ) as f:
            project_data = json.load(f)
    except Exception as e:
        logger.exception(f"Error loading project {project_id}:")
        return jsonify({"error": "Error loading project data", "details": str(e)}), 500
    return jsonify(project_data)


@app.route("/api/projects/<project_id>/save", methods=["POST"])
def save_project(project_id):
    """Saves a project's data."""
    project_path = os.path.join(PROJECTS_DIR, project_id)
    if not os.path.exists(project_path):
        return jsonify({"error": "Project not found"}), 404
    try:
        data = request.get_json()
        # Save project data (e.g., to a JSON file)
        with open(
            os.path.join(project_path, "project_data.json"), "w", encoding="utf-8"
        ) as f:
            json.dump(data, f)
    except Exception as e:
        logger.exception(f"Error saving project {project_id}:")
        return jsonify({"error": "Error saving project data", "details": str(e)}), 500
    return jsonify({"message": "Project saved successfully"})


@app.route("/api/data_collection/status", methods=["GET"])
def get_data_collection_status():
    """Gets the status of data collection."""
    # Replace with actual status check
    is_active = False
    return jsonify({"status": "active" if is_active else "inactive"})


@app.route("/api/data_collection/start", methods=["POST"])
def start_data_collection():
    """Starts data collection."""
    # Replace with actual data collection start logic
    return jsonify({"message": "Data collection started"})


@app.route("/api/data_collection/stop", methods=["POST"])
def stop_data_collection():
    """Stops data collection."""
    # Replace with actual data collection stop logic
    return jsonify({"message": "Data collection stopped"})


@app.route("/api/agents/<agent_id>/status", methods=["GET"])
def get_agent_status(agent_id):
    """Returns the status and last activity of the agent."""
    agent = get_agent_or_404(agent_id)
    return jsonify(
        {
            "status": agent.get_status(),
            "last_activity": agent.get_last_activity(),
        }
    )


@app.route("/api/logs", methods=["GET"])
def get_logs():
    """Returns the last 10 log entries."""
    log_file = "app.log"  # Assuming a single log file for simplicity
    try:
        with open(log_file, "r", encoding="utf-8") as f:
            logs = f.readlines()[-10:]  # Get the last 10 lines
        return jsonify(logs)
    except Exception as e:
        logger.exception("Error reading log file:")
        return jsonify({"error": "Error reading log file", "details": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
