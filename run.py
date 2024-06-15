import gradio as gr
import argparse
import logging
from llama_index.core.base.llms.types import (
    ChatMessage,
    MessageRole,
)
from agent.librarian import Librarian


def predict(user_input, _):
    """
    Wrapper around the GUI, called each time a new message is triggered.

    :param user_input: message inserted by the user.
    """
    # User friendly way to stream response 
    msg = agent.use_query_engine(ChatMessage(content=user_input, role=MessageRole.USER))
    return msg.response


# Serve the server 
demo = gr.ChatInterface(predict)
# Arguments with sensible default values
parser = argparse.ArgumentParser()
parser.add_argument("--name", type=str, default="Razvan")
parser.add_argument(
    "--model_id", type=str, default="meta-llama/Meta-Llama-3-8B-Instruct"
)
parser.add_argument("--lib_path", type=str, default="./books") 
args, unknown = parser.parse_known_args()

# Configure the logger to facilitate development
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("debug.log")],
)

# Create the agent
agent = Librarian(name=args.name, lib_path=args.lib_path, model_id=args.model_id)


if __name__ == "__main__":
    demo.queue().launch()
