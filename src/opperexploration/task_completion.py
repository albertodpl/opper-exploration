"""Task completion module for Opper AI exploration"""

from opperai import Opper
import os
from pydantic import BaseModel, Field
from typing import List

opper = Opper(http_bearer=os.getenv("OPPER_API_KEY", ""))


# Input schema with field descriptions
class KBQueryInput(BaseModel):
    facts: List[str] = Field(description="Standalone facts to answer from")
    question: str = Field(description="The question to answer")


# Output schema with field descriptions
class KBQueryOutput(BaseModel):
    thoughts: str = Field(description="Elaborate step-by-step reasoning")
    answer: str = Field(description="Concise answer to the question")


# Task definition and completion run
response = opper.call(
    name="mini_kb_query",
    instructions="Given the list of bullet-point facts, answer the question.",
    input_schema=KBQueryInput,
    output_schema=KBQueryOutput,
    input={
        "facts": [
            "Jupiter is the largest planet in the Solar System.",
            "The Great Red Spot is a giant storm on Jupiter.",
            "Saturn possesses the most extensive ring system in the Solar System.",
        ],
        "question": "Which planet hosts the Great Red Spot?",
    },
)

print(response.json_payload)
# {'thoughts': "From the facts provided, I know that Jupiter is the largest planet in the Solar System and that the Great Red Spot is a giant storm. This clearly links the Great Red Spot to Jupiter. Facts about Saturn's ring system are unrelated to the question. Therefore, the planet hosting the Great Red Spot is Jupiter.", 'answer': 'Jupiter'}
