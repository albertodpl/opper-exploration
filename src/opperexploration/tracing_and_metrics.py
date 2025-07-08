"""Tracing and metrics module for Opper AI exploration"""

from opperai import Opper
import os
from pydantic import BaseModel, Field


# Initialize Opper client
opper = Opper(http_bearer=os.getenv("OPPER_API_KEY"))


# Input schema for person analysis
class PersonAnalysisInput(BaseModel):
    name: str = Field(description="Person's name")
    age: int = Field(description="Person's age")
    city: str = Field(description="Person's city of residence")


# Output schema for person analysis
class PersonAnalysisOutput(BaseModel):
    profile_summary: str = Field(description="Brief summary of the person's profile")
    insights: str = Field(description="Key insights about the person")
    recommendations: str = Field(description="Recommendations or suggestions")


# Create a function in Opper AI
function_name = "analyze_person_data"

# Check if function exists
try:
    function = opper.functions.get_by_name(name=function_name)
    print(f"Function '{function_name}' already exists with ID: {function.id}")
except Exception:
    print(f"Function '{function_name}' does not exist. Creating it...")
    function = opper.functions.create(
        name=function_name,
        instructions="Analyze this person's data and provide insights about their profile. Include a summary, key insights, and recommendations.",
        input_schema=PersonAnalysisInput.model_json_schema(),
        output_schema=PersonAnalysisOutput.model_json_schema(),
        configuration={"invocation.few_shot.count": 2},
    )
    print(f"Created function '{function_name}' with ID: {function.id}")

# Create a trace to track this processing session
session_span = opper.spans.create(name="person_data_processing")

# Sample data to process
sample_data = [
    {"name": "Alice", "age": 30, "city": "New York"},
    {"name": "Bob", "age": 25, "city": "San Francisco"},
    {"name": "Charlie", "age": 35, "city": "Chicago"},
    {"name": "Diana", "age": 28, "city": "Boston"},
]

personas = []
for record in sample_data:
    # Analyze the record and connect it to the trace
    completion = opper.functions.call(
        function_id=function.id,
        input=record,
        parent_span_id=session_span.id,
    )

    analysis = completion.json_payload
    personas.append(analysis)

    print(f"Analysis for {record['name']}: {analysis}")

# Update the trace with input and output information
opper.spans.update(
    span_id=session_span.id,
    input=str(sample_data),
    output=str(personas),
    meta={"n_records": len(sample_data)},
)

# Save a metric that captures number of personas that are blank
# and attach it to the root span
opper.span_metrics.create_metric(
    span_id=session_span.id,
    dimension="n_failed",
    value=sum(1 for persona in personas if persona is None),
    comment="Number of personas with failed summary",
)
