from Services.groq_service import GroqService


def response_agent(state):

    recommendations = state.get("recommendations", [])
    budget = state.get("budget", 0)

    if not recommendations:
        return {
            "ai_response": "No products found."
        }

    groq = GroqService()

    top_product = recommendations[0]
    alternatives = recommendations[1:]

    comparison = groq.generate_comparison_summary(
        recommendations,
        budget
    )

    response = groq.generate_recommendation(
        top_product,
        alternatives
    )

    return {
        "comparison_summary": comparison,
        "ai_response": response
    }
