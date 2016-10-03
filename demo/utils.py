import logging

from django.http import Http404
from google.cloud import pubsub

logger = logging.getLogger('django')

PROJECT_IDENTIFIER = 'medxm'


class PubSubClient:

    def __init__(self):
        self.client = pubsub.Client()

    def push(self, mailing_id, name, **kwargs):
        topic = self.client.topic('{}-{}'.format(PROJECT_IDENTIFIER, mailing_id))
        if not topic.exists():
            topic.create()
            subscription = topic.subscription('{}-{}'.format(PROJECT_IDENTIFIER, mailing_id))
            subscription.create()

        attributes = {}
        for key, value in kwargs.items():
            attributes[key] = str(value)

        logger.info('Pushing data to PubSub...')
        logger.info('  mailing_id: {}'.format(mailing_id))
        logger.info('  name: {}'.format(name))
        for key, value in attributes.items():
            logger.info('  {}: {}'.format(key, value))

        topic.publish(name.encode('utf-8'), **attributes)

    def pull(self, topic_name):
        topic_identifier = '{}-{}'.format(PROJECT_IDENTIFIER, topic_name)
        subscription = self.client.topic(topic_identifier).subscription(topic_identifier)
        try:
            ack_id, msg = subscription.pull(1)[0]
        except IndexError:
            raise Http404
        subscription.acknowledge([ack_id])

        data = {
            'mailing_id': topic_name,
            'name': msg.data.decode('utf-8'),
        }

        for key, value in msg.attributes.items():
            data[key] = value

        logger.info('Pulled data from PubSub...')
        for key, value in data.items():
            logger.info('  {}: {}'.format(key, value))

        return data
