import unittest
from unittest.mock import patch
from DistanceSensor import DistanceSensor

class TestDistanceSensor(unittest.TestCase):

    def setUp(self):
        self.pinTrig = 6
        self.pinEcho = 5
        self.side = "Front"
        self.sensor = DistanceSensor(self.pinTrig, self.pinEcho, self.side)

    @patch("DistanceSensor.GPIO")
    @patch("DistanceSensor.time")
    def test_readValue_valid(self, mock_time, mock_gpio):

        """
        Normal read:
        We simulate a valid echo signal with a duration of 0.0012 seconds and we calculate the distance
        using the formula: distance = duration * 17150 (in cm).
        The expected distance is 20.57 cm (0.0012 * 17150)
        """

        mock_gpio.input.side_effect = [0, 1, 1, 0]   
        mock_time.time.side_effect = [
            1.0,      
            1.0001,  
            1.0001,   
            1.0013    
        ]

        distance = self.sensor.readValue()
        expected_distance = round((1.0013 - 1.0001) * 17150, 2)  
        self.assertAlmostEqual(distance, expected_distance, places=2)


    @patch("DistanceSensor.GPIO")
    @patch("DistanceSensor.time")
    def test_readValue_timeout(self, mock_time, mock_gpio):

        mock_gpio.input.return_value = 0
        mock_time.time.side_effect = [0.0, 0.06]

        distance = self.sensor.readValue()
        self.assertIsNone(distance)


    @patch("DistanceSensor.GPIO")
    @patch("DistanceSensor.time")
    def test_readValue_timeout_end(self, mock_time, mock_gpio):
            
        """
        We simulate a signal that is too long between the detection of High and his start to be valid (> 0.05 seconds)
        the signal never goes DOWN and then the GPIO stays HIGH until we got out of time
        """
            
        mock_gpio.input.side_effect = [1, 1, 1, 1]
        mock_time.time.side_effect = [
            1.0, 
            1.0, 
            1.06, 
            1.07
        ]

        distance = self.sensor.readValue()
        self.assertIsNone(distance)
    

    @patch("DistanceSensor.GPIO")
    @patch("DistanceSensor.time")
    def test_invalid_duration(self, mock_time, mock_gpio):

        """
        We simulate a signal that is too short to be valid
        There is no time to calculate the distance, so we return None
        """
        
        mock_gpio.input.side_effect = [1,0]
        mock_time.time.side_effect = [1.0, 1.0]

        result = self.sensor.readValue()
        self.assertIsNone(result)
    

    @patch("DistanceSensor.GPIO")
    @patch("DistanceSensor.time")
    def test_distance_out_of_range_low(self, mock_time, mock_gpio):

        """
        We simulate a signal that is too short to be valid (< 2 cm)
        We expect the distance to be None because the distance is out of range < 2cms
        """

        mock_gpio.input.side_effect = [0, 1, 1, 0]   
        mock_time.time.side_effect = [
            1.0,      
            1.0001,   
            1.0001,   
            1.00015   
        ]

        distance = self.sensor.readValue()
        self.assertIsNotNone(distance)
    


    @patch("DistanceSensor.GPIO")
    @patch("DistanceSensor.time")
    def test_distance_out_of_range_high(self, mock_time, mock_gpio):

        """
        We simulate a signal that is too short to be valid (> 400 cms)
        We expect the distance to be None because the distance is out of range > 400cms
        """

        mock_gpio.input.side_effect = [0, 1, 1, 0]   
        mock_time.time.side_effect = [
            1.0,      
            1.0001,   
            1.0001,   
            1.03  
        ]

        distance = self.sensor.readValue()
        self.assertIsNotNone(distance)


if __name__ == "__main__":
    unittest.main()