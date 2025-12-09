from ..models import UPSCState, get_llm_model, get_structured_response


def evaluate_thought(state: UPSCState):
    """Evaluate the clarity of thought of the essay"""
    model = get_llm_model(state["api_key"])
    
    prompt = f'Evaluate the clarity of thought of the following essay and provide a feedback and assign a score out of 10 \n {state["essay"]}'
    output = get_structured_response(model, prompt)

    return {'clarity_feedback': output['feedback'], 'individual_scores': [output['score']]}
