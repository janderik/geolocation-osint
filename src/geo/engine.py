"""Geolocation intelligence engine."""

import requests
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from pathlib import Path


@dataclass
class GeoResult:
    """Geolocation result."""
    latitude: float
    longitude: float
    accuracy: Optional[float]
    source: str
    metadata: Dict[str, Any]


class GeoEngine:
    """
    Main engine for geolocation intelligence.
    
    Combines multiple sources for location determination.
    """
    
    IP_API_URL = "http://ip-api.com/json/{ip}"
    
    def __init__(self):
        """Initialize the geolocation engine."""
        self.session = requests.Session()
    
    def locate_ip(self, ip_address: str) -> GeoResult:
        """
        Get geolocation from IP address.
        
        Args:
            ip_address: IPv4 or IPv6 address.
            
        Returns:
            GeoResult with location data.
        """
        response = self.session.get(
            self.IP_API_URL.format(ip=ip_address),
            timeout=10
        )
        data = response.json()
        
        if data.get('status') == 'success':
            return GeoResult(
                latitude=data.get('lat', 0),
                longitude=data.get('lon', 0),
                accuracy=1000,  # Approximate accuracy in meters
                source='ip-api',
                metadata={
                    'country': data.get('country'),
                    'city': data.get('city'),
                    'isp': data.get('isp'),
                    'org': data.get('org'),
                }
            )
        
        raise ValueError(f"Could not locate IP: {ip_address}")
    
    def extract_image_gps(self, image_path: str) -> Optional[GeoResult]:
        """
        Extract GPS coordinates from image EXIF data.
        
        Args:
            image_path: Path to the image file.
            
        Returns:
            GeoResult if GPS data found, None otherwise.
        """
        try:
            from PIL import Image
            from PIL.ExifTags import TAGS, GPSTAGS
            
            with Image.open(image_path) as img:
                exif = img._getexif()
                
                if not exif:
                    return None
                
                gps_info = {}
                for tag_id, value in exif.items():
                    tag = TAGS.get(tag_id, tag_id)
                    if tag == 'GPSInfo':
                        for gps_tag_id, gps_value in value.items():
                            gps_tag = GPSTAGS.get(gps_tag_id, gps_tag_id)
                            gps_info[gps_tag] = gps_value
                
                if 'GPSLatitude' in gps_info and 'GPSLongitude' in gps_info:
                    lat = self._convert_to_degrees(gps_info['GPSLatitude'])
                    lon = self._convert_to_degrees(gps_info['GPSLongitude'])
                    
                    if gps_info.get('GPSLatitudeRef') == 'S':
                        lat = -lat
                    if gps_info.get('GPSLongitudeRef') == 'W':
                        lon = -lon
                    
                    return GeoResult(
                        latitude=lat,
                        longitude=lon,
                        accuracy=10,
                        source='exif',
                        metadata={'image': image_path}
                    )
        
        except Exception:
            pass
        
        return None
    
    def _convert_to_degrees(self, value) -> float:
        """Convert GPS coordinates to degrees."""
        d = float(value[0])
        m = float(value[1])
        s = float(value[2])
        return d + (m / 60.0) + (s / 3600.0)
    
    def batch_ip_lookup(self, ip_addresses: List[str]) -> List[GeoResult]:
        """Perform batch IP geolocation."""
        results = []
        for ip in ip_addresses:
            try:
                results.append(self.locate_ip(ip))
            except Exception:
                continue
        return results
