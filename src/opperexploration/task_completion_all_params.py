"""Task completion module for Opper AI exploration"""

from opperai import Opper
import os
from pydantic import BaseModel, Field
from typing import List, Literal

opper = Opper(http_bearer=os.getenv("OPPER_API_KEY", ""))


# Input schema with field descriptions
class KBQueryInput(BaseModel):
    facts: List[str] = Field(description="Standalone facts to answer from")
    question: str = Field(description="The question to answer")


# Output schema with field descriptions
class KBQueryOutput(BaseModel):
    thoughts: str = Field(description="Elaborate step-by-step reasoning")
    classification: Literal["easy", "medium", "hard"] = Field(
        description="The difficulty of the question"
    )
    answer: str = Field(
        description="Concise answer to the question",
        pattern=r"^The answer to the question is [A-Za-z0-9\s]+$",
    )


# Task definition and completion run
response = opper.call(
    name="mini_kb_query",
    tags={
        "user": "lofkrantz",
        "env": "development",
    },
    model=[
        {  # first model to try
            "name": "openai/gpt-4o-mini",  # the model name
            "options": {
                "temperature": 0.1  # the options for the model
            },
        },
        {"name": "openai/gpt-4o"},  # second model to try
    ],
    instructions="Given the list of bullet-point facts, answer the question.",
    input_schema=KBQueryInput,
    output_schema=KBQueryOutput,
    input={
        "facts": [
            "Jupiter is the largest planet in the Solar System.",
            "The Great Red Spot is a giant storm on Jupiter.",
            "Saturn possesses the most extensive ring system in the Solar System.",
        ],
        # "question": "Which planet hosts the Great Red Spot?",
        "question": "How many planets are in the Solar System?",
    },
    # Example of how to handle the situation if there are no facts for the question.
    # You can add several examples. They will help the model to understand the task better.
    examples=[
        {
            "input": KBQueryInput(
                facts=[
                    "Jupiter is the largest planet in the Solar System.",
                    "The Great Red Spot is a giant storm on Jupiter.",
                    "Saturn possesses the most extensive ring system in the Solar System.",
                ],
                question="How many planets are in the Solar System?",
            ),
            "output": KBQueryOutput(
                thoughts="To determine the answer, I reviewed the provided facts. The facts discuss Jupiter, its Great Red Spot, and Saturn's extensive ring system, but they do not specify how many planets are in the Solar System. Without relevant information, the question cannot be answered based on these facts alone",
                classification="hard",
                answer="The answer to the question is unknown",
            ),
        }
    ],
)

print(response.json_payload)
# {'thoughts': "From the facts provided, I know that Jupiter is the largest planet in the Solar System and that the Great Red Spot is a giant storm. This clearly links the Great Red Spot to Jupiter. Facts about Saturn's ring system are unrelated to the question. Therefore, the planet hosting the Great Red Spot is Jupiter.", 'answer': 'Jupiter'}
