from django.core.management import BaseCommand
from kombu import Exchange, Queue

from core.rabbitmq import create_rabbitmq_connection
from core.services import create_video_service_factory


class Command(BaseCommand):
  help = 'Upload chunks to external storage'

  def handle(self, *args, **options):
    self.stdout.write(self.style.SUCCESS('Starting consumer...'))
    exchange = Exchange('conversion_exchange', type='direct', auto_delete=True)
    queue = Queue('chunks', exchange, routing_key='chunks')

    with create_rabbitmq_connection() as connection:
      with connection.Consumer(queue, callbacks=[self.process_message]):
        while True:
          self.stdout.write(self.style.SUCCESS('Waiting for messages...'))
          connection.drain_events()
  
  def process_message(self, body, message):
    self.stdout.write(self.style.SUCCESS(f'Processing message: {body}'))
    create_video_service_factory().upload_chunks_to_external_storage(body['video_id'])
    message.ack()