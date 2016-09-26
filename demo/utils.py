import logging

from google.cloud import pubsub

logger = logging.getLogger(__name__)


class PubSubClient:

    def __init__(self):
        self.client = pubsub.Client()

    def push(self, data):
        logger.debug('Pushing data: {}'.format(data))
        topic = self.client.list_topics()[0][0]
        topic.publish(data.encode('utf-8'))

    def pull(self):
        subscription = self.client.list_subscriptions()[0][0]
        ack_id, msg = subscription.pull(1)[0]
        subscription.acknowledge([ack_id])

        data = msg.data.decode('utf-8')
        logger.debug('Pulled data: {}'.format(data))

        return data
