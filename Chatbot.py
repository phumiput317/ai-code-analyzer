print("=== Simple AI Chatbot Test ===")
print("พิมพ์ 'exit' เพื่อออก")

while True:
    user_message = input("You: ")

    if user_message.lower() == "exit":
        print("Bot: Goodbye!")
        break

    if "hello" in user_message.lower():
        response = "Hello! How can I help you?"

    elif "name" in user_message.lower():
        response = "I'm your AI Assistant."

    elif "sql" in user_message.lower():
        response = "SQL is a language used to manage and query databases."

    else:
        response = "Sorry, I don't understand your question yet."

    print("Bot:", response)