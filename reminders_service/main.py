from confluent_kafka import Consumer, KafkaException, KafkaError
import json
import os
import sys
from datetime import datetime, timedelta

# Configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9093")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "todo-events")
KAFKA_GROUP_ID = os.getenv("KAFKA_GROUP_ID", "reminders-service-group")

def consume_events():
    conf = {
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'group.id': KAFKA_GROUP_ID,
        'auto.offset.reset': 'earliest'
    }

    consumer = Consumer(conf)

    try:
        consumer.subscribe([KAFKA_TOPIC])

        print(f"[*] Reminders Service started. Listening on topic '{KAFKA_TOPIC}'...")

        while True:
            msg = consumer.poll(timeout=1.0) # Poll for messages, 1-second timeout 

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event, not an error
                    sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                     (msg.topic(), msg.partition(), msg.offset()))
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                # Process message
                event_data = json.loads(msg.value().decode('utf-8'))
                event_type = event_data.get("event_type")
                todo_data = event_data.get("todo_data")
                
                print(f"Received event: {event_type} for Todo ID: {todo_data['id']} (User: {todo_data['user_id']})")

                if event_type in ["TodoCreated", "TodoUpdated"]:
                    due_date_str = todo_data.get("due_date")
                    completed = todo_data.get("completed", False)

                    if due_date_str and not completed:
                        try:
                            # Assuming due_date_str is in ISO format
                            due_date = datetime.fromisoformat(due_date_str.replace("Z", "+00:00"))
                            now = datetime.utcnow().replace(tzinfo=due_date.tzinfo) # Ensure timezone awareness
                            
                            # Check if due date is within the next 24 hours
                            if now < due_date and (due_date - now) < timedelta(days=1):
                                print(f"[REMINDER] Task '{todo_data['title']}' for user {todo_data['user_id']} is due soon: {due_date.isoformat()}")
                            elif now >= due_date:
                                print(f"[REMINDER] Task '{todo_data['title']}' for user {todo_data['user_id']} is OVERDUE: {due_date.isoformat()}")

                        except ValueError as e:
                            print(f"Error parsing due_date: {e}")
                            
                elif event_type == "TodoDeleted":
                    print(f"[INFO] Task '{todo_data['title']}' for user {todo_data['user_id']} has been deleted.")

    except KeyboardInterrupt:
        pass
    finally:
        # Close down consumer to commit final offsets.
        consumer.close()

if __name__ == "__main__":
    consume_events()
