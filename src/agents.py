#======================================
# Libraries
#======================================
import os
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
from dotenv import load_dotenv
from docx import Document

#======================================
# Load environment variables
#======================================
load_dotenv()

#======================================
# Azure OpenAI LLM configuration
#======================================
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

#======================================
# UserProxyAgent
#======================================
user_proxy = UserProxyAgent(
    name="User",
    human_input_mode="NEVER",
    code_execution_config={"use_docker": False},
    max_consecutive_auto_reply=0,
    )

#======================================
# Get agent names
#======================================
def get_agent_names(selected_agents):
    """Return a list of agent names excluding User and Orchestrator"""
    return [name for name in selected_agents if name not in ("Orchestrator", "User")]

#======================================
# Read PDF file
#======================================
def start_group_chat(pdf_path, selected_agents):
    """Start a group chat"""
    # Extract text from PDF file
    doc = Document(pdf_path)
    user_message = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
    groupchat = create_groupchat(selected_agents)
    manager = GroupChatManager(groupchat=groupchat)
    user_proxy.initiate_chat(manager, message=user_message)

#======================================
# Orchestrator Agent
# Modify the system prompt as needed.
#======================================
def generate_summary_system_message(selected_agents):
    """Generate system message for Orchestrator"""
    agent_list_str = "、".join(get_agent_names(selected_agents))
    return (
        "You are the orchestrator of the discussion."
        "At the beginning of the conversation, summarize the user's input and designate the agent who should speak first."
        f"The participating agents are: {agent_list_str}."
        "Once all agents have given their opinions, summarize the suggestions for the user at the end."
        f"For collaboration with other agents, use the names from {agent_list_str}."
    )

#======================================
# Agent
# Modify the system prompt as needed.
#======================================
def generate_agent_system_message(agent_type, selected_agents):
    """Generate system message for each agent"""
    agent_list_str = "、".join(get_agent_names(selected_agents))
    return (
        f"You are an expert in {agent_type}."
        "After reviewing from your own perspective, ask for opinions from other agents zero or one time."
        "If another agent asked for your opinion in the previous conversation, take that into account in your response."
        f"Do not comment on matters outside your area of expertise ({agent_type})."
        f"For collaboration with other agents, use the names from {agent_list_str}."
    )

#======================================
# Group chat
# Change agent names here as needed.
#======================================
def create_groupchat(selected_agents):
    """Create a group chat with the selected agents"""
    agent_map = {
        "Orchestrator": lambda: AssistantAgent(
            name="Orchestrator",
            system_message=generate_summary_system_message(selected_agents),
            llm_config=llm_config
        ),
        "AgentA": lambda: AssistantAgent(
            name="AgentA",
            system_message=generate_agent_system_message("AgentA", selected_agents),
            llm_config=llm_config
        ),
        "AgentB": lambda: AssistantAgent(
            name="AgentB",
            system_message=generate_agent_system_message("AgentB", selected_agents),
            llm_config=llm_config
        ),
        "AgentC": lambda: AssistantAgent(
            name="AgentC",
            system_message=generate_agent_system_message("AgentC", selected_agents),
            llm_config=llm_config
        ),
        "AgentD": lambda: AssistantAgent(
            name="AgentD",
            system_message=generate_agent_system_message("AgentD", selected_agents),
            llm_config=llm_config
        ),
        "AgentE": lambda: AssistantAgent(
            name="AgentE",
            system_message=generate_agent_system_message("AgentE", selected_agents),
            llm_config=llm_config
        ),
        "AgentF": lambda: AssistantAgent(
            name="AgentF",
            system_message=generate_agent_system_message("AgentF", selected_agents),
            llm_config=llm_config
        ),
        "User": lambda: user_proxy,
    }
    agents = [agent_map[name]() for name in selected_agents if name in agent_map]
#======================================
# Set the maximum number of conversation rounds
# Set max_round=10 to allow up to 10 rounds of conversation
#======================================
    return GroupChat(agents=agents, messages=[], max_round=10)