# -*- test-case-name: vumi.scripts.tests.test_model_migrator -*-
import sys

from twisted.python import usage

from vumi.utils import load_class_by_string
from vumi.persist.riak_manager import RiakManager


class Options(usage.Options):
    optParameters = [
        ["model", "m", None,
         "Full Python name of the model class to migrate."
         " E.g. 'vumi.components.message_store.InboundMessage'."],
        ["bucket-prefix", "b", None,
         "The bucket prefix for the Riak manager."],
    ]

    longdesc = """Offline model migrator. Necessary for updating
                  models when index names change so that old model
                  instances remain findable by index searches.
                  """

    def postOptions(self):
        if self.options['model'] is None:
            raise usage.UsageError("Please specify a model class.")
        if self.options['bucket_prefix'] is None:
            raise usage.UsageError("Please specify a bucket prefix.")


class ConfigHolder(object):
    def __init__(self, options):
        self.options = options
        model_cls = load_class_by_string(options['model'])
        riak_config = {
            'bucket_prefix': options['bucket-prefix'],
        }
        manager = RiakManager.from_config(riak_config)
        self.model = manager.proxy(model_cls)

    def emit(self, s):
        print s

    def run(self):
        for key in self.model.all_keys():
            obj = self.model.load(key)
            if obj is not None:
                obj.save()


if __name__ == '__main__':
    try:
        options = Options()
        options.parseOptions()
    except usage.UsageError, errortext:
        print '%s: %s' % (sys.argv[0], errortext)
        print '%s: Try --help for usage details.' % (sys.argv[0])
        sys.exit(1)

    cfg = ConfigHolder(options)
    cfg.run()
