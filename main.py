from dotenv import load_dotenv
import os
from unlimitedgen import unlimitedgen
import asyncio
load_dotenv()


async def main():
    unlimited = unlimitedgen()
    while True:
        user_input = input("Enter your message (type exit to stop): ")
        if user_input == "exit":
            break
        #print(f"You entered: {user_input}")
        await unlimited.gen(user_input)


if __name__ == "__main__":
    asyncio.run(main())
