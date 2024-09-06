from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

from level import Level

quiz_function = {
    "name": "create_quiz",
    "description": "function that takes a list of questions and answers and returns a quiz",
    "parameters": {
        "type": "object",
        "properties": {
            "questions": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "question": {
                            "type": "string",
                        },
                        "answers": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "answer": {
                                        "type": "string",
                                    },
                                    "correct": {
                                        "type": "boolean",
                                    },
                                },
                                "required": ["answer", "correct"],
                            },
                        },
                    },
                    "required": ["question", "answers"],
                },
            }
        },
        "required": ["questions"],
    },
}


class LLMManager:

    def initLlm(self, apiKey, level):
        llm = ChatOpenAI(
            temperature=0.1,
            openai_api_key=apiKey,
        ).bind(
            function_call={
                "name": "create_quiz",
            },
            functions=[
                quiz_function,
            ],
        )

        if level == Level.EASY:
            prompt = PromptTemplate.from_template("Make a easy quiz about {topic}")
        else:
            prompt = PromptTemplate.from_template(
                "make a very difficult problem about the {topic}"
            )

        chain = prompt | llm
        return chain
