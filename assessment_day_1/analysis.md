# Comparing a Plain Chatbot, a Rule-Based Workflow, and an AI Agent

## 1. Scenario

The scenario selected for this project is a **College Course Fee Assistant**. The system answers questions about course fees using a small private dataset.

The private course-fee data used in the project is:

| Course Code | Course Fee |
| ----------- | ---------: |
| CS101       |    ₹12,000 |
| AI202       |    ₹18,000 |
| DS303       |    ₹15,000 |

Example user requests include asking for the fee of a particular course, calculating the total fee of multiple courses, and calculating the final amount after applying a scholarship.

The same scenario is implemented using three different approaches: a plain chatbot, a rule-based workflow, and an AI agent.

---

## 2. Plain Chatbot

A plain chatbot mainly uses an LLM to understand the user's question and generate a response. It does not use external tools or a programmatic private-data lookup mechanism.

For example, if the user asks:

> What is the fee for AI202?

the LLM may generate:

> The fee for AI202 is ₹18,000.

However, the chatbot itself does not actually retrieve the value from the private course-fee data. The value must already be known to the model or included in its prompt or conversation context.

### Data Used

The chatbot mainly uses the information available in its conversation and the knowledge available to the LLM. It does not directly access the private course-fee data stored in the application.

### Tools and Rules

The plain chatbot does not use application tools such as `get_course_fee` or `calculator`. Its main component is the LLM.

### Request Handling

The user's question is sent to the LLM. The LLM interprets the question and generates a natural-language response.

### Limitations

The main limitation is that the chatbot cannot reliably retrieve changing private data unless that data is explicitly provided to it. It may also produce an incorrect answer if it does not know the current fee. Therefore, it is not suitable when accurate access to private and frequently changing information is required.

---

## 3. Rule-Based Workflow

The rule-based workflow solves the same problem using predefined programming rules. It does not use an LLM.

For example, the workflow can contain conditions such as:

* If the course code is `CS101`, return ₹12,000.
* If the course code is `AI202`, return ₹18,000.
* If the course code is `DS303`, return ₹15,000.

For a scholarship calculation, predefined mathematical operations can also be implemented in the program.

### Data Used

The rule-based workflow directly accesses the private course-fee data stored in the program or a local data source.

### Tools and Rules

It uses predefined rules, conditions, and calculations. There is no LLM involved.

### Request Handling

The workflow first identifies the course code using predefined logic. It then retrieves the corresponding fee and performs any predefined calculation required.

For example:

```text
User request
    ↓
Identify course
    ↓
Find matching course code
    ↓
Retrieve fee
    ↓
Apply predefined calculation
    ↓
Return result
```

### Limitations

The main limitation is flexibility. The workflow works well for requests that match its predefined conditions, but it may fail when users phrase questions differently or ask for a new type of operation that was not programmed.

For example, adding support for a new complex request may require writing additional conditions and modifying the program.

---

## 4. AI Agent

The AI agent combines an LLM, tools, and a loop. The LLM is responsible for deciding what actions are required, while tools provide access to private data and perform calculations.

The agent used in this project has tools such as:

* `get_course_fee`
* `calculator`

The agent follows the general process:

```text
User
 ↓
LLM
 ↓
Decide which tool is required
 ↓
Execute tool
 ↓
Observe tool result
 ↓
Decide whether another action is required
 ↓
Execute next tool if necessary
 ↓
Final answer
```

### Data Used

The AI agent can access the private course-fee data through the `get_course_fee` tool. Therefore, the LLM does not need to guess the fee.

### Tools and Rules

The agent uses:

* An LLM for reasoning and decision-making.
* `get_course_fee` for retrieving private course-fee information.
* `calculator` for arithmetic operations.
* A loop that allows the agent to perform multiple tool calls before producing the final answer.

### Request Handling

Consider the request:

> What is the total fee for CS101 and AI202 after a 10% scholarship?

The agent can perform the following steps:

```text
Step 1:
get_course_fee(CS101)
→ ₹12,000

Step 2:
get_course_fee(AI202)
→ ₹18,000

Step 3:
calculator((12000 + 18000) × (1 - 0.10))
→ ₹27,000

Final answer:
The total fee after a 10% scholarship is ₹27,000.
```

This demonstrates the agentic loop because the system does not simply execute one fixed sequence. The LLM decides which tools are required based on the user's request, receives the results, and continues until it can provide the final answer.

### Limitations

An AI agent is more flexible than a fixed workflow, but it introduces additional complexity. The model may select an inappropriate tool, misunderstand a request, or require safeguards around tool access. Therefore, tool validation, error handling, and controlled access to private data are important.

---

## 5. Comparison Table

| Basis for comparison     | Plain chatbot                                                                  | Rule-based workflow                               | AI agent                                                                  |
| ------------------------ | ------------------------------------------------------------------------------ | ------------------------------------------------- | ------------------------------------------------------------------------- |
| Flexibility              | High for natural-language conversation, but limited access to application data | Low to medium because behavior is predefined      | High because the LLM can adapt its tool usage to the request              |
| Decision-making          | LLM generates a response but does not perform application actions              | Decisions follow predefined conditions            | LLM decides which tools and actions are needed                            |
| Tool usage               | No application tools                                                           | Uses predefined program logic/functions           | Uses tools selected by the LLM                                            |
| Private-data access      | No direct access in this implementation                                        | Direct access to stored private data              | Accesses private data through controlled tools                            |
| Multi-step task handling | Limited                                                                        | Possible, but steps must be explicitly programmed | Can perform multiple tool calls through an agent loop                     |
| Automation               | Mainly response generation                                                     | Strong for predictable tasks                      | Strong for dynamic multi-step tasks                                       |
| Reliability              | Depends heavily on the LLM's available information                             | High for clearly defined cases                    | Can be reliable when tools, validation, and prompts are properly designed |

---

## 6. Suitability Analysis

For the College Course Fee Assistant scenario, the AI agent is suitable when users can ask different types of questions involving private data and multiple calculations.

The plain chatbot is useful for simple conversational questions, but it does not directly access the private course-fee data in this implementation. This creates a limitation when accurate and current private information is required.

The rule-based workflow provides direct access to the private data and can be reliable for predefined requests. However, its behavior must be explicitly programmed. New question types or more flexible requests may require additional rules.

The AI agent combines the advantages of natural-language understanding and controlled tool access. It can retrieve the required course fees and use a calculator for arithmetic. It can also perform multiple tool calls for a multi-step request. For this reason, the agent architecture provides a flexible way to handle the selected scenario, while still requiring proper tool validation and error handling.

---

## 7. Conclusion

A plain chatbot is most appropriate for simple conversational tasks where the required information is already available to the LLM or does not require external actions.

A rule-based workflow is appropriate when the problem has predictable inputs, clearly defined conditions, and deterministic steps. Examples include fixed validation processes, simple calculations, and predefined business rules.

An AI agent is appropriate when a task requires natural-language understanding, access to external or private data, multiple tools, and dynamic multi-step execution. The agent can interpret the user's request, select appropriate tools, observe their results, and continue taking actions until the task is completed.

The key distinction demonstrated by this project is that a plain chatbot primarily generates responses using an LLM, a rule-based workflow follows predefined programming logic without an LLM, while an AI agent combines an **LLM + Tools + Loop** to dynamically handle multi-step tasks.
