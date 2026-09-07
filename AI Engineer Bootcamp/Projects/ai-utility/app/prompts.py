from langchain_core.prompts import ChatPromptTemplate


summarize_prompt = ChatPromptTemplate.from_template(
    """
    Summarize the following text clearly and concisely.

    Text:
    {text}
    """
)


rewrite_prompt = ChatPromptTemplate.from_template(
    """
    Rewrite the following text to make it clear,
    professional, and grammatically correct.

    Preserve the original meaning.

    Text:
    {text}
    """
)


classify_prompt = ChatPromptTemplate.from_template(
    """
    Classify the following text into one of these categories:

    - technical_issue
    - billing
    - account
    - general
    - other

    Return only the most appropriate category.

    Text:
    {text}
    """
)