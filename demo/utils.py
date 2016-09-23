from google.cloud import pubsub


class PubSubClient:

    def __init__(self):
        self.client = pubsub.Client()

    def push(self, data):
        topic = self.client.list_topics()[0][0]
        topic.publish(data.encode('utf-8'))

    def pull(self):
        subscription = self.client.list_subscriptions()[0][0]
        ack_id, msg = subscription.pull(1)[0]
        subscription.acknowledge([ack_id])

        return msg.data.decode('utf-8')
