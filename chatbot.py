import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

# Load API key from .env
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("❌ GROQ_API_KEY not found. Add it to your .env file.")

# Initialize Groq LLM
llm = ChatGroq(
    api_key=api_key,
    model="llama-3.1-8b-instant",  # Fast and capable model
    temperature=0.7,  # Adjust for creativity (0-2)
    max_tokens=1000   # Limit response length
)

# Memory to remember past conversation
memory = ConversationBufferMemory()

# Create chatbot chain
chatbot = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True
)

# Chat loop
print("🤖 Groq Chatbot ready! Type 'exit' to quit.\n")
while True:
    try:
        user_input = input("You: ").strip()
        
        if user_input.lower() == "exit":
            print("Goodbye 👋")
            break
            
        if not user_input:
            print("⚠️ Please type something!")
            continue
            
        response = chatbot.predict(input=user_input)
        print("Bot:", response)
        
    except Exception as e:
        print("⚠️ Error:", e)