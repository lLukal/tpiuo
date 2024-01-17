import asyncio
import json
from azure.eventhub.aio import EventHubConsumerClient
import logging


eventhub_connection_str = "Endpoint=sb://tpiuo-lab-1.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=RilKYmaWgqcJeM4RZWbm/tTUOWh2O9cbT+AEhHNgK7k="
eventhub_name = "tpiuo-1-1"


async def on_event(partition_context, event):
    #print(f'Received event: "{json.loads(event.body_as_str(encoding="UTF-8")).get("title")}" from partition with ID: "{partition_context.partition_id}"')
    logging.warning(f'Received event: "{json.loads(event.body_as_str(encoding="UTF-8"))}" from partition with ID: "{partition_context.partition_id}"')
    # To print whole event:
    print(f'Received event: "{event.body_as_str(encoding="UTF-8")}" from partition with ID: "{partition_context.partition_id}"')


async def main():
    consumer_client = EventHubConsumerClient.from_connection_string(
        eventhub_connection_str,
        consumer_group="$Default",
        eventhub_name=eventhub_name
    )
    async with consumer_client:
        # -1 = read from beginning
        await consumer_client.receive(on_event=on_event, starting_position="-1")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

# Test Change Test 