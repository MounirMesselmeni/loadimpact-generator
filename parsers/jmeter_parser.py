from __future__ import unicode_literals

from lxml import etree

ARG_SELECTOR = str(".//elementProp[@name='HTTPsampler.Arguments']//"
                   "elementProp[@elementType='HTTPArgument']")


class JMeterParser(object):

    """Apache JMeter jmx Parser"""
    def __init__(self, file_path):
        super(JMeterParser, self).__init__()
        self.file = open(file_path)

    def initialize_etree(self):
        self.etree = etree.fromstring(self.file.read())
        self.file.close()

    def get_data(self):
        self.initialize_etree()
        return dict(
            testname=self.parse_testname(),
            num_threads=self.parse_num_threads(),
            ramp_time=self.parse_ramp_time(),
            domain=self.parse_domain(),
            concurrent_pool=self.parse_concurrent_pool(),
            urls=self.parse_entries(),
        )

    def parse_testname(self):
        test_plan = self.etree.find('.//TestPlan')
        if test_plan is not None and 'testname' in test_plan.attrib:
            return test_plan.attrib['testname']
        raise Exception("Mal formatted data")

    def parse_num_threads(self):
        num_threads = self.etree.find(".//stringProp[@name='ThreadGroup.num_threads']")
        if num_threads is not None:
            return num_threads.text
        raise Exception("Mal formatted data")

    def parse_ramp_time(self):
        ramp_time = self.etree.find(".//stringProp[@name='ThreadGroup.ramp_time']")
        if ramp_time is not None:
            return ramp_time.text
        raise Exception("Mal formatted data")

    def parse_domain(self):
        domain = self.etree.find(".//ConfigTestElement//stringProp[@name='HTTPSampler.domain']")
        if domain is not None:
            return domain.text
        raise Exception("Mal formatted data")

    def parse_concurrent_pool(self):
        concurrent_pool = self.etree.find(".//ConfigTestElement//stringProp[@name='HTTPSampler.concurrentPool']")
        if concurrent_pool is not None:
            return concurrent_pool.text
        raise Exception("Mal formatted data")

    def parse_entries(self):
        entries_trees = self.etree.findall(".//HTTPSamplerProxy")
        entries = list()
        for entry in entries_trees:
            entries.append(self.parse_entry(entry))
        return entries

    def parse_entry(self, entry):
        return dict(
            path=self.parse_entry_path(entry),
            method=self.parse_entry_method(entry),
            follow_redirects=self.parse_entry_follow_redirects(entry),
            auto_redirects=self.parse_entry_auto_redirects(entry),
            use_keepalive=self.parse_entry_use_keepalive(entry),
            do_multipart_post=self.parse_entry_do_multipart_post(entry),
            implementation=self.parse_entry_implementation(entry),
            monitor=self.parse_entry_monitor(entry),
            protocol=self.parse_entry_protocol(entry),
            arguments=self.parse_entry_arguments(entry),
        )

    def parse_entry_path(self, entry):
        path = entry.find(".//stringProp[@name='HTTPSampler.path']")
        if path is not None:
            return path.text
        raise Exception("Mal formatted data")

    def parse_entry_method(self, entry):
        method = entry.find(".//stringProp[@name='HTTPSampler.method']")
        if method is not None:
            return method.text
        raise Exception("Mal formatted data")

    def parse_entry_follow_redirects(self, entry):
        follow_redirects = entry.find(".//boolProp[@name='HTTPSampler.follow_redirects']")
        if follow_redirects is not None:
            return follow_redirects.text == "true"
        raise Exception("Mal formatted data")

    def parse_entry_auto_redirects(self, entry):
        auto_redirects = entry.find(".//boolProp[@name='HTTPSampler.auto_redirects']")
        if auto_redirects is not None:
            return auto_redirects.text == "true"
        raise Exception("Mal formatted data")

    def parse_entry_use_keepalive(self, entry):
        use_keepalive = entry.find(".//boolProp[@name='HTTPSampler.use_keepalive']")
        if use_keepalive is not None:
            return use_keepalive.text == "true"
        raise Exception("Mal formatted data")

    def parse_entry_do_multipart_post(self, entry):
        do_multipart_post = entry.find(".//boolProp[@name='HTTPSampler.DO_MULTIPART_POST']")
        if do_multipart_post is not None:
            return do_multipart_post.text == "true"
        raise Exception("Mal formatted data")

    def parse_entry_implementation(self, entry):
        implementation = entry.find(".//stringProp[@name='HTTPSampler.implementation']")
        if implementation is not None:
            return implementation.text
        raise Exception("Mal formatted data")

    def parse_entry_monitor(self, entry):
        monitor = entry.find(".//boolProp[@name='HTTPSampler.monitor']")
        if monitor is not None:
            return monitor.text == "true"
        raise Exception("Mal formatted data")

    def parse_entry_protocol(self, entry):
        protocol = entry.find(".//stringProp[@name='HTTPSampler.protocol']")
        if protocol is not None:
            return protocol.text
        raise Exception("Mal formatted data")

    def parse_entry_arguments(self, entry):
        arguments = entry.findall(ARG_SELECTOR)
        if not len(arguments):
            return []
        arguments_dict = dict()
        for arg in arguments:
            name = arg.find(".//stringProp[@name='Argument.name']").text
            value = arg.find(".//stringProp[@name='Argument.value']").text
            arguments_dict.update({name: value})
        return arguments_dict
