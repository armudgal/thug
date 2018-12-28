import os
import logging

from thug.ThugAPI.ThugAPI import ThugAPI

log = logging.getLogger("Thug")


class TestClassifiers(object):
    thug_path        = os.path.dirname(os.path.realpath(__file__)).split("thug")[0]
    classifiers_path = os.path.join(thug_path, "thug", "samples/classifiers")
    signatures_path  = os.path.join(thug_path, "thug", "tests/signatures")

    def do_perform_test(self, caplog, sample, expected):
        thug = ThugAPI()

        thug.set_useragent('winxpie70')
        thug.disable_cert_logging()

        thug.log_init(sample)

        thug.add_htmlclassifier(os.path.join(self.signatures_path, "html_signature_1.yar"))
        thug.add_jsclassifier(os.path.join(self.signatures_path, "js_signature_2.yar"))
        thug.add_urlclassifier(os.path.join(self.signatures_path, "url_signature_3.yar"))
        thug.add_urlfilter(os.path.join(self.signatures_path, "url_filter_4.yar"))

        thug.run_local(sample)

        records = [r.message for r in caplog.records]

        matches = 0

        for e in expected:
            for record in records:
                if e in record:
                    matches += 1

        assert matches >= len(expected)

    def test_html_classifier_1(self, caplog):
        sample   = os.path.join(self.classifiers_path, "test1.html")
        expected = ['[HTML Classifier]',
                    'thug/samples/classifiers/test1.html (Rule: html_signature_1, Classification: )']

        self.do_perform_test(caplog, sample, expected)

    def test_js_classifier_2(self, caplog):
        sample   = os.path.join(self.classifiers_path, "test2.html")
        expected = ['[JS Classifier]',
                    'thug/samples/classifiers/test2.html (Rule: js_signature_2, Classification: )']

        self.do_perform_test(caplog, sample, expected)

    def test_url_classifier_3(self, caplog):
        sample   = os.path.join(self.classifiers_path, "test3.html")
        expected = ['[URL Classifier] URL: http://www.antifork.org (Rule: url_signature_3, Classification: )']

        self.do_perform_test(caplog, sample, expected)

    def test_url_filter_4(self, caplog):
        sample   = os.path.join(self.classifiers_path, "test4.html")
        expected = ['[URLFILTER Classifier] URL: http://www.google.com (Rule: url_filter_4, Classification: )']

        self.do_perform_test(caplog, sample, expected)