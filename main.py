from dotenv import load_dotenv
import os
from unlimitedgen import unlimitedgen
import asyncio
load_dotenv()


def main():
    unlimited = unlimitedgen()
    while True:
        user_input = input("Enter your message: ")
        if user_input == "exit":
            break
        #print(f"You entered: {user_input}")
        asyncio.run(unlimited.gen(user_input))


if __name__ == "__main__":
    main()
