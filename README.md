# agentvisa-python

[![Tests](https://github.com/your-org/agentvisa-python/workflows/Tests/badge.svg)](https://github.com/your-org/agentvisa-python/actions)
[![PyPI version](https://badge.fury.io/py/agentvisa.svg)](https://badge.fury.io/py/agentvisa)
[![Python Support](https://img.shields.io/pypi/pyversions/agentvisa.svg)](https://pypi.org/project/agentvisa/)

The official Python SDK for the [AgentVisa API](https://agentvisa.dev). Simple, fast, and reliable.

## Quick Start

```bash
pip install agentvisa
```

```python
import agentvisa

# Initialize the SDK
agentvisa.init(api_key="your-api-key")

# Create a delegation
delegation = agentvisa.create_delegation(
    end_user_identifier="user123",
    scopes=["read", "write"]
)
print(f"Created delegation: {delegation['id']}")
```

## Installation

### Using pip
```bash
pip install agentvisa
```

### Using uv
```bash
uv add agentvisa
```

## Authentication

Get your API key from the [AgentVisa Dashboard](https://dashboard.agentvisa.dev).

```python
import agentvisa

agentvisa.init(api_key="av_1234567890abcdef")
```

## Usage

### Simple Interface (Recommended)

For most use cases, use the simple global interface:

```python
import agentvisa

# Initialize once
agentvisa.init(api_key="your-api-key")

# Create delegations
delegation = agentvisa.create_delegation(
    end_user_identifier="user123",
    scopes=["read", "write", "admin"],
    expires_in=7200  # 2 hours
)
```

### Client Interface

For advanced use cases or multiple configurations:

```python
from agentvisa import AgentVisaClient

# Create client instance
client = AgentVisaClient(api_key="your-api-key")

# Use the client
delegation = client.delegations.create(
    end_user_identifier="user123",
    scopes=["read", "write"],
    expires_in=3600
)
```

### Custom Base URL

```python
from agentvisa import AgentVisaClient

# For development or enterprise installations
client = AgentVisaClient(
    api_key="your-api-key",
    base_url="https://your-instance.agentvisa.dev/v1"
)
```

## API Reference

### Delegations

#### `create_delegation(end_user_identifier, scopes, expires_in=3600)`

Create a new agent delegation.

**Parameters:**
- `end_user_identifier` (str): Unique identifier for the end user
- `scopes` (List[str]): List of permission scopes
- `expires_in` (int): Expiration time in seconds (default: 3600)

**Returns:**
Dict containing delegation details including `id`, `token`, and `expires_at`.

**Example:**
```python
delegation = agentvisa.create_delegation(
    end_user_identifier="user123",
    scopes=["read", "write"],
    expires_in=7200
)
```

## Error Handling

The SDK raises standard Python exceptions:

```python
import agentvisa
from requests.exceptions import HTTPError

try:
    agentvisa.init(api_key="invalid-key")
    delegation = agentvisa.create_delegation("user123", ["read"])
except ValueError as e:
    print(f"Invalid input: {e}")
except HTTPError as e:
    print(f"API error: {e}")
except Exception as e:
    print(f"SDK not initialized: {e}")
```

## Development

### Setup

```bash
git clone https://github.com/your-org/agentvisa-python.git
cd agentvisa-python
make install
```

### Testing

```bash
make test
```

### Linting

```bash
make lint
```

### Type Checking

```bash
make typecheck
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`make test`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Support

- [Documentation](https://docs.agentvisa.dev)
- [API Reference](https://docs.agentvisa.dev/api)
- [Issues](https://github.com/your-org/agentvisa-python/issues)
- [Discord Community](https://discord.gg/agentvisa)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
