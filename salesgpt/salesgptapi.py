import json
import asyncio  # Import asyncio for asynchronous operations
from custom_api_gpt import CustomAPI  # Import the CustomAPI class
from salesgpt.agents import SalesGPT  # Import the SalesGPT class

class SalesGPTAPI:
    def __init__(self, config_path, verbose=False, max_num_turns=10, use_tools=False):
        self.config_path = config_path
        self.verbose = verbose
        self.max_num_turns = max_num_turns
        self.USE_TOOLS = use_tools  # Initialize USE_TOOLS
        self.llm = CustomAPI(api_key="YOUR_API_KEY", app_id="YOUR_APP_ID")  # Use CustomAPI

    async def do(self, conversation_history, human_input=None):
        if self.config_path == '':
            print('No agent config specified, using a standard config')
            if self.USE_TOOLS:
                sales_agent = SalesGPT.from_llm(self.llm, use_tools=True,
                                                product_catalog="examples/sample_product_catalog.txt",
                                                salesperson_name="Ted Lasso",
                                                verbose=self.verbose)
            else:
                sales_agent = SalesGPT.from_llm(self.llm, verbose=self.verbose)
        else:
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
            except Exception as e:
                print(f"Error decoding the file: {e}")
                return

            if self.verbose:
                print(f'Agent config {config}')
            sales_agent = SalesGPT.from_llm(self.llm, verbose=self.verbose, **config)

        # Check turns
        current_turns = len(conversation_history) + 1
        if current_turns >= self.max_num_turns:
            print('Maximum number of turns reached - ending the conversation.')
            return "<END_OF_>"

        # Seed
        sales_agent.seed_agent()
        sales_agent.conversation_history = conversation_history

        if human_input is not None:
            sales_agent.human_step(human_input)

        # Interact with the custom API using stream
        generated_text = await self.llm.stream_chat(
            chatId="some_chat_id",
            messages=conversation_history,
            onMessage=self.on_message_received
        )

        # Add the generated text to the conversation history
        sales_agent.conversation_history.append(generated_text)

        # End conversation
        if '<END_OF_CALL>' in sales_agent.conversation_history[-1]:
            print('Sales Agent determined it is time to end the conversation.')
            return "<END_OF_CALL>"

        reply = sales_agent.conversation_history[-1]

        if self.verbose:
            print('=' * 10)
            print(f"{sales_agent.salesperson_name}:{reply}")

        return reply.split(": ")

    def on_message_received(self, text):
        # Handle the received text here
        print("Received:", text)

# Example usage (you'll need to adapt this to your specific use-case)
if __name__ == "__main__":
    api = SalesGPTAPI(config_path="", verbose=True, max_num_turns=10, use_tools=True)
    asyncio.run(api.do(conversation_history=[], human_input="Hello"))
