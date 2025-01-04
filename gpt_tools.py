from openai import AsyncOpenAI
import os
from termcolor import colored
import asyncio

class GPTChat:
    def __init__(self, sys_message, model='gpt-4o'):
        self.messages = [{'role': 'system', 'content': sys_message}]
        self.model = model
        try:
            self.client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))
            print(colored("✓ OpenAI client initialized successfully", "green"))
        except Exception as e:
            print(colored(f"✗ Error initializing OpenAI client: {str(e)}", "red"))
            raise

    def add_message(self, role, content):
        self.messages.append({'role': role, 'content': content})
        print(colored(f"→ Added {role} message", "cyan"))

    async def get_gpt_response(self, user_input):
        self.add_message('user', user_input)
        
        try:
            print(colored("→ Sending request to OpenAI...", "yellow"))
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                temperature=0.3,
                stream=True
            )

            responses = ""
            async for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    response_content = chunk.choices[0].delta.content
                    responses += response_content
                    print(response_content, end='', flush=True)

            self.add_message('assistant', responses)
            print(colored("\n✓ Response received and processed", "green"))
            return responses

        except Exception as e:
            error_msg = f"✗ Error getting GPT response: {str(e)}"
            print(colored(error_msg, "red"))
            raise

    def get_completion(self, user_input):
        """Synchronous wrapper for getting GPT completion"""
        return asyncio.run(self.get_gpt_response(user_input))