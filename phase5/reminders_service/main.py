from confluent_kafka import Consumer, KafkaException, KafkaError
import json
import os
import sys
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from abc import ABC, abstractmethod

# Kafka Configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9093")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "todo-events")
KAFKA_GROUP_ID = os.getenv("KAFKA_GROUP_ID", "reminders-service-group")

# Notification Configuration
NOTIFICATION_METHOD = os.getenv("NOTIFICATION_METHOD", "console")

# SMTP Configuration
SMTP_HOST = os.getenv("SMTP_HOST", "localhost")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SMTP_FROM = os.getenv("SMTP_FROM", "reminders@todo-app.local")

# Webhook Configuration
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")


class NotificationSender(ABC):
    """Abstract base class for notification senders."""

    @abstractmethod
    def send(self, subject: str, message: str, user_id: str, todo_data: dict) -> bool:
        """Send a notification. Returns True on success, False on failure."""
        pass


class ConsoleNotificationSender(NotificationSender):
    """Sends notifications to the console (stdout)."""

    def send(self, subject: str, message: str, user_id: str, todo_data: dict) -> bool:
        print(f"[NOTIFICATION] {subject}")
        print(f"  User: {user_id}")
        print(f"  Message: {message}")
        return True


class EmailNotificationSender(NotificationSender):
    """Sends notifications via email using SMTP."""

    def __init__(self, host: str, port: int, user: str, password: str, from_addr: str):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.from_addr = from_addr

    def send(self, subject: str, message: str, user_id: str, todo_data: dict) -> bool:
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.from_addr
            # In a real application, you would look up the user's email from a database
            # For now, we use a placeholder that would need to be resolved
            to_addr = todo_data.get("user_email", f"{user_id}@todo-app.local")
            msg['To'] = to_addr
            msg['Subject'] = subject

            # Create HTML body
            html_body = f"""
            <html>
            <body>
                <h2>{subject}</h2>
                <p>{message}</p>
                <hr>
                <p><strong>Task Details:</strong></p>
                <ul>
                    <li><strong>Title:</strong> {todo_data.get('title', 'N/A')}</li>
                    <li><strong>Description:</strong> {todo_data.get('description', 'N/A')}</li>
                    <li><strong>Due Date:</strong> {todo_data.get('due_date', 'N/A')}</li>
                </ul>
            </body>
            </html>
            """
            msg.attach(MIMEText(html_body, 'html'))

            # Send email
            with smtplib.SMTP(self.host, self.port) as server:
                server.starttls()
                if self.user and self.password:
                    server.login(self.user, self.password)
                server.sendmail(self.from_addr, to_addr, msg.as_string())

            print(f"[EMAIL] Sent notification to {to_addr}: {subject}")
            return True

        except Exception as e:
            print(f"[EMAIL ERROR] Failed to send email: {e}")
            return False


class WebhookNotificationSender(NotificationSender):
    """Sends notifications via HTTP POST to a webhook URL."""

    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def send(self, subject: str, message: str, user_id: str, todo_data: dict) -> bool:
        if not self.webhook_url:
            print("[WEBHOOK ERROR] No webhook URL configured")
            return False

        try:
            payload = {
                "subject": subject,
                "message": message,
                "user_id": user_id,
                "todo_data": todo_data,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }

            response = requests.post(
                self.webhook_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            response.raise_for_status()

            print(f"[WEBHOOK] Sent notification to {self.webhook_url}: {subject}")
            return True

        except requests.exceptions.RequestException as e:
            print(f"[WEBHOOK ERROR] Failed to send webhook: {e}")
            return False


def get_notification_sender() -> NotificationSender:
    """Factory function to create the appropriate notification sender."""
    method = NOTIFICATION_METHOD.lower()

    if method == "email":
        print(f"[*] Using EMAIL notifications (SMTP: {SMTP_HOST}:{SMTP_PORT})")
        return EmailNotificationSender(
            host=SMTP_HOST,
            port=SMTP_PORT,
            user=SMTP_USER,
            password=SMTP_PASSWORD,
            from_addr=SMTP_FROM
        )
    elif method == "webhook":
        print(f"[*] Using WEBHOOK notifications (URL: {WEBHOOK_URL})")
        return WebhookNotificationSender(webhook_url=WEBHOOK_URL)
    else:
        if method != "console":
            print(f"[!] Unknown notification method '{method}', falling back to console")
        print("[*] Using CONSOLE notifications")
        return ConsoleNotificationSender()


def send_reminder(sender: NotificationSender, reminder_type: str, todo_data: dict):
    """Send a reminder notification using the configured sender."""
    title = todo_data.get('title', 'Untitled Task')
    user_id = todo_data.get('user_id', 'unknown')
    due_date = todo_data.get('due_date', 'N/A')

    if reminder_type == "due_soon":
        subject = f"Reminder: Task '{title}' is due soon"
        message = f"Your task '{title}' is due on {due_date}. Don't forget to complete it!"
    elif reminder_type == "overdue":
        subject = f"Overdue: Task '{title}' is past due"
        message = f"Your task '{title}' was due on {due_date}. Please complete it as soon as possible."
    else:
        subject = f"Task Update: {title}"
        message = f"There's an update regarding your task '{title}'."

    success = sender.send(subject, message, user_id, todo_data)

    if not success:
        # Fallback to console if the primary method fails
        print(f"[FALLBACK] Primary notification failed, logging to console:")
        ConsoleNotificationSender().send(subject, message, user_id, todo_data)


def consume_events():
    conf = {
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'group.id': KAFKA_GROUP_ID,
        'auto.offset.reset': 'earliest'
    }

    consumer = Consumer(conf)
    notification_sender = get_notification_sender()

    try:
        consumer.subscribe([KAFKA_TOPIC])

        print(f"[*] Reminders Service started. Listening on topic '{KAFKA_TOPIC}'...")

        while True:
            msg = consumer.poll(timeout=1.0)  # Poll for messages, 1-second timeout

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
                            now = datetime.utcnow().replace(tzinfo=due_date.tzinfo)

                            # Check if due date is within the next 24 hours
                            if now < due_date and (due_date - now) < timedelta(days=1):
                                send_reminder(notification_sender, "due_soon", todo_data)
                            elif now >= due_date:
                                send_reminder(notification_sender, "overdue", todo_data)

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
