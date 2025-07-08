"""Main module for Opper AI exploration"""

from opperai import Opper

# Our SDK supports Pydantic to provide structured output
from pydantic import BaseModel
import os


# Define the output structure
class RoomDescription(BaseModel):
    room_count: int
    view: str
    bed_size: str
    hotel_name: str


def main():
    opper = Opper(http_bearer=os.getenv("OPPER_API_KEY"))

    # Complete a task
    completion = opper.call(
        name="extractRoom",
        instructions="Extract details about the room from the provided text",
        input="The Grand Hotel offers a luxurious suite with 3 spacious rooms, each providing a breathtaking view of the ocean. The suite includes a king-sized bed, an en-suite bathroom, and a private balcony for an unforgettable stay.",
        output_schema=RoomDescription,
    )

    print(completion.json_payload)
    # {'room_count': 3, 'view': 'ocean', 'bed_size': 'king-sized', 'hotel_name': 'The Grand Hotel'}


if __name__ == "__main__":
    main()
