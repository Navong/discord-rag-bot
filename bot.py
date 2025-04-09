# bot.py
from interactions import Client, Intents, listen, slash_command, slash_option, OptionType, File, SlashContext, Permissions
from dotenv import load_dotenv
import os
import aiohttp
from langchain_core.messages import SystemMessage, HumanMessage
from utils import update_index, agent_executor, reset_index

load_dotenv()
bot = Client(intents=Intents.ALL)


@listen()
async def on_ready():
    print("Ready")


@listen()
async def on_message_create(event):
    print(f"message received: {event.message.content}")


@slash_command(name="query", description="Enter your query :)")
@slash_option(
    name="input_text",
    description="input text",
    required=True,
    opt_type=OptionType.STRING,
)

async def get_response(ctx: SlashContext, input_text: str):

    await ctx.defer()
    config = {"configurable": {"thread_id": str(ctx.channel.id)}}
    input_message = input_text.strip()

    system_prompt = SystemMessage(
    content=(
        "You are a helpful assistant. "
        "Use only the retrieved content from the database to answer questions. "
        "If the information is not found in the database, respond with: "
        "'I'm sorry, I couldn't find information about that in the available documents.' "
        "Do not use outside knowledge. "
        "Keep answers concise and factual. "
        "Limit your response to 1 sentences only."
    )
)

    final_ai_message = None
    for event in agent_executor.stream(
        {
            "messages": [system_prompt, HumanMessage(content=input_message)]
        },
        stream_mode="values",
        config=config,
    ):
        for message in event["messages"]:
            if message.type == "ai":
                final_ai_message = message

    full_response = final_ai_message

    if full_response:
        content = full_response.content
        if len(content) > 2000:
            for i in range(0, len(content), 2000):
                # await ctx.send(content[i:i+2000])
                await ctx.send(f'**Input Query**: {input_text}\n\n{content[i:i+2000]}')
        else:
            await ctx.send(f'**Input Query**: {input_text}\n\n{content}')
    else:
        await ctx.send("Sorry, I couldn't generate a response.")


@slash_command(name="updatedb", description="Update your information database :)")
@slash_option(
    name="file",
    description="PDF file to update the index",
    opt_type=OptionType.ATTACHMENT,
    required=True,
)
async def updated_database(ctx: SlashContext, file: File):

    await ctx.defer(ephemeral=True)


    await ctx.send("Downloading and processing the document. This might take a moment...")


    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(file.url) as resp:
                if resp.status == 200:
                    with open("./pdf/latest.pdf", "wb") as f:
                        f.write(await resp.read())
                else:
                    await ctx.send(f"Failed to download the file (status {resp.status})")
                    return
    except Exception as e:
        await ctx.send(f"Failed to save the uploaded file: {e}")
        return

    update = await update_index(file_path="./pdf/latest.pdf")
    if update:
        response = f'✅ Updated {sum(update)} document chunks.'
    else:
        response = f'Error updating index.'
    await ctx.send(response)

@slash_command(
    name="resetdb",
    description="Reset the vector store to empty",
    default_member_permissions=Permissions.ADMINISTRATOR  # 🛡️ Only admins
)
async def reset_database(ctx: SlashContext):
    await ctx.defer()
    try:
        reset_index()
        await ctx.send("The vector store has been reset.")
    except Exception as e:
        await ctx.send(f"Failed to reset DB: {e}")

# summarize
@slash_command(name="summarize", description="Summarize the current document in the database.")
@slash_option(
    name="doc_type",
    description="Type of the document to customize summary style",
    required=True,
    opt_type=OptionType.STRING,
    choices=[
        {"name": "Normal", "value": "normal"},
        {"name": "Research Paper", "value": "research"},
    ],
)
async def summarize_vector_db(ctx: SlashContext, doc_type: str):
    await ctx.defer()

    # Set prompt based on document type
    if doc_type == "research":
        prompt_content = (
            "You are an expert summarizer for academic research papers. "
            "Summarize the content in the vector database using the following structure:\n"
            "**Background:**\n...\n"
            "**Methods:**\n...\n"
            "**Results:**\n...\n"
            "**Conclusion:**\n..."
        )
    else:
        prompt_content = (
            "You are a helpful assistant that summarizes the content in the vector database. "
            "Give a concise summary of the most important points covered in the document."
        )

    system_prompt = SystemMessage(content=prompt_content)

    # Ask the agent to summarize the entire DB context
    query = "Please summarize the content in the vector database."

    final_ai_message = None
    for event in agent_executor.stream(
        {
            "messages": [system_prompt, HumanMessage(content=query)]
        },
        stream_mode="values",
        config={"configurable": {"thread_id": str(ctx.channel.id)}}
    ):
        for message in event["messages"]:
            if message.type == "ai":
                final_ai_message = message

    if final_ai_message:
        summary = final_ai_message.content
        if len(summary) > 2000:
            for i in range(0, len(summary), 2000):
                await ctx.send(summary[i:i+2000])
        else:
            await ctx.send(f"**Summary:**\n{summary}")
    else:
        await ctx.send("Sorry, I couldn't generate a summary.")




bot.start(os.getenv("DISCORD_BOT_TOKEN"))