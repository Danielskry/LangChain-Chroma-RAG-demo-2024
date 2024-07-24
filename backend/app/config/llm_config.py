from langchain_openai import ChatOpenAI
from langchain_core.callbacks import StreamingStdOutCallbackHandler

class LLMConfig(object):
    """ Backend LLM configuration parameters. """
    pass

class OpenAIConfig(LLMConfig):
    """ Configuration for OpenAI LLM. """
    model_name = "gpt-4o-mini"
    llm = ChatOpenAI(
        model_name=model_name,
        streaming=True,
        callbacks=[StreamingStdOutCallbackHandler()],
        temperature=0
    )
