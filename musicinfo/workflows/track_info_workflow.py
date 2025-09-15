import functools
from typing import TypedDict, Literal, Annotated
from langchain_core.messages import ToolMessage, AIMessage, AnyMessage
from langgraph.constants import START, END
from langgraph.graph import StateGraph, add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from musicinfo.agents import track_info_agent
from musicinfo.tools import get_track_basic_info, get_song_history, format_json, get_track_info_from_url


class NodeMainInput(TypedDict ):
    song_raw:str

class AgentState(TypedDict):
    #track_info_raw: str
    #track_info: dict[Literal["artist", "song"], str]
    #track_info_formatted: str
    messages: Annotated[list[AnyMessage], add_messages]
    sender: str | None


def agent_node(state, agent, name):
    result = agent.invoke(state)
    # We convert the agent output into a format that is suitable to append to the global state
    if isinstance(result, ToolMessage):
        pass
    else:
        result = AIMessage(**result.dict(exclude={"type", "name"}), name=name);

    next_state = {
        "messages": [result],
        # Since we have a strict workflow, we can
        # track the sender so we know who to pass to next.
        "sender": name,

    }
    # print('next_state')
    # print(next_state)
    # print('next_state')
    return next_state


def assistant_node(state: AgentState ):
    size = len(state['messages'])

    #print(f'state[ messages ]: {size} {[ type(m).__name__ for m in state["messages"] ] }' )
    next_message =  track_info_agent.invoke(state["messages"])
    # if isinstance(next_message, ToolMessage):
    #     print('ToolMessage')
    #     pass
    print('return')
    return {"messages": [next_message],'hola':'HOLA MUNDO' }




def get_graph():
    #main_node = functools.partial(agent_node, agent=track_info_agent, name="Main")

    tools = [get_track_info_from_url, get_track_basic_info, get_song_history, format_json]
    tool_node = ToolNode(tools)
    workflow = StateGraph(AgentState)


    workflow.add_node("Main", assistant_node)
    workflow.add_node("tools", tool_node)

    workflow.add_edge(START, "Main")


    workflow.add_conditional_edges(
        'Main',
        tools_condition ,
    )

    workflow.add_edge("tools", "Main")

    workflow.add_edge("Main", END)
    #workflow.add_edge("tools", END)

    graph = workflow.compile()

    return graph

graph = get_graph()
