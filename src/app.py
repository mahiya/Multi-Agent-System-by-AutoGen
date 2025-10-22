# ======================================
# Libraries
# ======================================
import os
import re
import time
from io import BytesIO
import PyPDF2
import streamlit as st

from autogen import GroupChatManager
from dotenv import load_dotenv
from agents import create_groupchat

# ======================================
# Load environment variables
# ======================================
load_dotenv()

# ======================================
# Azure OpenAI LLM configuration
# ======================================
llm_config = {
    "config_list": [
        {
            "model": os.getenv("DEPLOYMENT_NAME"),
            "api_type": "azure",
            "api_key": os.getenv("API_KEY"),
            "base_url": os.getenv("API_ENDPOINT"),
            "api_version": os.getenv("API_VERSION"),
        }
    ]
}


# ======================================
# Read PDF file
# ======================================
def read_pdf(file_source):
    text = ""
    if isinstance(file_source, str):
        with open(file_source, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return text

    if hasattr(file_source, "seek"):
        file_source.seek(0)
    pdf_bytes = file_source.read()
    reader = PyPDF2.PdfReader(BytesIO(pdf_bytes))
    for page in reader.pages:
        text += page.extract_text() + "\n"
    if hasattr(file_source, "seek"):
        file_source.seek(0)
    return text


# ======================================
# Agent settings *Color
# Change agent names and colors as needed.
# ======================================
agent_styles = {
    "User": "background-color:#b0c4d6; color:#1a2634;",
    "Orchestrator": "background-color:#ffe2b2; color:#5a3e1b;",
    "AgentA": "background-color:#d1c4e9; color:#2d254c;",
    "AgentB": "background-color:#b7d7c9; color:#1b3a2b;",
    "AgentC": "background-color:#f5e9b5; color:#665c1e;",
    "AgentD": "background-color:#f3c1c6; color:#6b2b36;",
    "AgentE": "background-color:#b3d1e6; color:#1b2c3a;",
    "AgentF": "background-color:#d7ccc8; color:#3e2723;",
}

# ======================================
# Agent settings *Icon
# Change agent names and icons as needed.
# ======================================
agent_images = {
    "Orchestrator": "https://img.icons8.com/fluency/96/administrator-male.png",
    "AgentA": "https://img.icons8.com/color/96/000000/a.png",
    "AgentB": "https://img.icons8.com/color/96/000000/b.png",
    "AgentC": "https://img.icons8.com/color/96/000000/c.png",
    "AgentD": "https://img.icons8.com/color/96/000000/d.png",
    "AgentE": "https://img.icons8.com/color/96/000000/e.png",
    "AgentF": "https://img.icons8.com/color/96/000000/f.png",
    "User": "https://img.icons8.com/color/96/000000/user.png",
}


# ======================================
# Streamlit settings
# ======================================
def main():
    st.markdown(
        # ======================================
        # If you have a company logo, please put the URL here
        # ======================================
        """
        <div style="text-align:center;">
            <img src="https://logos-world.net/wp-content/uploads/2020/09/Microsoft-Logo.png" width="220"/>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.markdown(
        # ======================================
        # Set the title of the multi-agent system
        # ======================================
        """
        <h2 style="text-align:center;">
            Example: Multi-Agent System<br> Subtitle
        </h2>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")

    # ======================================
    # Change agent names as needed.
    # ======================================
    selectable_agents = ["AgentA", "AgentB", "AgentC", "AgentD", "AgentE", "AgentF"]

    theme = st.text_input("Enter theme (required)", key="discussion_theme")

    selected_agents = st.multiselect("Select agents", options=selectable_agents, default=[])
    # Orchestrator and User are default
    selected_agents = ["Orchestrator"] + selected_agents + ["User"]

    # Initialize session
    if "groupchat" not in st.session_state:
        st.session_state.groupchat = None
    if "manager" not in st.session_state:
        st.session_state.manager = None
    if "user_message" not in st.session_state:
        st.session_state.user_message = None
    if "initialized" not in st.session_state:
        st.session_state.initialized = False
    if "chat_started" not in st.session_state:
        st.session_state.chat_started = False

    # Read PDF file
    uploaded_file = st.file_uploader("Upload reference PDF (optional)", type=["pdf"], key="pdf_upload")

    # Send input to agents
    if st.button("Send input to agents"):
        user_message = ""
        if uploaded_file is not None:
            try:
                user_message = read_pdf(uploaded_file)
                st.session_state.user_message = user_message
                st.success("File loaded successfully.")
                st.text_area("Loaded file", user_message, height=200)
            except Exception as e:
                st.error(f"An error occurred: {e}")
                return

        if theme.strip():
            if user_message:
                user_message += f"\n\n[Theme]\n{theme.strip()}"
            else:
                user_message = f"[Theme]\n{theme.strip()}"

        if not user_message.strip():
            st.warning("Please enter either a PDF or a theme.")
            return

        # Initialize group chat
        groupchat = create_groupchat(selected_agents)
        manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)
        st.session_state.groupchat = groupchat
        st.session_state.manager = manager
        st.session_state.initialized = True
        st.session_state.chat_started = False  # Reset chat start flag

        # Run chat here (complete in terminal)
        groupchat.agents[-1].initiate_chat(manager, message=user_message)

    # Start conversation
    if st.session_state.initialized and st.session_state.groupchat:
        if st.button("Start discussion"):
            st.session_state.chat_started = True

    # Display conversation history
    if st.session_state.initialized and st.session_state.groupchat and st.session_state.chat_started:
        st.markdown(
            """
        <style>
        .chat-row { margin-bottom: 1.5em; }
        .chat-bubble {
            border-radius: 18px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            padding: 1em 1.2em;
            max-width: 60vw;
            font-size: 1.08em;
            line-height: 1.7;
            position: relative;
            word-break: break-word;
        }
        .chat-label {
            font-weight: bold;
            font-size: 0.98em;
            color: #333;
            margin-bottom: 0.3em;
            display: block;
        }
        .chat-row.left .chat-bubble {
            margin-left: 0.5em;
            background: #f9fafb;
        }
        .chat-row.right .chat-bubble {
            margin-right: 0.5em;
            background: #e3f2fd;
        }
        .chat-row img {
            border-radius: 50%;
            border: 2px solid #fff;
            box-shadow: 0 1px 4px rgba(0,0,0,0.07);
        }
        </style>
        """,
            unsafe_allow_html=True,
        )

        st.markdown("### Conversation history of each agent")
        chat_container = st.container()

        with chat_container:
            for idx, msg in enumerate(st.session_state.groupchat.messages):
                if not isinstance(msg, dict):
                    continue
                if msg.get("type") in ["tool_use", "tool_result"]:
                    continue
                name = msg.get("name", "Unknown")
                content = msg.get("content", "")
                if content is None or (isinstance(content, str) and content.strip() in ["", "None"]) or isinstance(content, (list, dict)):
                    continue
                if not isinstance(content, str):
                    content = str(content)
                if (
                    re.search(r"\*{5} (Suggested tool call|Response from calling tool)", content)
                    or content.strip().startswith("***** Suggested tool call")
                    or content.strip().startswith("***** Response from calling tool")
                ):
                    continue
                if isinstance(content, str) and (
                    (content.strip().startswith("[{") and content.strip().endswith("}]"))
                    or (content.strip().startswith("{") and content.strip().endswith("}"))
                ):
                    continue
                if name == "User" and not content.strip():
                    continue

                html_content = "<br>".join(line if line.strip() else "<br>" for line in content.splitlines())
                style = agent_styles.get(name, "background-color:#eeeeee; color:#222;")
                align_class = "left" if idx % 2 == 0 else "right"

                if align_class == "left":
                    st.markdown(
                        f"""
                        <div class="chat-row left" style="display:flex;align-items:flex-start;">
                            <img src="{agent_images.get(name, '')}" alt="{name}" width="48" height="48" style="margin-right:1em;align-self:flex-start;"/>
                            <div class="chat-bubble" style="{style}">
                                <span class="chat-label">{name}</span>
                                <span>{html_content}</span>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f"""
                        <div class="chat-row right" style="display:flex;flex-direction:row-reverse;align-items:flex-start;">
                            <img src="{agent_images.get(name, '')}" alt="{name}" width="48" height="48" style="margin-left:1em;align-self:flex-start;"/>
                            <div class="chat-bubble" style="{style}">
                                <span class="chat-label">{name}</span>
                                <span>{html_content}</span>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                time.sleep(5)  # Set the display interval for each message to 5 seconds


if __name__ == "__main__":
    main()
