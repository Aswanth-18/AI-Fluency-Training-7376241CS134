# Day 3 Failure Log

## Failure 1: Missing webpage

Input:
data/missing.html

Expected failure:
The reader returns a file-not-found error.

Possible impact:
The agent cannot obtain the attendance records.

Fix:
Return a readable error message and instruct the agent not to invent data.

## Failure 2: Unknown tool

Test:
Request a tool name that is not in the tool registry.

Expected failure:
The dispatcher cannot find the requested tool.

Possible impact:
The agent may be unable to complete the requested action.

Fix:
Check the tool name against the registry and return an explicit error.

## Failure 3: Repeated tool call

Test:
Attempt the same tool call repeatedly with identical arguments.

Expected failure:
The basic agent may waste iterations repeating work.

Fix:
Store each tool name and its arguments. Block a repeated call.

## Failure 4: Oversized tool output

Test:
Read data/large_attendance.html.

Expected failure:
A large tool result consumes too much conversation context.

Fix:
Truncate the tool result before adding it to the conversation.

## Failure 5: Context budget exceeded

Test:
Process a conversation or tool result exceeding the configured budget.

Expected failure:
Further model calls may exceed the chosen context limit.

Fix:
Check the estimated context size before and after tool execution.
Stop safely when the budget is exceeded.

## Actual observations

Replace the expected failures above with what happened during
your own tests. Record the command, output, and whether the fix worked.