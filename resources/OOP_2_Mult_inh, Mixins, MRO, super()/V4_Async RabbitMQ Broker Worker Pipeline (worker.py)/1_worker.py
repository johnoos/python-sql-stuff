import asyncio
import json
import aio_pika
from app_pipeline import NextGenComputeCore

# Configuration parameters for the microservice connection
RABBITMQ_URL = "amqp://guest:guest@localhost:5672/"
QUEUE_NAME = "packet_ingestion_queue"


async def process_message(message: aio_pika.abc.AbstractIncomingMessage, node: NextGenComputeCore):
    """
    Callback function that processes a single incoming message stream.
    Uses context management to guarantee message acknowledgment or rejection.
    """
    async with message.process():
        try:
            # 1. Decode byte payload from the network queue
            payload_str = message.body.decode()
            print(f"\n[Worker] Received message from queue broker: {payload_str}")
            
            # 2. Process payload using our optimized slotted architecture
            pipeline_result = await node.ingest_packet_async(payload_str)
            print(f"[Worker] Pipeline Execution Metrics: {pipeline_result}")
            
        except Exception as e:
            print(f"[Worker Error] Failed to route cluster workload: {e}")
            # If an error happens, the message context safely rejects it back to RabbitMQ


async def run_worker_pipeline():
    """Sets up the asynchronous RabbitMQ connection listener loop."""
    print("[Pipeline Engine] Connecting to RabbitMQ async broker network...")
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    
    # Initialize the processing compute core node instance
    compute_node = NextGenComputeCore(node_id="Worker-Core-Node", hardware_cost=12000.00, region="eu-west-1")
    
    async with connection:
        # Open an asynchronous communication channel
        channel = await connection.channel()
        
        # Optimize performance: limit the number of unacknowledged messages the worker can hold
        await channel.set_qos(prefetch_count=10)
        
        # Declare the queue (creates it if it doesn't exist yet)
        queue = await channel.declare_queue(QUEUE_NAME, durable=True)
        
        print(f"[Pipeline Engine] Active. Listening for tasks on stream queue: '{QUEUE_NAME}'...")
        
        # Begin consuming messages asynchronously, routing them to our callback function
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                # Process messages concurrently as they arrive on the loop
                asyncio.create_task(process_message(message, compute_node))


if __name__ == "__main__":
    try:
        asyncio.run(run_worker_pipeline())
    except KeyboardInterrupt:
        print("\n[Pipeline Engine] Shutting down connection layers gracefully.")
