from langgraph.graph import StateGraph, START , END
from app.graph.state import AgentState
from app.graph.nodes import analyze_question,retrieve_code,generate_answer


def build_graph():
    """build and complie the MVP langgraph workflow"""

    workflow = StateGraph(AgentState)

    workflow.add_node("analyze_question",analyze_question)
    workflow.add_node("retrieve_code",retrieve_code)
    workflow.add_node("generate_answer",generate_answer)

    workflow.add_edge(START,"analyze_question")
    workflow.add_edge("analyze_question","retrieve_code")
    workflow.add_edge("retrieve_code","generate_answer")
    workflow.add_edge("generate_answer",END)

    return workflow.compile()

graph_app = build_graph()