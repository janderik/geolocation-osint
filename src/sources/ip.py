"""IP geolocation source."""

import requests
from typing import Dict, Any, Optional


class IPSource:
    """IP-based geolocation source."""
    
    def __init__(self):
        """Initialize the IP source."""
        self.session = requests.Session()
    
    def lookup(self, ip: str) -> Dict[str, Any]:
        """Look up geolocation for an IP address."""
        try:
            response = self.session.get(
                f"http://ip-api.com/json/{ip}",
                timeout=10
            )
            return response.json()
        except Exception as e:
            return {'error': str(e)}
