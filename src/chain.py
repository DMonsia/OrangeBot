import os
import pickle

import chainlit as cl
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

import config


async def vectorize_and_store(texts, metadatas):
    store_file = "./data/vectorstore.pk"
    if os.path.isfile(store_file):
        with open(store_file, "rb") as f:
            chroma_instance = pickle.load(f)
        return chroma_instance
    embeddings = OpenAIEmbeddings()
    chroma_instance = await cl.make_async(FAISS.from_texts)(
        texts, embeddings, metadatas=metadatas
    )
    with open(store_file, "wb") as f:
        pickle.dump(chroma_instance, f)
    with open("./data/texts.pkl", "wb") as f:
        pickle.dump(texts, f)
    with open("./data/metadatas.pkl", "wb") as f:
        pickle.dump(metadatas, f)
    return chroma_instance


model = config.CHAT_MODEL or "gpt-3.5-turbo"
print("model used: ", model)


def get_chain(vectorstore, chain_type_kwargs):
    # Création d'une chaîne de traitement
    return RetrievalQAWithSourcesChain.from_chain_type(
        ChatOpenAI(model=model, temperature=0, streaming=True),
        chain_type="stuff",
        retriever=vectorstore.as_retriever(),
        chain_type_kwargs=chain_type_kwargs,
        reduce_k_below_max_tokens=True,
    )
