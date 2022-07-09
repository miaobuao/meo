"""
for spider
"""
from enum import Enum

class UserAgent(Enum):

    """UA in different platform"""

    FIREFOX = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"

    SAFARI_IPHONE = "Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) " \
                    "AppleWebKit/605.1.15 (KHTML, like Gecko) " \
                    "Version/15.4 Mobile/15E148 Safari/604.1"

    SAFARI_IPAD = "Mozilla/5.0 (iPad; CPU OS 15_5 like Mac OS X) " \
                    "AppleWebKit/605.1.15 (KHTML, like Gecko) " \
                    "Version/15.4 Mobile/15E148 Safari/604.1"

    SAFARI_IPOD = "Mozilla/5.0 (iPod touch; CPU iPhone 15_5 like Mac OS X) " \
                    "AppleWebKit/605.1.15 (KHTML, like Gecko) " \
                    "Version/15.4 Mobile/15E148 Safari/604.1"
