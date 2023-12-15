import os
from typing import Annotated

import config
from fastapi import FastAPI, File, HTTPException, Query, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from src.chain import get_chain, get_vectorstore, vectorize_and_store
from src.prompt import chain_type_kwargs, text_splitter
from src.utils import process_uploaded_files

app = FastAPI(
    title="OrangeBot",
    description="""**OrangeBot** est chatbot spécialisé basé sur ChatGPT qui répond aux questions des utilisateurs grâce aux documents de référence qui sont fournis.""",
    version="0.1.0",
    contact={
        "name": "N'GUESSAN Kouakou Vincent",
    },
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/load_file")
def load_file(
    files: Annotated[
        list[UploadFile],
        File(
            title="The source documents",
            description="The source documents you wish to interact with.",
        ),
    ],
):
    if not os.path.isdir(config.STORE_FILE):
        documents, metadatas = process_uploaded_files(files, text_splitter)
        vectorize_and_store(documents, metadatas, config.STORE_FILE)

    return {"info": f"Documents are stored at {config.STORE_FILE}."}


@app.get("/question_answer")
async def question_answer(
    query: Annotated[
        str,
        Query(
            title="The user question",
            description="A string as a question to ask to the bot.",
        ),
    ]
):
    if not os.path.isdir(config.STORE_FILE):
        raise HTTPException(
            status_code=500,
            detail="Load your documents before starting a chat.",
        )
    vectorstore = get_vectorstore(config.STORE_FILE)
    chain = get_chain(
        model=config.CHAT_MODEL or "gpt-3.5-turbo",
        vectorstore=vectorstore,
        chain_type_kwargs=chain_type_kwargs,
    )
    return await chain.acall(query)
