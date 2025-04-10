import unittest
import logging
import datetime
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'source')))


class TestLogs(unittest.TestCase):
    def setUp(self):
        """
        This method is called before each test. It sets up the logging configuration.
        It creates a directory for logs if it doesn't exist and configures the logger to write logs to a file.
        """

        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        log_path=os.path.join(
                log_dir,
                f"LamboCar_{datetime.datetime.now().date()}.log"
                )

        logging.basicConfig(
            filename=log_path,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO,
            filemode='a',
        )

        self.logger = logging.getLogger(__name__)


    def test_name_logging(self):
        self.assertEqual(self.logger.name, __name__)
    

    def test_info_logging(self):
        """
        This test checks if the logger correctly logs an info message.
        It uses the assertLogs context manager to capture log messages and verifies the output.
        """
        with self.assertLogs('test', level='INFO') as cm:
            logging.getLogger('test').info('first message')
        self.assertEqual(cm.output, ['INFO:test:first message'])
        

    def test_warning_logging(self):
        """
        This test checks if the logger correctly logs an warning message.
        It uses the assertLogs context manager to capture log messages and verifies the output.
        """
        with self.assertLogs('test', level='WARNING') as cm:
            logging.getLogger('test').warning('first message')
        self.assertEqual(cm.output, ['WARNING:test:first message'])

    def test_error_logging(self):
        """
        This test checks if the logger correctly logs an error message.
        It uses the assertLogs context manager to capture log messages and verifies the output.
        """

        with self.assertLogs('test', level='ERROR') as cm:
            logging.getLogger('test').error('first message')
        self.assertEqual(cm.output, ['ERROR:test:first message'])
    

    def test_in_file_content(self):
        """
        This test checks if the log file contains a specific log message.
        It reads the log file and verifies that the expected message is present.
        """
        try:
            log_path = os.path.join(
                "logs",
                f"LamboCar_{datetime.datetime.now().date()}.log"
            )

            self.logger.info("Add log to check the log file.")

            with open(log_path, "r") as file:
                content = file.read()
                self.assertIn("Add log to check the log file.", content)

        except FileNotFoundError:
            self.fail(f"Log file {log_path} not found.")
    

if __name__ == "__main__":
    unittest.main()
        