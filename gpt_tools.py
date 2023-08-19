import openai

class GPTChat:
    def __init__(self, sys_message, model='gpt-3.5-turbo-16k-0613'):
        self.messages = [{'role': 'system', 'content': sys_message}]
        self.model = model

    def add_message(self, role, content):
        self.messages.append({'role': role, 'content': content})

    def get_gpt3_response(self, user_input):
        self.add_message('user', user_input)
        
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.messages,
            temperature=0.3,
            stream=True
        )

        responses = ""

        for chunk in response:
            response_content = chunk.get("choices", [{}])[0].get("delta", {}).get("content")
            if response_content:
                responses += response_content
                print(response_content, end='', flush=True)

        self.add_message('assistant', responses)

        return responses