from langgraph.graph import StateGraph, START, END
from ..models import UPSCState
from ..evaluators import evaluate_language, evaluate_analysis, evaluate_thought, final_evaluation


def create_workflow():
    """Create and compile the UPSC essay evaluation workflow"""
    graph = StateGraph(UPSCState)

    # Add nodes
    graph.add_node('evaluate_language', evaluate_language)
    graph.add_node('evaluate_analysis', evaluate_analysis)
    graph.add_node('evaluate_thought', evaluate_thought)
    graph.add_node('final_evaluation', final_evaluation)

    # Add edges - parallel execution for evaluation nodes
    graph.add_edge(START, 'evaluate_language')
    graph.add_edge(START, 'evaluate_analysis')
    graph.add_edge(START, 'evaluate_thought')

    # All evaluations feed into final evaluation
    graph.add_edge('evaluate_language', 'final_evaluation')
    graph.add_edge('evaluate_analysis', 'final_evaluation')
    graph.add_edge('evaluate_thought', 'final_evaluation')
    graph.add_edge('final_evaluation', END)

    # Compile and return the workflow
    return graph.compile()


def evaluate_essay(essay_text: str, api_key: str):
    """Evaluate an essay using the workflow"""
    workflow = create_workflow()
    
    initial_state = {
        'essay': essay_text,
        'api_key': api_key
    }
    
    result = workflow.invoke(initial_state)
    return result
