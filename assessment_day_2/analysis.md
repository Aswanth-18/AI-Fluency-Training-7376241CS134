# Assessment Day 2 - Reasoning and Acting

## Scenario

This assessment uses an e-commerce shopping assistant.

Product prices:

- Laptop = Rs. 60,000
- Monitor = Rs. 15,000
- Keyboard = Rs. 2,000

The system uses two tools:

- get_product_price()
- calculator()

---

## 1. ReAct

Question:

Which is cheaper: buying a Laptop and Monitor with a 10% discount,
or buying a Laptop, Monitor and Keyboard with a 15% discount?
By how much?

### Expected Calculation

Option 1:

(60000 + 15000) * 0.90 = Rs. 67,500

Option 2:

(60000 + 15000 + 2000) * 0.85 = Rs. 65,450

Difference:

67500 - 65450 = Rs. 2,050

The second option is cheaper by Rs. 2,050.

The ReAct agent obtains product prices using tools and uses the
calculator tool for arithmetic.

---

## 2. Direct Prompting vs Chain-of-Thought

The same reasoning questions were tested using:

1. Direct prompting
2. Chain-of-Thought prompting

Direct prompting asks only for the final answer.

CoT prompting asks the model to solve the problem step by step.

### Observation

Direct prompting generally produces shorter responses.

CoT provides intermediate calculations and reasoning, making it
easier to inspect how the answer was obtained.

---

## 3. Self-Consistency

The first reasoning question was executed multiple times with:

Temperature = 0.8

Number of runs = 5

The final answers were collected and the majority answer was selected.

Self-consistency can reduce the effect of occasional inconsistent
reasoning by selecting the most common answer among multiple attempts.

---

## 4. Comparison

| Method | Tools | Reasoning visibility | Speed | Consistency |
|--------|-------|----------------------|-------|-------------|
| Direct Prompting | No | Low | Fast | High at temp 0 |
| Chain-of-Thought | No | Higher | Slower | High at temp 0 |
| ReAct | Yes | High | Slower | Depends on tool execution |
| Self-Consistency | No | Higher | Slowest | Majority-based |

---

## 5. Conclusion

Direct prompting is useful for simple questions where only the final
answer is required.

Chain-of-Thought is useful for multi-step reasoning because it produces
intermediate calculations.

ReAct is useful when the problem requires external information or tools.

Self-consistency can be used when multiple reasoning attempts are
available and a majority answer is useful.