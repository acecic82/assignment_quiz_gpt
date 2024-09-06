from stmodule import getStreamlit as st
import streamlit
import json

from langchain.retrievers import WikipediaRetriever
from openai.error import AuthenticationError

from llmmodule import LLMManager
from level import Level

st().set_page_config(
    page_title="QuizGPT",
    page_icon="❓",
)

st().title("QuizGPT")

llmManager = LLMManager()


@streamlit.cache_data(show_spinner="Searching Wikipedia...")
def wiki_search(term):
    retriever = WikipediaRetriever(top_k_results=5)
    return retriever.get_relevant_documents(term)


@streamlit.cache_data(show_spinner="Making quiz.....")
def getResponse(topic, level, apiKey, _chain):
    try:
        response = _chain.invoke({"topic": topic})
        response = response.additional_kwargs["function_call"]["arguments"]

        return json.loads(response)
    except AuthenticationError:
        st().write("Invalid api key. Check your API key")
        return None


def makeLevel():
    level = st().selectbox(
        "Choose the level.",
        (
            Level.EASY.value,
            Level.HARD.value,
        ),
    )

    return Level.valueOf(level)


def makeLLM(apiKey, level):
    return llmManager.initLlm(apiKey, level)


with st().sidebar:
    docs = None
    chain = None

    apiKey = st().text_input("Please set an open ai api key")
    st().session_state["api_key"] = apiKey

    level = makeLevel()
    topic = st().text_input("Search Wikipedia...")

    if topic:
        chain = makeLLM(apiKey, level)
        if chain:
            docs = wiki_search(topic)

if not docs:
    st().markdown(
        """
            Welcome to QuizGPT.
                        
            I will make a quiz from Wikipedia articles or files you upload to test your knowledge and help you study.
                        
            Get started by uploading a file or searching on Wikipedia in the sidebar.
        """
    )

else:
    response = getResponse(topic, level, apiKey, chain)

    if response:
        with st().form("questions_form"):
            questionCnt = 0
            correct = 0
            for question in response["questions"]:
                st().write(question["question"])

                value = st().radio(
                    "Select an option.",
                    [answer["answer"] for answer in question["answers"]],
                    index=None,
                    key=questionCnt,
                )

                if {"answer": value, "correct": True} in question["answers"]:
                    st().success(value)
                    correct += 1
                else:
                    st().error(value)

                questionCnt += 1

            button = st().form_submit_button()

        if questionCnt == correct:
            st().balloons()
