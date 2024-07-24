from langchain_openai import OpenAIEmbeddings

class EmbeddingConfig(object):
    """ Backend embedding configuration parameters. """
    pass

class OpenAIEmbeddingConfig(EmbeddingConfig):
    """ Configuration for OpenAI embeddings. """
    model_name = "text-embedding-ada-002"
    embeddings = OpenAIEmbeddings(
        model=model_name
    )
