"""Task completion module for Opper AI exploration"""

import os
from typing import List

from opperai import Opper
from pydantic import BaseModel, Field


# Input schema with field descriptions
class KBQueryInput(BaseModel):
    facts: List[str] = Field(description="Standalone facts to answer from")
    question: str = Field(description="The question to answer")


# Output schema with field descriptions
class KBQueryOutput(BaseModel):
    thoughts: str = Field(description="Elaborate step-by-step reasoning")
    answer: str = Field(
        description=(
            "Concise answer to the question starting with "
            "'The answer to the question is '"
        ),
        pattern=r"^The answer to the question is [A-Za-z0-9\s ]+$",
    )


def main():
    opper = Opper(http_bearer=os.getenv("OPPER_API_KEY", ""))

    # Create a function in Opper AI
    function_name = "mini_kb_query2"

    # Check if function exists
    try:
        function = opper.functions.get_by_name(name=function_name)
        print(f"Function '{function_name}' already exists with ID: {function.id}")
    except Exception:
        print(f"Function '{function_name}' does not exist. Creating it...")
        function = opper.functions.create(
            name=function_name,
            instructions=(
                "Given the list of bullet-point facts, then answer the question."
            ),
            input_schema=KBQueryInput.model_json_schema(),
            output_schema=KBQueryOutput.model_json_schema(),
            configuration={"invocation.few_shot.count": 3},
        )
        print(f"Created function '{function_name}' with ID: {function.id}")

    # Completion run
    response = opper.functions.call(
        function_id=function.id,
        input={
            "facts": [
                "Jupiter is the largest planet in the Solar System.",
                "The Great Red Spot is a giant storm on Jupiter.",
                "Saturn possesses the most extensive ring system in the Solar System.",
            ],
            "question": "What planet has the largest ring system?",
        },
    )

    print(response.json_payload)


if __name__ == "__main__":
    main()
