# Multi-Agent System by AutoGen

## Overview
This project is a multi-agent system where multiple AI agents collaborate to conduct discussions. Using a Streamlit-based web UI, users can input a PDF or a theme, and the selected agents will automatically generate discussions and proposals. Each agent can be assigned a unique role and prompt, leveraging Azure OpenAI Service.

---

## Main Features

- **PDF and Theme Input**
  Users can input a PDF file or a text theme to serve as the basis for the discussion.

- **Agent Selection and Role Assignment**
  You can select participants from the "Orchestrator" plus up to six agents.
  Each agent provides opinions from their area of expertise and can ask for input from other agents.

- **Automated Group Chat Progression**
  The Orchestrator summarizes the discussion and aggregates the opinions of all agents to generate a final proposal.

- **Web Interface with Streamlit**
  Conversation history is displayed with color coding and icons for each agent.

---

## File Structure

- `src/agents.py`
  Manages agent creation, prompt settings, group chat construction, and other AI agent logic.

- `src/app.py`
  Handles the Streamlit web UI, PDF reading, user input, and conversation history display.

---

## Requirements

- Python 3.8 or higher
- Azure OpenAI Service API key
- Required Python packages (see `requirements.txt`)

---

## Setup

1. **Clone the repository**
    ```sh
    git clone <repository-url>
    cd Multi-Agent
    ```

2. **Create and activate a virtual environment**
    ```sh
    python -m venv venv_demo
    .\venv_demo\Scripts\activate #for windows
    ```

3. **Install dependencies**
    ```sh
    pip install -r requirements.txt
    ```

4. **Set environment variables**
   Create a `.env` file in the project root and add the following:
    ```
    DEPLOYMENT_NAME=(Your Azure OpenAI deployment name)
    API_KEY=(Your Azure OpenAI API key)
    API_ENDPOINT=(Your endpoint URL)
    API_VERSION=(API version, e.g., 2023-05-15)
    ```

---

## How to Run

1. **Start the Streamlit app**
    ```sh
    streamlit run .\src\app.py #for windows
    ```

2. **Access via web browser**
   Open the specified local URL (e.g., http://localhost:8501).

---

## Usage

1. Enter a theme (required) and, if needed, a PDF file path.
2. Select the agents you want to participate.
3. Click the "Send Input to Agents" button to send your input to the agents.
4. Click the "Start Discussion" button to begin the conversation.
5. Each agent's statements will be displayed with color coding and icons.

---

## Customization

- Agent names, roles, and prompts can be edited in `src/agents.py`.
- Agent colors and icons can be changed in the `agent_styles` and `agent_images` sections of `src/app.py`.

---

## License

This project is licensed under the MIT License.

---

## Notes

- You need an API key and endpoint to use Azure OpenAI Service.
- If you want to use the application in Japanese, please refer to the code in the files with `ja` in their names (e.g., `app-ja.py`, `agents-ja.py`).

---

## References

- [src/agents.py](src/agents.py)
- [src/app.py](src/app.py)

---

## アプリケーションの Azure へのデプロイ (Azure CLI から)
```sh
# リポジトリの取得
git clone https://github.com/mahiya/Multi-Agent-System-by-AutoGen
cd Multi-Agent-System-by-AutoGen

# 環境変数の設定
export API_ENDPOINT="https://[Azure OpenAI Service のアカウント名].openai.azure.com/"
export API_KEY="[Azure OpenAI Service のキー]"
export API_VERSION="2025-03-01-preview"
export DEPLOYMENT_NAME="gpt-4o"

# デプロイ
chmod +x deploy.sh
./deploy.sh
```