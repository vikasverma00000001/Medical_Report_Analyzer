
import os
from langchain_core.messages import (SystemMessage,HumanMessage)
from langchain_groq import ChatGroq
from utils.prompts import SYSTEM_PROMPT


class MedicalLLM:

    def __init__(self):

        self.llm = ChatGroq(

            api_key=os.getenv("GROQ_API_KEY"),

            model="llama-3.1-8b-instant",

            temperature=0

        )

    def generate_answer(

        self,

        prompt

    ):

        messages = [

            SystemMessage(

                content=SYSTEM_PROMPT

            ),

            HumanMessage(

                content=prompt

            )

        ]

        response = self.llm.invoke(

            messages

        )

        return response.content

    def generate_summary(self, context):
        from langchain_core.messages import (
            SystemMessage,
            HumanMessage
        )

        from utils.summary_prompt import (
            SUMMARY_SYSTEM_PROMPT,
            build_summary_prompt
        )

        prompt = build_summary_prompt(context)

        messages = [

            SystemMessage(
                content=SUMMARY_SYSTEM_PROMPT
            ),

            HumanMessage(
                content=prompt
            )

        ]

        response = self.llm.invoke(messages)

        return response.content

    def generate_insights(self, context):
        from langchain_core.messages import (
            SystemMessage,
            HumanMessage
        )

        from utils.insights_prompt import (
            INSIGHTS_SYSTEM_PROMPT,
            build_insights_prompt
        )

        prompt = build_insights_prompt(context)

        messages = [

            SystemMessage(
                content=INSIGHTS_SYSTEM_PROMPT
            ),

            HumanMessage(
                content=prompt
            )

        ]

        response = self.llm.invoke(messages)

        return response.content