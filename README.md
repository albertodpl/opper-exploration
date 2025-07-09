# Opper AI Exploration

This repository contains examples and experiments using the Opper AI SDK, demonstrating various capabilities of the unified AI API for building model-independent, structured, and performant AI applications.

## Overview

Opper is a Unified API that makes it easy to build AI code that is model independent, structured and performant. This project explores key Opper concepts through practical examples.

## Getting Started

### Prerequisites

- Python 3.8+
- An Opper AI API key (get one at https://platform.opper.ai)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/albertodpl/opper-exploration.git
cd opper-exploration
```

2. Set up virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your OPPER_API_KEY
```

## Examples

### Basic Usage

**Room Information Extraction** (`getting_started.py`)
- Demonstrates structured data extraction from unstructured text
- Shows input/output schema definitions with Pydantic models
- Example of field descriptions for model prompting

```bash
source venv/bin/activate && source .env && python src/opperexploration/getting_started.py
```

**Knowledge Base Query** (`task_completion.py`)
- Shows knowledge base creation and querying
- Demonstrates semantic search and retrieval
- Example of structured responses with references

```bash
source venv/bin/activate && source .env && python src/opperexploration/task_completion.py
```

### Advanced Features

- **Tests and Evaluations** (`tests_and_evals.py`) - Testing AI functions with metrics and evaluations
- **Tracing and Metrics** (`tracing_and_metrics.py`) - Multi-step workflow tracing
- **In-Context Learning** (`in_context_learning.py`) - Using examples to improve model performance
- **Custom Knowledge Base** (`custom_knowledge.py`) - Support ticket management system
- **Task Completion at Scale** (`task_completion_at_scale.py`) - Batch processing examples

## Key Concepts

- **Call**: Structured interaction with generative models using input/output schemas
- **Span**: Logging and tracing mechanism for AI operations
- **Metric**: Evaluation and feedback system for model outputs
- **Dataset**: Ground truth collections for testing and examples
- **Knowledge Base**: Semantic search-enabled database for AI applications

## Development

### Linting and Formatting

```bash
# Check code style
source venv/bin/activate && ruff check src/

# Format code
source venv/bin/activate && ruff format src/
```

### Project Structure

```
src/opperexploration/
├── getting_started.py               # Room extraction example
├── task_completion.py               # Knowledge base query example
├── tests_and_evals.py               # Testing and evaluation example
├── tracing_and_metrics.py          # Tracing and evaluation
├── in_context_learning.py          # Example-based learning
├── custom_knowledge.py             # Support ticket management
├── task_completion_at_scale.py     # Batch processing
└── task_completion_all_params.py   # Comprehensive parameter usage
```

## Contributing

1. Follow the existing code style and patterns
2. Add examples that demonstrate specific Opper capabilities
3. Include clear documentation and comments
4. Test your examples before submitting

## License

This project is for educational and exploration purposes. Please refer to Opper AI's terms of service for usage guidelines.