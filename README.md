# SMAF: Smart, Code-Aware Functions

SMAF (Smart, Code-Aware Functions) is a Python library that provides intelligent, context-aware function calls using LLMs. It analyzes the context in which it's called and performs appropriate operations based on the available variables and inferred intent.

For now, it only works with OpenAI models (gpt-4o-mini). So set your `OPENAI_API_KEY` environment variable.

## Installation

To install SMAF, use pip:
```bash
pip install smaf
```

Or if you're using Poetry:

```bash
poetry add smaf
```

## Usage

```python
from smaf.smart_call import smart_call

def get_country_data(city: str):
    country_data = smart_call()

    return {
        "country_name": country_data["name"],
        "country_code": country_data["code"],
        "country_flag": country_data["emoji"],
    }
```

## License

This project is licensed under the MIT License.