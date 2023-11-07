import openai

# Set your OpenAI API key
api_key = "your_api_key"
openai.api_key = api_key

# Initialize the OpenAI client
def chatgpt_conversation(conversation_log):
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=conversation_log
    )

    conversation_log.append({
        'role': response.choices[0].message.role, 
        'content': response.choices[0].message.content.strip()
    })
    return conversation_log

question = "Как дела у тебя?"
conversations = []
conversations.append({'role': 'user', 'content': question})
conversations = chatgpt_conversation(conversations)
# Вывод ответа в print
print(conversations[-1]['content'].strip())
