def create_dynamic_plan(user_request):
    """Choose agents based on the user's request."""

    request = user_request.lower()

    if any(word in request for word in ["summarize", "rewrite", "write"]):
        return ["writer"]

    if any(word in request for word in ["analyze", "analyse", "evaluate"]):
        return ["analyst", "writer"]

    if any(word in request for word in ["research", "compare", "investigate"]):
        return ["researcher", "analyst", "writer"]

    return ["researcher", "analyst", "writer"]
