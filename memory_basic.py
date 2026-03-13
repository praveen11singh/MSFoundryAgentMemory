import asyncio
import os
from dotenv import load_dotenv
from azure.core.exceptions import ResourceNotFoundError
from azure.identity.aio import ClientSecretCredential 
from azure.ai.projects.aio import AIProjectClient
from azure.ai.projects.models import (
    MemoryStoreDefaultDefinition,
    MemoryStoreDefaultOptions,
    MemorySearchOptions,
)

load_dotenv()

tenant_id = os.environ["AZURE_TENANT_ID"]
client_id = os.environ["AZURE_CLIENT_ID"]
client_secret = os.environ["AZURE_CLIENT_SECRET"]


async def main() -> None:

    endpoint = os.environ["AZURE_AI_PROJECT_ENDPOINT"]

    async with (
       ClientSecretCredential(
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret,
        ) as credential,
        AIProjectClient(endpoint=endpoint, credential=credential, allow_preview=True) as project_client,
    ):

        # Delete memory store, if it already exists
        memory_store_name = "pk1_memory_store"
        try:
            await project_client.beta.memory_stores.delete(memory_store_name)
            print(f"Memory store `{memory_store_name}` deleted")
        except ResourceNotFoundError:
            pass

        # Create a memory store
        definition = MemoryStoreDefaultDefinition(
            chat_model=os.environ["MEMORY_STORE_CHAT_MODEL_DEPLOYMENT_NAME"],
            embedding_model=os.environ["MEMORY_STORE_EMBEDDING_MODEL_DEPLOYMENT_NAME"],
            options=MemoryStoreDefaultOptions(
                user_profile_enabled=True, chat_summary_enabled=True
            ),  # Note: This line will not be needed once the service is fixed to use correct defaults
        )
        memory_store = await project_client.beta.memory_stores.create(
            name=memory_store_name,
            description="Example memory store for conversations",
            definition=definition,
        )
        print(f"Created memory store: {memory_store.name} ({memory_store.id}): {memory_store.description}")
        if isinstance(memory_store.definition, MemoryStoreDefaultDefinition):
            print(f"  - Chat model: {memory_store.definition.chat_model}")
            print(f"  - Embedding model: {memory_store.definition.embedding_model}")

        # Set scope to associate the memories with
        # You can also use "{{$userId}}" to take the oid of the request authentication header
        scope = "user_123"

        # Add a memory to the memory store
        update_poller = await project_client.beta.memory_stores.begin_update_memories(
            name=memory_store.name,
            scope=scope,
            items="I prefer dark roast coffee and usually drink it in the morning",  # Pass conversation items that you want to add to memory
            update_delay=0,  # Trigger update immediately without waiting for inactivity
        )

        # Wait for the update operation to complete, but can also fire and forget
        update_result = await update_poller.result()
        print(f"Updated with {len(update_result.memory_operations)} memory operations")
        for operation in update_result.memory_operations:
            print(
                f"  - Operation: {operation.kind}, Memory ID: {operation.memory_item.memory_id}, Content: {operation.memory_item.content}"
            )

        # Retrieve memories from the memory store
        search_response = await project_client.beta.memory_stores.search_memories(
            name=memory_store.name,
            scope=scope,
            items="What are my coffee preferences?",
            options=MemorySearchOptions(max_memories=5),
        )
        print(f"Found {len(search_response.memories)} memories")
        for memory in search_response.memories:
            print(f"  - Memory ID: {memory.memory_item.memory_id}, Content: {memory.memory_item.content}")

        # Delete memories for a specific scope
        await project_client.beta.memory_stores.delete_scope(name=memory_store.name, scope=scope)
        print(f"Deleted memories for scope '{scope}'")

        # Delete memory store
        await project_client.beta.memory_stores.delete(memory_store.name)
        print(f"Deleted memory store `{memory_store.name}`")


if __name__ == "__main__":
    asyncio.run(main())