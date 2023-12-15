import os
import pickle

from src.chain import get_chain, vectorize_and_store
from src.prompt import chain_type_kwargs, text_splitter
from src.utils import process_uploaded_files

import chainlit as cl


# Définition d'une fonction d'initialisation exécutée au démarrage
@cl.on_chat_start
async def init():
    # Message d'accueil
    await cl.Message(
        content="Bienvenue !\n Je suis votre assistant virtuel charger de vous aider dans la comprehension des services d'Orange. Je réponds à vos questions sur la base des documents que vous me donnez.",
    ).send()

    # Verifier si des documents ont deja ete charger
    store_file = "./data/vectorstore.pk"
    if os.path.isfile(store_file):
        with open(store_file, "rb") as f:
            vectorstore = pickle.load(f)
        with open("./data/texts.pkl", "rb") as f:
            documents = pickle.load(f)
        with open("./data/metadatas.pkl", "rb") as f:
            metadatas = pickle.load(f)
    else:  # Si non, charger et traiter des fichiers
        files = None
        while files is None:
            files = await cl.AskFileMessage(
                content="Veuillez charger vos documents (maximun 10) pour commencer !",
                accept=[
                    "text/plain",
                    "application/pdf",
                    "text/csv",
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    "application/vnd.ms-excel",
                ],
                max_files=10,
                max_size_mb=100,
            ).send()

        documents, metadatas = process_uploaded_files(files, text_splitter)
        vectorstore = await vectorize_and_store(documents, metadatas)
    chain = get_chain(vectorstore, chain_type_kwargs)

    # Enregistrement des métadonnées et des textes dans la session utilisateur
    cl.user_session.set("metadatas", metadatas)
    cl.user_session.set("texts", documents)
    cl.user_session.set("chain", chain)
    # Notification de l'utilisateur que le traitement est terminé
    await cl.Message(
        content="Traitement terminé. Vous pouvez maintenant poser des questions !"
    ).send()


# Définition d'une fonction principale exécutée à chaque message
@cl.on_message
async def main(message):
    # Récupération de la chaîne depuis la session utilisateur
    chain = cl.user_session.get("chain")

    # Traitement du message à l'aide de la chaîne
    cb = cl.AsyncLangchainCallbackHandler(
        stream_final_answer=True, answer_prefix_tokens=["FINAL", "ANSWER"]
    )
    cb.answer_reached = True
    res = await chain.acall(message, callbacks=[cb])
    answer = res["answer"]
    sources = res["sources"].strip()
    source_elements = []

    # Récupération des métadonnées et des textes depuis la session utilisateur
    metadatas = cl.user_session.get("metadatas")
    all_sources_ = [m["source"] for m in metadatas]
    texts = cl.user_session.get("texts")

    if sources:
        try:
            found_sources = []
            for source in sources.split(","):
                index = all_sources_.index(source)
                text = texts[index]  # type: ignore
                found_sources.append(source)
                source_elements.append(cl.Text(content=text, name=source))

            if found_sources:
                answer += f"\nSources: {','.join(found_sources)}"
            else:
                answer += "\nPas de sources"
        except Exception as e:
            ## mauvaise pratique mais il faut que ca passe
            print("Erreur survenue lors de l'extraction des sources")
            print(e)

    if cb.has_streamed_final_answer:
        cb.final_stream.elements = source_elements  # type: ignore
        await cb.final_stream.update()  # type: ignore
    else:
        await cl.Message(content=answer, elements=source_elements).send()
