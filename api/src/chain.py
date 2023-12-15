import config
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

embeddings = OpenAIEmbeddings(api_key=config.OPENAI_API_KEY)


def get_vectorstore(store_file):
    return FAISS.load_local(store_file, embeddings)


def vectorize_and_store(texts, metadatas, store_file):
    chroma_instance = FAISS.from_texts(texts, embeddings, metadatas=metadatas)
    chroma_instance.save_local(store_file)


def get_chain(model, vectorstore, chain_type_kwargs):
    # Création d'une chaîne de traitement
    return RetrievalQAWithSourcesChain.from_chain_type(
        ChatOpenAI(model=model, temperature=0, api_key=config.OPENAI_API_KEY),
        chain_type="stuff",
        retriever=vectorstore.as_retriever(),
        chain_type_kwargs=chain_type_kwargs,
        reduce_k_below_max_tokens=True,
    )
