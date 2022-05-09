import os

from google.cloud import pubsub
from google.pubsub import PullResponse, ReceivedMessage
from google.cloud.pubsub import SubscriberClient, PublisherClient
from typing import Optional

from service.queue.i_queue import IQueue
from util.i_logger import ILogger


class GCPQueue(IQueue):
    """Google Cloud queue service implementation."""
    def __init__(self, logger: ILogger):
        self.logger: ILogger = logger

        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'gcp_queue_key.json'
        self.pub_sub_topic: str = 'bouken-ci'
        self.pub_sub_project: str = 'stoked-archway-349702'
        self.pub_sub_subscription: str = 'bouken-ci-sub'

        self.publisher_client: PublisherClient = pubsub.PublisherClient()
        self.publish_path: str = self.publisher_client.topic_path(
            self.pub_sub_project, self.pub_sub_topic)

        self.subscriber_client: SubscriberClient = pubsub.SubscriberClient()
        self.subscribe_path: str = self.subscriber_client.topic_path(
            self.pub_sub_project, self.pub_sub_subscription)

    def get_message(self) -> Optional[str]:
        content: Optional[str] = None

        try:
            res: PullResponse = self.subscriber_client.pull(
                subscription=self.subscribe_path, max_messages=1)
            if not res:
                return None

            msg: ReceivedMessage = res[0]
            content = str(msg.data)
            msg.ack()
        except Exception as ex:
            self.logger.error(f'Exception while pulling from queue', ex)

        return content

    def push_message(self, payload: str) -> None:
        try:
            data = payload.encode('utf-8')
            self.publisher_client.publish(self.publish_path, data)
        except Exception as ex:
            self.logger.error(f'Exception while pushing item to queue, payload: {payload}', ex)
