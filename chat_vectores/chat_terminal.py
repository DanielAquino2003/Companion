import requests

def chat_loop(ia_name):
    print(f"Chat with IA '{ia_name}'. Type 'exit' to quit.")
    while True:
        user_input = input("Tú: ")
        if user_input.lower() == "exit":
            break
        res = requests.post(f"http://localhost:8000/chat/{ia_name}", params={"user_message": user_input})
        print("IA:", res.json()["response"])


if __name__ == "__main__":
    ia_name = input("Introduce el nombre de la IA: ")
    chat_loop(ia_name)