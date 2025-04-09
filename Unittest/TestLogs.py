import unittest
import logging
import datetime
import os


class TestLogs(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            )
        self.logger = logging.getLogger(__name__)


    def test_name_logging(self):
        self.assertEqual(self.logger.name, __name__)
    

    def test_info_logging(self):
        with self.assertLogs('test', level='INFO') as cm:
            logging.getLogger('test').info('first message')
        self.assertEqual(cm.output, ['INFO:test:first message'])
        

    def test_warning_logging(self):
        with self.assertLogs('test', level='WARNING') as cm:
            logging.getLogger('test').warning('first message')
        self.assertEqual(cm.output, ['WARNING:test:first message'])

    def test_error_logging(self):
        with self.assertLogs('test', level='ERROR') as cm:
            logging.getLogger('test').error('first message')
        self.assertEqual(cm.output, ['ERROR:test:first message'])
    

    def test_file_content(self):
        log_path = os.path.join(
            "logs",
            f"LamboCar_{datetime.datetime.now().date()}.log"
        )
        
        with open(log_path, "r") as file:
            content = file.read()
            self.assertIn(str(datetime.datetime.now().date()), content)
    

if __name__ == "__main__":
    unittest.main()
        