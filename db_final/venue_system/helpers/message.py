import json


class Message():
    def __init__(self):
        self.response = {}
        self.response["msg"] = {}
        self.response["err"] = {}

    def add_error(self, err):
        self.response["err"] = {
            "err_type": err.type,
            "err_msg": err.message
        }
    def add_payload(self, message, payload):
        self.response["msg"] = {
            "message": message,
            "payload": payload
        }