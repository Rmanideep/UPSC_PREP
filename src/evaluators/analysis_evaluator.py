from ..models import UPSCState, get_llm_model, get_structured_response


def evaluate_analysis(state: UPSCState):
    """Evaluate the depth of analysis of the essay"""
    model = get_llm_model(state["api_key"])
    
    prompt = f'Evaluate the depth of analysis of the following essay and provide a feedback and assign a score out of 10 \n {state["essay"]}'
    output = get_structured_response(model, prompt)

    return {'analysis_feedback': output['feedback'], 'individual_scores': [output['score']]}
