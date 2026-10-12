# Assessment Day 3: Build a ReAct Agent, Break It, and Fix It

## Aim

To implement a ReAct-based AI agent with tool calling, deliberately test failure conditions, and improve reliability using repeat detection, tool-output truncation, and a context-budget guard.

## Scenario

The Student Attendance and Eligibility Assistant reads a sample HTML attendance report, calculates attendance percentages, and determines whether students meet a minimum attendance requirement of 75%.

## Tools Used

1. **read_webpage:** Reads a local HTML file and returns its text.
2. **calculator:** Evaluates basic arithmetic expressions using a restricted arithmetic evaluator.

## ReAct Cycle

- **Reason:** Determine which information or calculation is required.
- **Act:** Call the appropriate tool.
- **Observe:** Read the tool result.
- **Repeat or respond:** Continue if more information is required, or provide the final answer.

## Failure Modes

1. Missing webpage or invalid file path.
2. Unknown tool name.
3. Repeated tool calls.
4. Oversized tool output.
5. Conversation exceeding the configured character budget.

## Reliability Improvements

- Validate tool names before execution.
- Return readable error messages instead of crashing.
- Detect repeated calls using tool names and arguments.
- Truncate large tool outputs before sending them back to the model.
- Check estimated conversation size and stop safely when the configured limit is exceeded.
- Apply a maximum number of agent iterations.

## Expected Results

Arun attended 85 out of 100 working days, resulting in 85% attendance. He meets the 75% requirement.

Priya attended 68 out of 100 working days, resulting in 68% attendance. She does not meet the 75% requirement.

The calculator should return 30 for 15% of 200.

## Conclusion

The experiment demonstrates a ReAct agent that interacts with tools and uses their results to answer questions. Failure testing highlights the risks of repeated calls, invalid tools, missing files, and large outputs. The fixed version introduces safeguards to improve execution reliability. Actual model outputs and observations should be recorded after running the experiments.