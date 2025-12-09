from ..models import UPSCState, get_llm_model


def final_evaluation(state: UPSCState):
    """Generate final evaluation summary and calculate average score"""
    model = get_llm_model(state["api_key"])
    
    # Generate summary feedback
    system_prompt = """You are an essay evaluator. Create a concise overall summary based on the individual feedback provided.
    Focus on highlighting the key strengths and areas for improvement."""
    
    prompt = f'''Based on the following detailed feedback, create a concise summary:
    
    Language Quality: {state["language_feedback"]}
    Depth of Analysis: {state["analysis_feedback"]}
    Clarity of Thought: {state["clarity_feedback"]}
    
    Keep the summary focused on the main points and provide actionable suggestions.'''
    
    response = model.invoke([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ])
    
    overall_feedback = response.content

    # Calculate average score
    avg_score = sum(state['individual_scores']) / len(state['individual_scores'])

    return {'overall_feedback': overall_feedback, 'avg_score': avg_score}
