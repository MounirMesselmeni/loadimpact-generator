from __future__ import unicode_literals

import urllib
import random

from jinja2 import Environment, PackageLoader
ENV = Environment(loader=PackageLoader('generator', 'templates'))

import getpass
import loadimpact

from parsers.jmeter_parser import JMeterParser


class LoadImpactGenerator(object):

    """Load Impact Generator Class"""

    def __init__(self):
        """Getting user API TOKEN and initializing loadimpact client"""
        super(LoadImpactGenerator, self).__init__()
        self.api_token = getpass.getpass('Your API TOKEN:')
        self.client = loadimpact.ApiTokenClient(api_token=self.api_token)
        self.rand = random.randint(0, 5050000)

    def generate_scenario(self):
        """Generating lua user scenario using jinga2 template"""
        print("Generating scenario")
        #Construction of urls and using urlencode for arguments creation
        for url in self.data['urls']:
            if len(url['arguments']):
                args = urllib.urlencode(url['arguments'])
                url['url'] = "{0}://{1}{2}?{3}".format(url['protocol'], self.data['domain'],
                                                       url['path'], args)
            else:
                url['url'] = "{0}://{1}{2}".format(url['protocol'], self.data['domain'],
                                                   url['path'])
        template = ENV.get_template('lua.tpl')
        kwargs = {
            'tests': self.data['urls'],
            'num_threads': self.data['num_threads'],
        }
        user_scenario = template.render(**kwargs)
        print("Scenario generated \n{0}".format(user_scenario))
        return user_scenario

    def upload_scenario(self):
        print("Uploading scenario")
        load_script = self.generate_scenario()
        user_scenario = self.client.create_user_scenario({
            'name': "{0} scenario {1}".format(self.data['testname'], self.rand),
            'load_script': load_script
        })
        self.scenario_id = user_scenario.id
        print("Scenario uploaded")
        return user_scenario

    def validate_scenario(self):
        user_scenario = self.client.get_user_scenario(self.scenario_id)
        validation = user_scenario.validate()
        stream = validation.result_stream()
        print("Starting validation #%d..." % (validation.id,))
        for result in stream:
            if 'stack_trace' in result:
                print('[%s]: %s @ line %s'
                      % (result['timestamp'], result['message'],
                         result['line_number']))
                print('Stack trace:')
                for filename, line, function in result['stack_trace']:
                    print('\t%s:%s in %s' % (function, line, filename))
            else:
                print('[%s]: %s' % (result['timestamp'], result['message']))
        print("Validation completed with status '%s'"
              % (loadimpact.UserScenarioValidation.status_code_to_text(validation.status)))

    def configure_test(self):
        print("Creating test config")
        config = {
            'name': 'My {0} configuration {1}'.format(self.data['testname'], self.rand),
            'url': 'http://{0}'.format(self.data['domain']),
            'config': {
                "load_schedule": [{"users": self.data['num_threads'], "duration": 5}],
                "tracks": [{
                    "clips": [{
                        "user_scenario_id": self.scenario_id, "percent": 100
                    }],
                    "loadzone": loadimpact.LoadZone.AMAZON_US_ASHBURN
                }],
                "user_type": "sbu"
            }
        }
        self.test_config = self.client.create_test_config(config)
        print("Test config created")

    def run_tests(self):
        print("Running tests")
        test = self.test_config.start_test()
        print("Test runned: test ID {0}".format(test))

    def execute(self):
        """Executing the whole process using the instance methods"""
        parser = JMeterParser()
        self.data = parser.get_data()
        self.upload_scenario()
        self.validate_scenario()
        self.configure_test()
        self.run_tests()
