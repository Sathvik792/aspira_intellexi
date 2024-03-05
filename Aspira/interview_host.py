import os
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
import json
from langchain_openai.llms import OpenAI
from langchain.chains import LLMChain
from langchain.schema import AIMessage, HumanMessage


class Host:
    class RelevanceEvalutor(BaseModel):
        relevant: bool = Field(
            description="Given response is relevant to the question or not"
        )
        follow_up_question: str = Field(
            description="Best possible next question for the question asked and the user response"
        )
        answered: bool = Field(
            description="The response completely answers the question or not or shall we ask a follow-up question again?"
        )

    def __init__(self,main_question) -> None:
        self.main_question = main_question
        self.model = OpenAI()
        self.template = """You are an intelligent assistant tasked to mimic humans in responding to a response for a given question. Understand the context of the question and check if the response is relevant and completely answers the question.
        
        1. If the response is relevant but doesnot answer the question completly come up with a follow-up question strictly based on the context of the given question and the provided answer in order to fully answer the question.
        2. If the response is not relevant ask the follow up question requesting for a valid response for getting a response that completely answers the question.
        3. If the response for a question is relevant and completely answers the question then do not ask a follow up question.
        4. At any point to avoid confusion always refer to the first question in the conversation for any explanations if asked by the user.
        5. Avoid any follow up question once the question is completely answered.
        6. Avoid asking any general questions apart from those required by the main question.
        7. In cases where you identify mismatch across the question and the answer or if the answer does not seem to match the entity type required ask for clarification from the user.
        8. Strictly follow the above instructions and finally return an output json that complys with the provided format instructions.
        
        Conversation History: {chat_history}
        
        The format: {format_instructions}
        Main Question is :{main_question}
        Question is : {question}
        User response is : {answer}

        The Output Json is :"""
        self.json_parser = JsonOutputParser(pydantic_object=self.RelevanceEvalutor)
        self.chat_history = []

        self.prompt = PromptTemplate(
            template=self.template,
            input_variables=["question", "answer", "chat_history", "main_question"],
            partial_variables={
                "format_instructions": self.json_parser.get_format_instructions()
            },
        )

        self.chain = LLMChain(prompt=self.prompt, llm=self.model)

    def check_relevance(self, question, answer):
        response = self.chain.invoke(
            {
                "question": question,
                "answer": answer,
                "chat_history": self.chat_history,
                "main_question": self.main_question,
            }
        )
        print(type(response),"   Response    :  ", response)
        eval_details = response["text"]
        try:
            if eval_details:
                self.chat_history.append(AIMessage(content=question))
                self.chat_history.append(HumanMessage(content=answer))
            print(type(eval_details),"Eval Details    :",eval_details)
            details = self.json_parser.parse(eval_details)
            print("Details    :  ",details)
            return details
        except :
            self.chat_history.pop()
            self.chat_history.pop()
            return self.check_relevance(question=question,answer="")

class Synthesizer:
    def __init__(self, main_question, follow_ups: list) -> None:
        self.main_question = main_question
        self.follow_ups = follow_ups
        self.template = """You are an intelligent assistant tasked to understand the conversation over the follow up questions in getting the desired result from the user.
        And return the final response for the question thorugh understanding the context from all the answers by the user for the follow up questions asked.
        1. Strictly understand the context of the main question.
        2. Identify the context in the questions asked and answers provided by the user.
        3. While returning the final answer do not give any self referential phrases, instead return the answer directly.
         
        The question to be answered is:
        {main_question}
        
        The conversational Question and Answers are:
        {follow_ups}
        
        the final answer is:
        """
        self.prompt = PromptTemplate(
            template=self.template, input_variables=["main_question", "follow_ups"]
        )

        self.llm = OpenAI()

        self.chain = LLMChain(prompt=self.prompt, llm=self.llm)

    def get_answer(self):
        response = self.chain.invoke(
            {"main_question": self.main_question, "follow_ups": self.follow_ups}
        )
        # response = self.chain.invoke(
        #     {"main_question": self.main_question, "follow_ups": self.host.chat_history}
        # )
        print("response is     ---", response)
        print(response["text"])
        return response["text"]


class Evaluator(BaseModel):
    story_name: bool = Field(
        description="The story name describes the core functionality or feature being developed or tested."
    )
    missing_points: str = Field(
        description="The set of steps that were missed in the UserStory generated from the TestCase Scenarios."
    )
    summary: str = Field(
            description="It describes about the resemblance analysis of the testcase scenarios and the Userstory, steps missed and the coverage result."
    )

    coverage_percentage: int = Field(
            description="The percentage measure of the userstory generated as per given testcase scenarios."
    )

