from typing import NotRequired
from langgraph.constants import START, END
from langgraph.graph import StateGraph,  MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from musicinfo.agents import get_full_tools_agent


# class NodeMainInput(TypedDict ):
#     song_raw:str

class MyState(MessagesState):
    song_json: NotRequired[dict[str, list | str]]


def build_assistant_node(agent):

    def assistant_node(state: MyState):
        next_message = agent.invoke(state["messages"])
        print('return')
        return {"messages": [next_message], 'hola': 'HOLA MUNDO'}

    return assistant_node


def get_graph():
    # main_node = functools.partial(agent_node, agent=track_info_agent, name="Main")
    agent_attr = get_full_tools_agent()
    tools = agent_attr['tools']
    tool_node = ToolNode(tools)
    workflow = StateGraph(MyState)

    workflow.add_node("Main", build_assistant_node(agent_attr['agent']))
    workflow.add_node("tools", tool_node)

    workflow.add_edge(START, "Main")

    workflow.add_conditional_edges(
        'Main',
        tools_condition,
    )

    workflow.add_edge("tools", "Main")

    workflow.add_edge("Main", END)

    graph = workflow.compile()

    return graph


graph = get_graph()
