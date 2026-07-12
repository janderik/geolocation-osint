"""Map visualization for geolocation data."""

from typing import List, Dict, Any
from pathlib import Path


class MapGenerator:
    """Generate HTML maps from geolocation data."""
    
    def __init__(self):
        """Initialize the map generator."""
        self.template = """
<!DOCTYPE html>
<html>
<head>
    <title>Geolocation Map</title>
    <style>
        #map {{ height: 600px; width: 100%; }}
    </style>
</head>
<body>
    <h1>Geolocation Results</h1>
    <div id="map"></div>
    <script>
        function initMap() {{
            var map = new google.maps.Map(document.getElementById('map'), {{
                zoom: 2,
                center: {{lat: 0, lng: 0}}
            }});
            
            var locations = {locations};
            
            locations.forEach(function(loc) {{
                new google.maps.Marker({{
                    position: {{lat: loc.lat, lng: loc.lng}},
                    map: map,
                    title: loc.label
                }});
            }});
        }}
    </script>
    <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&callback=initMap"></script>
</body>
</html>
"""
    
    def generate_map(
        self,
        locations: List[Dict[str, Any]],
        output_path: str
    ) -> str:
        """
        Generate an HTML map from locations.
        
        Args:
            locations: List of location dictionaries with lat, lng, label.
            output_path: Path to save the HTML file.
            
        Returns:
            Path to the generated file.
        """
        import json
        
        html = self.template.format(locations=json.dumps(locations))
        
        path = Path(output_path)
        path.write_text(html)
        
        return str(path)
