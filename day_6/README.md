THE API CONTRACT:-
    -chat completions 
    -streaming
    -respponse style
    -tool schemas
    -parallel calls
    -malformed cells

-Tool calling in depth,validate and retry and inject faults

The req:
    model:ollama or vLLM or clouds
    meessage:-system role
             -user role
    temperature:0  for toools and facts
    max_tokens:
    stram(continuos ah answer thara mari):False

The res:
    choices:-role,content
            -finish reason
    usage:-prompt rokens,completuin tasks

Streaming:
    if we didn't stop the streaming it will continuously give outputs , so it may take more no of tokens

Compatible:
    tool call,structured outputs,seed and reproducibility,logprobs,error bodies

Tool calling :
    The shape os a tool call(5 Steps):
        -You send
        -Model replies
        -You run
        -result
        -final response

