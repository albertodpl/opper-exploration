"""In-context learning module for Opper AI exploration"""

from opperai import Opper
from pydantic import BaseModel, Field
from typing import List
import os


# --------- Schemas --------- #


class RoomDatabaseEntry(BaseModel):
    hotel_name: str = Field(description="Name of the hotel offering the room")
    room_count: int = Field(description="Number of rooms in the suite")
    view: str = Field(description="Type of view from the room, e.g., ocean, city")
    beds: int = Field(description="Number of beds in the room")
    price_per_night: float = Field(description="Cost of the room per night in USD")
    amenities: List[str] = Field(
        description="List of amenities available in the room, e.g., wifi, breakfast, parking"
    )


class RoomDescription(BaseModel):
    description: str = Field(
        description="A natural language description of the room suitable for customers"
    )


def setup_function(opper: Opper):
    """Setup and return the room description function."""
    function_name = "generate_room_description"
    function = None

    # Try to get existing function first
    try:
        function = opper.functions.get_by_name(name=function_name)
        print(f"Function '{function_name}' already exists with ID: {function.id}")
        return function
    except Exception:
        print(f"Function '{function_name}' does not exist. Creating it...")

    # If function doesn't exist, create it
    try:
        function = opper.functions.create(
            name=function_name,
            instructions="Given a room database entry, describe the room in a way that is easy to understand and use for a customer.",
            input_schema=RoomDatabaseEntry.model_json_schema(),
            output_schema=RoomDescription.model_json_schema(),
            configuration={"invocation.few_shot.count": 3},
        )
        print(f"Created function '{function_name}' with ID: {function.id}")
        return function
    except Exception as e:
        print(f"Error creating function: {e}")
        raise RuntimeError(
            f"Failed to create or retrieve function '{function_name}'"
        ) from e


def add_examples(opper: Opper, dataset_id: str):
    """Create example datasets for few-shot learning (only if dataset is empty)."""

    # Check if dataset already has entries
    try:
        dataset_entries = opper.datasets.list_entries(dataset_id=dataset_id)
        if len(dataset_entries.data) > 0:
            print(
                f"Dataset {dataset_id} already has {len(dataset_entries.data)} entries. Skipping example addition."
            )
            return
    except Exception as e:
        print(
            f"Could not check existing dataset entries: {e}. Proceeding with example addition."
        )

    examples = [
        {
            "input": RoomDatabaseEntry(
                hotel_name="Seaside Resort",
                room_count=2,
                view="ocean",
                beds=1,
                price_per_night=250,
                amenities=["wifi", "room service", "minibar", "balcony"],
            ).model_dump(),
            "output": RoomDescription(
                description="This room at Seaside Resort features an elegant 2-room oceanfront suite with a comfortable king bed and private balcony offering stunning ocean views. Premium amenities include complimentary WiFi, personalized room service, and a well-stocked minibar. Perfect for couples seeking a romantic getaway or honeymooners looking for luxury and privacy."
            ).model_dump(),
            "comment": "Example of a luxury oceanview suite with emphasis on romantic atmosphere",
        },
        {
            "input": RoomDatabaseEntry(
                hotel_name="Mountain Lodge",
                room_count=3,
                view="mountain",
                beds=4,
                price_per_night=350,
                amenities=["wifi", "fireplace", "kitchen", "ski storage", "parking"],
            ).model_dump(),
            "output": RoomDescription(
                description="This room at Mountain Lodge features a spacious 3-room suite with 4 comfortable beds, a fully equipped kitchen, and a cozy fireplace. The breathtaking mountain views complement modern amenities like WiFi and convenient ski storage, with complimentary parking included. Ideal for families or groups of friends planning an active mountain getaway."
            ).model_dump(),
            "comment": "Example of a family-friendly mountain suite with practical amenities",
        },
        {
            "input": RoomDatabaseEntry(
                hotel_name="Urban Boutique Hotel",
                room_count=1,
                view="city",
                beds=1,
                price_per_night=150,
                amenities=["wifi", "workspace", "coffee maker", "gym access"],
            ).model_dump(),
            "output": RoomDescription(
                description="This room at Urban Boutique Hotel features a modern space with a comfortable queen bed, dedicated workspace, and spectacular city views. Amenities include complimentary high-speed WiFi, an in-room coffee maker, and access to our fitness center. Perfect for business travelers who need a productive and convenient city-center base."
            ).model_dump(),
            "comment": "Example of a business-oriented city room with focus of productivity",
        },
    ]

    print(f"Adding {len(examples)} examples to empty dataset {dataset_id}...")

    # Add examples to the dataset
    added_count = 0
    for i, example in enumerate(examples, 1):
        try:
            opper.datasets.create_entry(
                dataset_id=dataset_id,
                input=str(example["input"]),
                output=str(example["output"]),
                comment=str(example["comment"]),
            )
            print(f"  ✓ Added example {i}: {example['comment']}")
            added_count += 1
        except Exception as e:
            print(f"  ✗ Error adding example {i}: {e}")

    print(f"Successfully added {added_count}/{len(examples)} examples to dataset")


def main():
    opper = Opper(http_bearer=os.getenv("OPPER_API_KEY", ""))
    function = setup_function(opper)

    print(f"Function dataset_id: {function.dataset_id}")
    add_examples(opper, function.dataset_id)

    # Test the function with an example
    print("\n=== Testing Function ===")
    test_input = RoomDatabaseEntry(
        hotel_name="Test Hotel",
        room_count=1,
        view="garden",
        beds=2,
        price_per_night=100,
        amenities=["wifi", "breakfast"],
    )

    response = opper.functions.call(
        function_id=function.id, input=test_input.model_dump()
    )

    print(f"Test input: {test_input}")
    print(f"Generated description: {response.json_payload}")


if __name__ == "__main__":
    main()
