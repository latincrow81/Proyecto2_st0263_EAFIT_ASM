import json
from unittest import TestCase

from app.controllers import create_queue, push_message_to_queue, pop_message_from_queue


class TestControllerMom(TestCase):
    def setUp(self):
        self.queue_name = "test_queue"

    def test_create_queue(self):
        # when
        queue = create_queue(self.queue_name)
        # then
        self.assertTrue(True)
        self.assertEqual(queue.shm.name, self.queue_name)

    def test_push_message_to_queue(self):
        # given
        message_payload = {
            'key1': 'value 1',
            'key2': 'value 2',
            'key3': 'value 3'
        }
        # when
        create_queue(self.queue_name)
        shared_list = push_message_to_queue(self.queue_name, message_payload)

        # then
        self.assertTrue(True)
        self.assertTrue(shared_list[0], json.dumps(message_payload))

    def test_pop_message_from_queue(self):
        # given
        message_payload = {
            'key1': 'value 1',
            'key2': 'value 2',
            'key3': 'value 3'
        }

        # when
        create_queue(self.queue_name)
        push_message_to_queue(self.queue_name, message_payload)
        message = pop_message_from_queue(self.queue_name)

        # then
        self.assertEqual(message, json.dumps(message_payload))