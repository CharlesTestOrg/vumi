from twisted.python import log
import json, datetime

class Message(object):
    """
    Start of a somewhat unified message object to be
    used internally in Vumi and while being in transit
    over AMQP

    scary transport format -> Vumi Tansport -> Unified Message -> Vumi Worker
    
    """

    def __init__(self, **kwargs):
        self.payload = kwargs

    def to_json(self):
        return json.dumps(self.payload, cls=JSONMessageEncoder)
    
    @classmethod
    def from_json(klass, json_string):
        dictionary = json.loads(json_string, object_hook=date_time_decoder)
        return klass(**dictionary)

    def __str__(self):
        return u"<Message payload=\"%s\">" % self.payload

def date_time_decoder(json_object):
    for key,value in json_object.items():
        iso_valid_formats = [
                '%Y-%m-%dT%H:%M:%S.%f',
                '%Y-%m-%dT%H:%M:%S'
                ]
        for format in iso_valid_formats:
            try:
                json_object[key] = datetime.datetime.strptime(value, format)
            except ValueError, e:
                continue
            except TypeError, e:
                continue
    return json_object 


class JSONMessageEncoder(json.JSONEncoder):
    """A JSON encoder that is able to serialize datetime"""
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return super(JSONEncoder, self).default(obj)
    

