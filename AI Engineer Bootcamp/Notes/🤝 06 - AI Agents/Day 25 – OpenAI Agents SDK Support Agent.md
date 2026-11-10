## 1. Objective

Explore the OpenAI Agents SDK and build a basic customer-support agent for a fictional e-commerce company called ShopEase.

The agent is designed to help customers:

- Check order status.
    
- Retrieve return and refund policies.
    
- Handle invalid order IDs without inventing order information.
    

**Learning constraint:** OpenAI API credits were unavailable, so live LLM execution was not performed. Local mock tools and `ScriptedModel` were used for testing.

## 2. Tech Stack

- Python 3.12
    
- OpenAI Agents SDK (`openai-agents` 0.24.0)
    
- Streamlit (installed for the project)
    
- python-dotenv
    
- ScriptedModel for deterministic testing
    

## 3. Project Structure

```
openai-agents-support-agent/
│
├── app/
│   ├── mock_data.py
│   ├── support_tools.py
│   ├── agent.py
│   ├── main.py
│   ├── test_support.py
│   ├── test_agent_tools.py
│   ├── test_agent.py
│   └── test_scenarios.py
│
├── .env
├── .gitignore
└── requirements.txt
```

Do not commit `.env` or `.venv`.

## 4. Core Concepts Learned

### 4.1 Agent

An Agent represents an AI agent with a name, instructions, model configuration, and available tools.

```
support_agent = Agent(
    name="ShopEaseSupportAgent",
    model="gpt-4.1-mini",
    instructions="You are a customer support assistant.",
    tools=[lookup_order, check_return_policy]
)
```

The model configuration is defined, but actual model execution was not tested because API credits were unavailable.

### 4.2 Function Tools

The `@function_tool` decorator exposes Python functions as tools that an agent can call.

```
@function_tool
def lookup_order(order_id: str) -> str:
    result = get_order_status(order_id)
    return str(result)
```

Another tool retrieves the return policy:

```
@function_tool
def check_return_policy() -> str:
    result = get_return_policy()
    return str(result)
```

### 4.3 Runner

`Runner.run()` executes an agent with a supplied input.

```
result = await Runner.run(
    support_agent,
    "Where is my order ORD1001?"
)
```

A live run using the configured OpenAI model requires API access. We did not perform one.

### 4.4 ScriptedModel

`ScriptedModel` is available through `agents.testing`.

It allows predefined model outputs to be supplied for deterministic tests without contacting a live LLM.

Useful helpers explored:

- `ScriptedModel`
    
- `function_call()`
    
- `assistant_message()`
    

Example:

```
scripted_model = ScriptedModel(
    steps=[
        {
            "output": [
                function_call(
                    name="lookup_order",
                    arguments={"order_id": "ORD1001"},
                    call_id="call_001"
                )
            ]
        },
        {
            "output": [
                assistant_message(
                    "Your order ORD1001 has been shipped."
                )
            ]
        }
    ]
)
```

The scripted model simulates the tool-call decision and final response. It does not demonstrate autonomous LLM reasoning.

## 5. Mock Data and Tools

Three sample orders were created:

|Order ID|Customer|Status|Amount|
|---|---|---|---|
|ORD1001|Alex|Shipped|₹1,499|
|ORD1002|Sam|Delivered|₹799|
|ORD1003|Jordan|Processing|₹2,499|

Return policy:

- Return window: 7 days.
    
- Refund processing: 5–7 business days.
    
- Product must be eligible for return.
    

## 6. Testing Performed

### Test 1 – Mock functions

Verified:

- Existing order lookup.
    
- Another existing order lookup.
    
- Invalid order lookup.
    
- Return-policy retrieval.
    

### Test 2 – SDK tool registration

Confirmed that the agent registered:

- `lookup_order`
    
- `check_return_policy`
    

### Test 3 – Scripted agent execution

Used `ScriptedModel` and `Runner.run()` to simulate an order-status request.

Expected response:

> Your order ORD1001 has been shipped. The order amount is ₹1,499.

### Test 4 – Multiple scripted scenarios

|Scenario|Expected outcome|Result|
|---|---|---|
|ORD1001|Order shipped|Passed|
|ORD9999|Order not found|Passed|
|Return policy|7-day return window|Passed|

**Testing limitation:** The final responses were predefined. These tests validate the scripted execution workflow, not genuine model reasoning or the model's ability to interpret tool results.

## 7. Important Learnings

1. An Agent combines instructions, model configuration, and tools.
    
2. Function tools connect Python functionality to an agent.
    
3. Runner is used to execute an agent.
    
4. ScriptedModel enables deterministic tests without live model calls.
    
5. Mock testing and genuine LLM testing are different.
    
6. API billing and SDK implementation are separate concerns.
    

## 8. What Was Not Explored

Due to the lack of API credits, the following remain unverified:

- Genuine LLM-driven tool selection.
    
- Model reasoning using actual tool results.
    
- Multi-turn conversational memory.
    
- Handoffs between multiple agents.
    
- Guardrails and input/output validation.
    
- Live tracing and observability.
    
- End-to-end live customer-support interaction.
    

These are potential topics for future exploration when API access is available.

## 9. Interview Questions

**Q1. What is the OpenAI Agents SDK?**

It is a Python SDK for building agents that can use tools and execute agent workflows.

**Q2. What is a function tool?**

A Python function exposed to an agent so it can perform a specific operation.

**Q3. What is the purpose of Runner?**

It executes an agent with a given input and returns the run result.

**Q4. What is ScriptedModel?**

A testing utility that simulates model outputs using predefined steps, enabling deterministic testing without live LLM calls.

**Q5. What is the difference between mock testing and live agent testing?**

Mock testing uses predefined data and outputs. Live agent testing uses a real model that interprets requests, selects tools, and generates responses dynamically.

## 10. Day 25 Conclusion

Completed a basic customer-support agent structure using the OpenAI Agents SDK. Implemented mock order and policy tools, registered them with the agent, and tested scripted execution.

The fundamental SDK concepts were explored, but genuine LLM-driven behaviour remains untested due to API credit limitations.