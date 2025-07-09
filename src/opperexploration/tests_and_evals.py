"""Tests and evaluations example for Opper AI exploration"""

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


def test_room_extraction():
    """Test room extraction functionality with evaluation metrics"""
    opper = Opper(http_bearer=os.getenv("OPPER_API_KEY"))

    # Test case 1: Basic room extraction
    test_input = "The Grand Hotel offers a luxurious suite with 3 spacious rooms, each providing a breathtaking view of the ocean. The suite includes a king-sized bed, an en-suite bathroom, and a private balcony for an unforgettable stay."

    # Assumes that the function 'extractRoom' is already defined and available in the Opper AI environment
    completion = opper.call(
        name="extractRoom",
        instructions="Extract details about the room from the provided text",
        input=test_input,
        output_schema=RoomDescription,
    )

    result = completion.json_payload
    print("Test 1 - Basic extraction:")
    print(f"Result: {result}")

    # Evaluation 1: Check if all required fields are present
    required_fields = ["room_count", "view", "bed_size", "hotel_name"]
    has_all_fields = all(field in result for field in required_fields)

    opper.span_metrics.create_metric(
        span_id=completion.span_id,
        dimension="has_all_required_fields",
        value=1 if has_all_fields else 0,
        comment="Checks if all required fields are present in the output",
    )

    # Evaluation 2: Check if room count is reasonable (1-10)
    room_count_valid = 1 <= result.get("room_count", 0) <= 10

    opper.span_metrics.create_metric(
        span_id=completion.span_id,
        dimension="room_count_valid",
        value=1 if room_count_valid else 0,
        comment="Checks if room count is within reasonable range (1-10)",
    )

    # Evaluation 3: Check if hotel name is extracted correctly
    expected_hotel = "The Grand Hotel"
    hotel_correct = result.get("hotel_name", "").lower() == expected_hotel.lower()

    opper.span_metrics.create_metric(
        span_id=completion.span_id,
        dimension="hotel_name_accuracy",
        value=1 if hotel_correct else 0,
        comment="Checks if hotel name is extracted correctly",
    )

    print(f"✅ All fields present: {has_all_fields}")
    print(f"✅ Room count valid: {room_count_valid}")
    print(f"✅ Hotel name correct: {hotel_correct}")
    print()


def test_edge_cases():
    """Test edge cases and error handling"""
    opper = Opper(http_bearer=os.getenv("OPPER_API_KEY"))

    # Test case 2: Minimal information
    test_input_minimal = "A room at Hotel ABC with a bed."

    completion = opper.call(
        name="extractRoom",
        instructions="Extract details about the room from the provided text",
        input=test_input_minimal,
        output_schema=RoomDescription,
    )

    result = completion.json_payload
    print("Test 2 - Minimal information:")
    print(f"Result: {result}")

    # Evaluation: Check if model handles minimal information gracefully
    has_reasonable_defaults = (
        result.get("room_count", 0) >= 1
        and result.get("hotel_name", "") != ""
        and result.get("bed_size", "") != ""
    )

    opper.span_metrics.create_metric(
        span_id=completion.span_id,
        dimension="handles_minimal_info",
        value=1 if has_reasonable_defaults else 0,
        comment="Checks if model handles minimal information with reasonable defaults",
    )

    print(f"✅ Handles minimal info: {has_reasonable_defaults}")
    print()


def test_multiple_scenarios():
    """Test multiple scenarios to evaluate consistency"""
    opper = Opper(http_bearer=os.getenv("OPPER_API_KEY"))

    test_cases = [
        {
            "name": "Luxury suite",
            "input": "The Ritz Carlton presidential suite features 5 rooms with stunning mountain views and a California king bed.",
            "expected_hotel": "The Ritz Carlton",
        },
        {
            "name": "Budget hotel",
            "input": "Budget Inn room 101 has twin beds and overlooks the parking lot.",
            "expected_hotel": "Budget Inn",
        },
        {
            "name": "Boutique hotel",
            "input": "The Artisan Hotel offers a cozy single room with garden view and queen bed.",
            "expected_hotel": "The Artisan Hotel",
        },
    ]

    accuracy_scores = []

    for i, test_case in enumerate(test_cases, 3):
        print(f"Test {i} - {test_case['name']}:")

        completion = opper.call(
            name="extractRoom",
            instructions="Extract details about the room from the provided text",
            input=test_case["input"],
            output_schema=RoomDescription,
        )

        result = completion.json_payload
        print(f"Result: {result}")

        # Check hotel name accuracy
        hotel_correct = (
            test_case["expected_hotel"].lower() in result.get("hotel_name", "").lower()
        )
        accuracy_scores.append(1 if hotel_correct else 0)

        opper.span_metrics.create_metric(
            span_id=completion.span_id,
            dimension="hotel_extraction_accuracy",
            value=1 if hotel_correct else 0,
            comment=f"Hotel name accuracy for {test_case['name']}",
        )

        print(f"✅ Hotel name accuracy: {hotel_correct}")
        print()

    # Overall accuracy metric
    overall_accuracy = sum(accuracy_scores) / len(accuracy_scores)
    print(f"Overall hotel extraction accuracy: {overall_accuracy:.2%}")


def main():
    """Run all tests and evaluations"""
    print("🧪 Running Opper AI Tests and Evaluations")
    print("=" * 50)

    test_room_extraction()
    test_edge_cases()
    test_multiple_scenarios()

    print("✅ All tests completed!")


if __name__ == "__main__":
    main()
