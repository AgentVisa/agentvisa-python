# AgentVisa Python SDK

[![Tests](https://github.com/AgentVisa/agentvisa-python/workflows/Tests/badge.svg)](https://github.com/AgentVisa/agentvisa-python/actions)
[![PyPI version](https://badge.fury.io/py/agentvisa.svg)](https://badge.fury.io/py/agentvisa)
[![Python Support](https://img.shields.io/pypi/pyversions/agentvisa.svg)](https://pypi.org/project/agentvisa/)

The official Python SDK for the [AgentVisa API](https://agentvisa.dev).

## Quick Start

```bash
uv add agentvisa
```

```python
import agentvisa

# Initialize the SDK
agentvisa.init(api_key="your-api-key")

# Create a delegation (type defaults to "ephemeral")
delegation = agentvisa.create_delegation(
    end_user_identifier="user123",
    scopes=["read", "write"],
)
print(f"Credential: {delegation['credential'][:12]}... (agent_id={delegation['agent_id']})")
```

## Installation

```bash
uv add agentvisa
```

## Authentication

Get your API key from the [AgentVisa Dashboard](https://agentvisa.dev/dashboard).

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
    expires_in=7200,  # 2 hours
    metadata={"description": "Test agent"},
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

## Integrating with LangChain

You can easily secure LangChain agents by creating a custom tool that wraps AgentVisa. This ensures that every time an agent needs to perform a privileged action, it acquires a fresh, scoped, short-lived credential tied to the end-user.

This example shows how to create a secure "email sending" tool.

### 1. Create the AgentVisa-powered Tool

The tool's `_run` method will call `agentvisa.create_delegation` to get a secure token just before it performs its action.

```python
from langchain.tools import BaseTool
import agentvisa

# Initialize AgentVisa once in your application
agentvisa.init(api_key="your-api-key")

class SecureEmailTool(BaseTool):
    name = "send_email"
    description = "Use this tool to send an email."

    def _run(self, to: str, subject: str, body: str, user_id: str):
        """Sends an email securely using an AgentVisa token."""
        
        # 1. Get a short-lived, scoped credential from AgentVisa
        try:
            delegation = agentvisa.create_delegation(
                end_user_identifier=user_id,
                scopes=["send:email"]
            )
            token = delegation.get("credential")
            print(f"Successfully acquired AgentVisa for user '{user_id}' with scope 'send:email'")
        except Exception as e:
            return f"Error: Could not acquire AgentVisa. {e}"

        # 2. Use the token to call your internal, secure email API
        # Your internal API would verify this token before sending the email.
        print(f"Calling internal email service with token: {token[:15]}...")
        # response = requests.post(
        #     "https://internal-api.yourcompany.com/send-email",
        #     headers={"Authorization": f"Bearer {token}"},
        #     json={"to": to, "subject": subject, "body": body}
        # )
        
        # For this example, we'll simulate a successful call
        return "Email sent successfully."

    async def _arun(self, to: str, subject: str, body: str, user_id: str):
        # LangChain requires an async implementation for tools
        raise NotImplementedError("SecureEmailTool does not support async")
```

### 2. Add the Tool to your Agent

Now, you can provide this tool to your LangChain agent. When the agent decides to use the `send_email` tool, it will automatically generate a new, auditable AgentVisa.

```python
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI

# Initialize your LLM
llm = ChatOpenAI(model_name="gpt-5-2025-08-07", temperature=0)

# Create an instance of your secure tool
tools = [SecureEmailTool()]

# Initialize the agent
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Run the agent
# The agent will correctly parse the user_id and pass it to the tool
agent.run("Please send an email to team@example.com with the subject 'Project Update' and body 'The new feature is live.' for user_id 'user_anne'.")
```

This pattern provides the perfect combination of LangChain's powerful reasoning capabilities with AgentVisa's secure, auditable credentialing system.

## API Reference

### Delegations

#### `create_delegation(end_user_identifier, scopes, expires_in=3600, *, delegation_type="ephemeral", metadata=None, timeout=15)`

Create a new agent delegation.

**Parameters:**
- `end_user_identifier` (str): Unique identifier for the end user
- `scopes` (List[str]): List of permission scopes
- `expires_in` (int): Expiration time in seconds (default: 3600)

**Returns:**
Dict containing delegation details including `agent_id`, `credential`, and `expires_at`.
For backward compatibility the dict also includes aliases: `id` mirrors `agent_id`, and `token` mirrors `credential`.

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

### Check the code
Run all checks (format, lint, typecheck, test)

```bash
make check
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

- [Documentation](https://agentvisa.dev/docs)
- [Issues](https://github.com/AgentVisa/agentvisa-python/issues)
- [Discord Community](https://discord.gg/ZupkwFbvqC)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
