import os

import openai
from langchain.chains import LLMChain, SequentialChain
# from langchain.chat_models import ChatOpenAI
from langchain.chat_models import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.schema import HumanMessage, SystemMessage

from traceloop.sdk import Traceloop

Traceloop.init(app_name='langchain_example')


def langchain_app():
    chat = AzureChatOpenAI(
        openai_api_base=os.environ.get('OPENAI_API_BASE'),
        openai_api_version='2023-05-15',
        deployment_name='GPT-35-Turbo-4k',
        openai_api_key=os.environ.get('OPENAI_AZURE_API_KEY'),
        openai_api_type='azure',
        temperature=0,
    )

    first_prompt_messages = [
        SystemMessage(content='You are a funny sarcastic nerd.'),
        HumanMessage(content='Tell me a joke about OpenTelemetry.'),
    ]
    first_prompt_template = ChatPromptTemplate.from_messages(
        first_prompt_messages
    )
    first_chain = LLMChain(
        llm=chat, prompt=first_prompt_template, output_key='joke'
    )

    second_prompt_messages = [
        SystemMessage(content='You are an Elf.'),
        HumanMessagePromptTemplate.from_template(
            'Translate the joke below into Sindarin language:\n {joke}'
        ),
    ]
    second_prompt_template = ChatPromptTemplate.from_messages(
        second_prompt_messages
    )
    second_chain = LLMChain(llm=chat, prompt=second_prompt_template)

    workflow = SequentialChain(
        chains=[first_chain, second_chain], input_variables=[]
    )
    workflow({})


langchain_app()
