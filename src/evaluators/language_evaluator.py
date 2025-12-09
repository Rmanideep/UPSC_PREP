from ..models import UPSCState, get_llm_model, get_structured_response


def evaluate_language(state: UPSCState):
    """Evaluate the language quality of the essay"""
    model = get_llm_model(state["api_key"])
    
    prompt = f'Evaluate the language quality of the following essay and provide a feedback and assign a score out of 10 \n {state["essay"]}'
    output = get_structured_response(model, prompt)

    return {'language_feedback': output['feedback'], 'individual_scores': [output['score']]}
