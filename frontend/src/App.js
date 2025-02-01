import React, { useState, useEffect } from 'react';
import './App.css';
import Editor from 'react-simple-code-editor';
import { highlight, languages } from 'prismjs/components/prism-core';
import 'prismjs/components/prism-clike';
import 'prismjs/components/prism-python';
import 'prismjs/themes/prism.css'; // Import a theme for the code editor
function App() {
    const [code, setCode] = useState('');
    const [lintOutput, setLintOutput] = useState('');
    const [llmSuggestion, setLlmSuggestion] = useState('');
    const [projectId, setProjectId] = useState('');
    const [fineTuningData, setFineTuningData] = useState('');
    const [fineTuningMessage, setFineTuningMessage] = useState('');
    const [agentId, setAgentId] = useState(null);
    const [availableAgents, setAvailableAgents] = useState([]);
    const [selectedAgentId, setSelectedAgentId] = useState(null);
    const [projects, setProjects] = useState([]);
    const [selectedProjectId, setSelectedProjectId] = useState(null);
    const [baseModel, setBaseModel] = useState('');
    const [ollamaName, setOllamaName] = useState('');
    const [conversionStatus, setConversionStatus] = useState('');
    const [agentStatus, setAgentStatus] = useState("Idle");
    const [agentLastActivity, setAgentLastActivity] = useState("");
    const [logs, setLogs] = useState([]);
    useEffect(() => {
        const createAgent = async () => {
            const response = await fetch('/api/agents/create', { method: 'POST' });
            const data = await response.json();
            if (response.ok) {
                setAgentId(data.agent_id);
                setAvailableAgents([data.agent_id]);
                setSelectedAgentId(data.agent_id);
            } else {
                console.error("Failed to create agent:", data.error);
            }
        };
        const fetchProjects = async () => {
            const response = await fetch('/api/projects');
            if (response.ok) {
                const data = await response.json();
                setProjects(data.projects || []);
            } else {
                console.error("Failed to fetch projects");
            }
        };
        createAgent();
        fetchProjects();
    }, []);
    useEffect(() => {
        const statusInterval = setInterval(() => {
            if (selectedAgentId) {
                fetch(`/api/agents/${selectedAgentId}/status`)
                    .then(response => response.json())
                    .then(data => {
                        setAgentStatus(data.status);
                        setAgentLastActivity(data.last_activity);
                    })
                    .catch(error => console.error("Error fetching agent status:", error));
            }
        }, 1000);
        return () => clearInterval(statusInterval);
    }, [selectedAgentId]);
    const handleLint = async () => {
        const response = await fetch('/api/lint', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ code: code, projectId: projectId }),
        });
        const data = await response.json();
        if (response.ok) {
            setLintOutput(data.lint_output);
            setProjectId(data.projectId);
        } else {
            setLintOutput(`Error: ${data.error} - ${data.details}`);
        }
    };
    const handleSuggestion = async () => {
        if (!selectedAgentId) {
            setLlmSuggestion("Agent not selected.");
            return;
        }
        const response = await fetch(`/api/agents/${selectedAgentId}/suggest`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ prompt: code }),
        });
        const data = await response.json();
        if (response.ok) {
            setLlmSuggestion(data.suggestion);
        } else {
            setLlmSuggestion(`Error: ${data.error} - ${data.details}`);
        }
    };
    const handleFineTune = async () => {
        if (!selectedAgentId) {
            setFineTuningMessage("Agent not selected.");
            return;
        }
        const response = await fetch(`/api/agents/${selectedAgentId}/fine_tune`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ data: fineTuningData }),
        });
        const data = await response.json();
        if (response.ok) {
            setFineTuningMessage(data.message);
        } else {
            setFineTuningMessage(`Error: ${data.error} - ${data.details}`);
        }
    };
    const handleCreateProject = async () => {
        const response = await fetch('/api/projects/create', { method: 'POST' });
        const data = await response.json();
        if (response.ok) {
            setProjectId(data.project_id);
            setProjects([...projects, data.project_id]);
            setSelectedProjectId(data.project_id);
            alert(`Project created with ID: ${data.project_id}`);
        } else {
            alert(`Error creating project: ${data.error}`);
        }
    };
    const handleLoadProject = async (projectIdToLoad) => {
        const response = await fetch(`/api/projects/${projectIdToLoad}/load`);
        if (response.ok) {
            const data = await response.json();
            setCode(data.code || '');
            setSelectedProjectId(projectIdToLoad);
            alert(`Project ${projectIdToLoad} loaded successfully.`);
        } else {
            const data = await response.json();
            alert(`Error loading project: ${data.error}`);
        }
    };
    const handleSaveProject = async () => {
        if (!selectedProjectId) {
            alert("No project selected to save.");
            return;
        }
        const response = await fetch(`/api/projects/${selectedProjectId}/save`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ code: code }),
        });
        if (response.ok) {
            alert(`Project ${selectedProjectId} saved successfully.`);
        } else {
            const data = await response.json();
            alert(`Error saving project: ${data.error}`);
        }
    };
    const handleAgentChange = (event) => {
        setSelectedAgentId(event.target.value);
    };
    const handleConvert = async () => {
        if (!selectedAgentId) {
            setConversionStatus("Agent not selected.");
            return;
        }
        const response = await fetch(`/api/agents/${selectedAgentId}/convert_to_ollama`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ base_model: baseModel, ollama_name: ollamaName }),
        });
        const data = await response.json();
        if (response.ok) {
            setConversionStatus(data.status);
        } else {
            setConversionStatus(`Error: ${data.error} - ${data.details}`);
        }
    };
    useEffect(() => {
        const fetchLogs = async () => {
            try {
                const response = await fetch('/api/logs');
                if (response.ok) {
                    const data = await response.json();
                    setLogs(data);
                } else {
                    console.error("Failed to fetch logs");
                }
            } catch (error) {
                console.error("Error fetching logs:", error);
            }
        };
        const logsInterval = setInterval(fetchLogs, 5000);
        return () => clearInterval(logsInterval);
    }, []);
    return (
        <div className="App">
            <h1>LLMCoder Foundation</h1>
            <div className="controls-container">
                <div className="agent-selector">
                    <label htmlFor="agent-select">Select Agent:</label>
                    <select id="agent-select" value={selectedAgentId || ''} onChange={handleAgentChange}>
                        {availableAgents.map(agentId => (
                            <option key={agentId} value={agentId}>{agentId}</option>
                        ))}
                    </select>
                </div>
                <div className="project-controls">
                    <button onClick={handleCreateProject}>Create Project</button>
                    <select onChange={(e) => setSelectedProjectId(e.target.value)} value={selectedProjectId || ''}>
                        <option value="">Select Project</option>
                        {projects.map(projectId => (
                            <option key={projectId} value={projectId}>{projectId}</option>
                        ))}
                    </select>
                    <button onClick={() => handleLoadProject(selectedProjectId)} disabled={!selectedProjectId}>
                        Load Selected Project
                    </button>
                    <button onClick={handleSaveProject} disabled={!selectedProjectId}>Save Project</button>
                </div>
            </div>
            <div className="code-editor">
                <Editor
                    value={code}
                    onValueChange={code => setCode(code)}
                    highlight={code => highlight(code, languages.python)}
                    padding={10}
                    style={{
                        fontFamily: '"Fira code", "Fira Mono", monospace',
                        fontSize: 14,
                        border: '1px solid #ccc',
                        marginBottom: '10px',
                    }}
                />
            </div>
            <div className="button-container">
                <button onClick={handleLint}>Run Pylint</button>
                <button onClick={handleSuggestion}>Get LLM Suggestion</button>
                <button onClick={handleFineTune}>Fine-Tune Model</button>
            </div>
            <div className="output-area">
                <h2>Pylint Output:</h2>
                <pre>{lintOutput}</pre>
            </div>
            <div className="output-area">
                <h2>LLM Suggestion:</h2>
                <pre>{llmSuggestion}</pre>
            </div>
            <div className="fine-tuning-area">
                <h2>Fine-Tuning</h2>
                <textarea
                    placeholder="Enter fine-tuning data here (e.g., JSON or text)"
                    value={fineTuningData}
                    onChange={(e) => setFineTuningData(e.target.value)}
                />
                <p>
                    <b>Fine-Tuning Message:</b> {fineTuningMessage}
                </p>
            </div>
            <div className="conversion-area">
                <h2>Convert to Ollama</h2>
                <input
                    type="text"
                    placeholder="Base Model (HuggingFace)"
                    value={baseModel}
                    onChange={(e) => setBaseModel(e.target.value)}
                />
                <input
                    type="text"
                    placeholder="Ollama Model Name"
                    value={ollamaName}
                    onChange={(e) => setOllamaName(e.target.value)}
                />
                <button onClick={handleConvert}>Convert</button>
                <p>Status: {conversionStatus}</p>
            </div>
            <div className="status-area">
                <h2>Agent Status:</h2>
                <p>
                    <b>Status:</b> {agentStatus}
                </p>
                <p>
                    <b>Last Activity:</b> {agentLastActivity}
                </p>
            </div>
            <div className="logs-area">
                <h2>Logs:</h2>
                <ul>
                    {logs.map((log, index) => (
                        <li key={index}>{log}</li>
                    ))}
                </ul>
            </div>
        </div>
    );
}
export default App;