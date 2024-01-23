import asyncio
import datetime
import json
from azure.eventhub.aio import EventHubConsumerClient
from azure.storage.blob.aio import ContainerClient
import logging


eventhub_connection_str = "Endpoint=sb://tpiuo-lab-1.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=RilKYmaWgqcJeM4RZWbm/tTUOWh2O9cbT+AEhHNgK7k="
eventhub_name = "tpiuo-1-1"
storage_account_name = "tpiuostorageaccount"
storage_account_key = "avGmQ9MEDbN8Lq19nc9T33+DJIBKBSc1b4Fa6Y71Z3GOOekbMZV2YWaUGenYonGn+RcYcU62i9x++ASt61SYdg=="
container_name = "newcontainer"


async def save_to_data_lake(data, created_time):
    try:
        blob_path = f"{created_time.year}/{created_time.month:02d}/{created_time.day:02d}/{created_time.hour:02d}/{created_time.minute:02d}/{created_time.second:02d}.json"
        container_client = ContainerClient.from_connection_string(
            conn_str=f"DefaultEndpointsProtocol=https;AccountName={storage_account_name};AccountKey={storage_account_key};EndpointSuffix=core.windows.net",
            container_name=container_name
        )
        logging.warning('\tModified...')
        logging.warning('!!!!!!!!!!!!!!!!!!!!!!!')
        async with container_client:
            blob_client = container_client.get_blob_client(blob=blob_path)

            async with blob_client:
                await blob_client.upload_blob(json.dumps(data), overwrite=True)
        logging.warning(f'Successfully saved to Data Lake: {blob_path}')
    except Exception as e:
        logging.error(f'Error saving to Data Lake: {e}')


async def on_event(partition_context, event):
    try:
        data = json.loads(event.body_as_str(encoding="UTF-8"))
        created_utc = datetime.datetime.utcfromtimestamp(data.get("created_utc"))
        # Save data to Data Lake
        await save_to_data_lake(data, created_utc)
    except Exception as e:
        logging.error(f'Error processing event: {e}')

    # logging.warning(f'Received event: "{data}" from partition with ID: "{partition_context.partition_id}"')


async def main():
    consumer_client = EventHubConsumerClient.from_connection_string(
        eventhub_connection_str,
        consumer_group="$Default",
        eventhub_name=eventhub_name
    )
    logging.warning('\tModified...')
    logging.warning('!!!!!!!!!!!!!!!!!!!!!!!')
    async with consumer_client:
        # -1 = read from beginning
        await consumer_client.receive(on_event=on_event, starting_position="-1")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
