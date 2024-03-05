import os
from langchain.chains import LLMChain
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

MODEL_NAME='gpt-3.5-turbo-16k'

def summary_fn(input_text:str,prompt:str, format_string=None):
    print("*"*20)
    print(input_text)
    print("*" * 20)
    llm = ChatOpenAI(model_name=MODEL_NAME,temperature=0)
    '''
    Provided the Input Text(Raw extracted text), Conversion format (format_string) and the prompt 
    prompt the OpenAi model and return the response received 
    '''
    template = """{prompt}
    The Sample JSON format -{format_string}

    \n\nThe input content is : {input}
    \n\nThe final json result is :"""
    try:
        print('#'*20,"in side try")
        prompt_template = PromptTemplate(input_variables=["prompt", "format_string","input"], template=template)
        print(prompt_template)
        llm_chain = LLMChain(llm=llm, prompt=prompt_template, output_key="result")

        output = llm_chain.invoke({'prompt':prompt, 'format_string':format_string,'input': input_text })
        print(output)
        return output
    except Exception as e:
        print("error in formatting is-----------",{e})
        return None
     