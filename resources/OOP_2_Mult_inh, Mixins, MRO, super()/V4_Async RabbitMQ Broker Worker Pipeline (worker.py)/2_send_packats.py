import asyncio
import aio_pika
async def publish_test_packets():
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost:5672/")
    async with connection:
        channel = await connection.channel()
        
        test_payloads = [
            "ValidSystemDataPacketAlpha",
            "Short",  # Will fail validation
            "ValidSystemDataPacketBeta"
        ]
        
        print("[Producer] Dispatching messages to RabbitMQ cluster...")
        for payload in test_payloads:
            await channel.default_exchange.publish(
                aio_pika.Message(body=payload.encode()),
                routing_key="packet_ingestion_queue"
            )
            print(f"  Sent: {payload}")

if __name__ == "__main__":
    asyncio.run(publish_test_packets())
