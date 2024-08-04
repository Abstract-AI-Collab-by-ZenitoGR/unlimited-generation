import time
from typing import Literal
import asyncio
from libs.groq import groq_response, groq_streaming
async def run_groq_streaming(messages):
    response = ""
    async for delta in groq_streaming(messages):
        if delta is not None:
            response += delta
            print(delta, end="", flush=True)
    return response

async def run_groq_response(messages,max_tokens=8192):
    return await groq_response(messages,max_tokens=max_tokens)
        
    

class unlimitedgen():
    def __init__(self):
        self.conversation_history = [
            {"role": "system", "content": 
                ("You are Groqy Fast; a fast AI chatbot based on Groq fast inference."
                "\nInstructions:"
                "\n- Be as verbose as needed."
                "\n- Your responses can be any length."
                "\n- if you are asked for a any number of items respond with one by one, once reached max_tokens respond with <<CONTINUEGEN>>"
                "\n- if you have completely finished with the users request (all items) respond with <<FINISHED>>"
                "\n- your code includes running requests when reached max_tokens until you have finished all items"
                "\n- note: your code includes running requests when reached max_tokens until you have finished all items \n"
                "so do not shorten your generations"
                )
            },
        ]
        print("\nclass:unlimitedgen: loaded")
    
    async def gen(self, input):
        self.conversation_history.append({"role": "user", "content": input})
        await self.run_groq()

    async def run_groq(self):
        total_response = ""
        total_completion_tokens = 0
        start_time = time.time()
        response, completion_tokens, max_tokens = await run_groq_response(self.conversation_history, max_tokens=8192)
        end_time_single = time.time()
        print (f"Groq took {end_time_single - start_time:.2f} seconds to respond.")
        print(response)
        total_response = total_response + response
        total_completion_tokens = total_completion_tokens + completion_tokens
        self.conversation_history.append({"role": "assistant", "content": response})
        while response.find("<<FINISHED>>") == -1:
            
            self.conversation_history.append(
                {"role": "user", "content": 
                    (
                        "\n- Be as verbose as needed."
                        "\n- Your responses can be any length."
                        "\n- continue generating items one by one, once reached max_tokens respond with <<CONTINUEGEN>>"
                        "\n- if you have completely finished with the users request (all items) respond with <<FINISHED>>"
                        "\n- note: your code includes running requests when reached max_tokens until you have finished all items \n"
                        "so do not shorten your generations"
                    )
                })
                    
            start_time_single = time.time()
            response, completion_tokens, max_tokens = await run_groq_response(self.conversation_history, max_tokens=8192)
            print(response)
            end_time_single = time.time()
            print(f"Groq took {end_time_single - start_time_single:.2f} seconds to respond.")
            total_response = total_response + response
            
            total_completion_tokens = total_completion_tokens + completion_tokens
            self.conversation_history.append({"role": "assistant", "content": response})
        end_time = time.time()
        print(f"Unlimited generation took {end_time - start_time:.2f} seconds.")
