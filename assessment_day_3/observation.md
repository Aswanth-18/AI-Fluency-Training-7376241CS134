# Day 3 Observations

## Test 1: Arun

Input:
Read the attendance report and calculate Arun's attendance.

Expected calculation:
(85 / 100) * 100 = 85%

Expected conclusion:
Arun meets the 75% requirement.

## Test 2: Priya

Input:
Read the attendance report and calculate Priya's attendance.

Expected calculation:
(68 / 100) * 100 = 68%

Expected conclusion:
Priya does not meet the 75% requirement.

## Test 3: Calculator

Input:
What is 15% of 200?

Expected result:
30

## Test 4: Missing webpage

Expected behavior:
The tool returns an error instead of inventing attendance records.

## Test 5: Large report

Expected behavior:
The fixed agent truncates oversized tool output and checks
its configured context budget.

## Comparison

Basic agent:
- Does not detect identical tool calls explicitly.
- Does not truncate tool results.
- Does not check a configured conversation character budget.
- Uses a maximum step limit.

Fixed agent:
- Detects repeated tool calls.
- Truncates large tool results.
- Checks its estimated conversation size.
- Stops safely when its guards trigger.

Actual results:
Update this section after running the scripts.