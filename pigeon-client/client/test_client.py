import os
import unittest
import tempfile
from networking import server_messages


class TestClient(unittest.TestCase):
    valid_id = "592b02cf-f520-44d5-9898-2c0dedd32980"
    invalid_id = "Hello" 

    valid_json = {
    "meta": {
        "to": "11111111-1111-1111-1111-111111111111",
        "from": "11111111-1111-1111-1111-111111111112",
        "datetime": "1985-04-12T23:20:50.52Z"
    },
    "message": "i do believe"
    }

    invalid_json = {
        "to": "11111111-1111-1111-1111-111111111111",
        "from": "11111111-1111-1111-1111-111111111112",
        "datetime": "1985-04-12T23:20:50.52Z",
        "message": "i do believe"
    }

    def test_valid_uid(self):
        self.assertEquals(server_messages.send_message(self.valid_json, self.valid_id), 0)

    def test_invalid_uid(self):
        self.assertEquals(server_messages.send_message(self.valid_json, self.invalid_id), 1)

    def test_valid_json(self):
        self.assertEquals(server_messages.send_message(self.valid_json, self.valid_id), 0)

    def test_invalid_json(self):
        self.assertEquals(server_messages.send_message(self.invalid_json, self.valid_id), 1)
        
if __name__ == '__main__':
    unittest.main()
