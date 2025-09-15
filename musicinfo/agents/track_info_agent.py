from dotenv import load_dotenv

load_dotenv()
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

from musicinfo.tools import get_song_history, format_json, get_track_basic_info, get_track_info_from_url


def create_agent():
    """Create an agent."""
    llm = ChatOpenAI(model="gpt-4o", temperature=0.1)
    tools = [get_track_info_from_url, get_track_basic_info, get_song_history, format_json]
    system_message = """
    You must obtain basic information about the song,
    then you must get the history of the song
    and finally you must format the JSON for your final answer.

    General rules:
    - ALWAYS use the provided tools.
    - NO ADD additional text, ONLY return the JSON formatted .

    """
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                " You are a helpful AI assistant, collaborating with other assistants."
                " Use the provided tools to progress towards answering the question." 
                " {system_message}"
                " You have access to the following tools: {tool_names}.",
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )
    prompt = prompt.partial(system_message=system_message)
    prompt = prompt.partial(tool_names=", ".join([tool.name for tool in tools]))
    return prompt | llm.bind_tools(tools)



track_info_agent = create_agent( )
# res = track_info_agent.invoke({"messages": [HumanMessage(content='dame la informacion basica de la cancion maría magdalena - Sandra ')]})
# print(res)
# print("EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
# res.pretty_print()
