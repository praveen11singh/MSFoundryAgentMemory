
from azure.ai.projects.aio import AIProjectClient
from azure.ai.projects.models import MemoryStoreDefaultDefinition
import asyncio
import os
from dotenv import load_dotenv
from azure.core.exceptions import ResourceNotFoundError
from azure.identity.aio import DefaultAzureCredential

load_dotenv()


async def main() -> None:

    endpoint = os.environ["AZURE_AI_PROJECT_ENDPOINT"]

    async with (
        DefaultAzureCredential() as credential,
        AIProjectClient(endpoint=endpoint, credential=credential) as project_client,
    ):

        # Delete memory store, if it already exists
        memory_store_name = "pk_memory_store"
        try:
            await project_client.beta.memory_stores.delete(memory_store_name)
            print(f"Memory store `{memory_store_name}` deleted")
        except ResourceNotFoundError:
            pass

        # Create Memory Store
        definition = MemoryStoreDefaultDefinition(
            chat_model=os.environ["MEMORY_STORE_CHAT_MODEL_DEPLOYMENT_NAME"],
            embedding_model=os.environ["MEMORY_STORE_EMBEDDING_MODEL_DEPLOYMENT_NAME"],
        )
        memory_store = await project_client.beta.memory_stores.create(
            name=memory_store_name,
            description="Example memory store for conversations",
            definition=definition,
        )
        print(f"Created memory store: {memory_store.name} ({memory_store.id}): {memory_store.description}")

        # Get Memory Store
        get_store = await project_client.beta.memory_stores.get(memory_store.name)
        print(f"Retrieved: {get_store.name} ({get_store.id}): {get_store.description}")

        # Update Memory Store
        updated_store = await project_client.beta.memory_stores.update(
            name=memory_store.name,
            description="Updated description",
        )
        print(f"Updated: {updated_store.name} ({updated_store.id}): {updated_store.description}")

        # List Memory Store
        memory_stores = []
        async for store in project_client.beta.memory_stores.list(limit=10):
            memory_stores.append(store)
        print(f"Found {len(memory_stores)} memory stores")
        for store in memory_stores:
            print(f"  - {store.name} ({store.id}): {store.description}")

        # Delete Memory Store
        delete_response = await project_client.beta.memory_stores.delete(memory_store.name)
        print(f"Deleted: {delete_response.deleted}")


if __name__ == "__main__":
    asyncio.run(main())