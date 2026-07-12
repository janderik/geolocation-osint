# Geolocation OSINT

[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

A comprehensive geolocation intelligence tool for OSINT investigations. Determine locations from IP addresses, images, and social media metadata.

## Features

- **IP geolocation** - Locate devices by IP address
- **Image geolocation** - Extract GPS from photos
- **Social media geo** - Find location data from posts
- **Map visualization** - Interactive map output
- **Batch processing** - Analyze multiple targets

## Installation

```bash
git clone https://github.com/janderik/geolocation-osint.git
cd geolocation-osint
pip install -r requirements.txt
```

## Usage

```bash
# IP geolocation
python cli.py ip 8.8.8.8

# Extract GPS from image
python cli.py image photo.jpg

# Batch IP lookup
python cli.py batch ips.txt --output results.json

# Generate map
python cli.py map results.json --output map.html
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
