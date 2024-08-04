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
            {"role": "system", "content": ("You are Groqy Fast; a fast AI chatbot based on Groq fast inference."
                                           "\nInstructions:"
                                           "\n- Be as verbose as needed."
                                           "\n- Your responses can be any length."
                                           "\n- say [<<FINISHED>>] at the end of your response if you have completely finished with the users request")},
        ]
        print("\nclass:unlimitedgen: loaded")
    
    async def gen(self, input):
        self.conversation_history.append({"role": "user", "content": input})
        self.run_groq()

    async def run_groq(self):
        total_response = ""
        start_time = time.time()
        response, token_count, max_tokens = await run_groq_response(self.conversation_history, max_tokens=8192)
        total_response = total_response + response
        self.conversation_history.append({"role": "assistant", "content": response})
        while response.find("<<FINISHED>>") == -1:
            
            self.conversation_history.append({"role": "user", "content": "continue your response\n- Be as verbose as needed.\n- Your responses can be any length.\n- say [<<FINISHED>>] at the end of your response if you have completely finished with the users request"})
            response, token_count, max_tokens = await run_groq_response(self.conversation_history, max_tokens=8192)
            
            total_response = total_response + response
            self.conversation_history.append({"role": "assistant", "content": response})
        end_time = time.time()
        print(f"Groqy took {end_time - start_time:.2f} seconds to respond.")
