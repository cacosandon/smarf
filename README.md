
# SCAF: Smart, Code-Aware Functions

SCAF (Smart, Code-Aware Functions) is a Python library that provides intelligent, context-aware function calls using LLMs. It analyzes the context in which it's called and performs appropriate operations based on the available variables and inferred intent.

## Installation

To install SCAF, use pip:
```bash
pip install scaf
```

Or if you're using Poetry:

```bash
poetry add scaf
```

## Usage

```python
from scaf.smart_call import smart_call

def get_country_data(city: str):
    country = smart_call(city)

    return {
        "country_name": country["name"],
        "country_code": country["code"],
        "country_flag_emoji": country["emoji"],
    }
```

## License

This project is licensed under the MIT License.