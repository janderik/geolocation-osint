#!/usr/bin/env python3
"""
Geolocation OSINT CLI.

A command-line tool for geolocation intelligence.
"""

import argparse
import json
import sys
from pathlib import Path

from src.geo.engine import GeoEngine


def ip_command(args):
    """Execute the IP geolocation command."""
    engine = GeoEngine()
    
    print(f"[*] Looking up IP: {args.ip}")
    
    try:
        result = engine.locate_ip(args.ip)
        
        print(f"\n[+] Location found:\n")
        print(f"  Latitude: {result.latitude}")
        print(f"  Longitude: {result.longitude}")
        print(f"  Source: {result.source}")
        
        if result.metadata:
            print(f"\n  Additional Info:")
            for key, value in result.metadata.items():
                print(f"    {key}: {value}")
        
        if args.output:
            output_data = {
                'ip': args.ip,
                'latitude': result.latitude,
                'longitude': result.longitude,
                'source': result.source,
                'metadata': result.metadata
            }
            Path(args.output).write_text(json.dumps(output_data, indent=2))
            print(f"\n[+] Results saved to: {args.output}")
    
    except Exception as e:
        print(f"[-] Error: {e}")
        sys.exit(1)


def image_command(args):
    """Execute the image GPS extraction command."""
    engine = GeoEngine()
    
    print(f"[*] Extracting GPS from: {args.image}")
    
    try:
        result = engine.extract_image_gps(args.image)
        
        if result:
            print(f"\n[+] GPS data found:\n")
            print(f"  Latitude: {result.latitude}")
            print(f"  Longitude: {result.longitude}")
            
            if args.output:
                output_data = {
                    'image': args.image,
                    'latitude': result.latitude,
                    'longitude': result.longitude
                }
                Path(args.output).write_text(json.dumps(output_data, indent=2))
                print(f"\n[+] Results saved to: {args.output}")
        else:
            print("[-] No GPS data found in image")
    
    except Exception as e:
        print(f"[-] Error: {e}")
        sys.exit(1)


def batch_command(args):
    """Execute the batch IP lookup command."""
    engine = GeoEngine()
    
    # Read IPs from file
    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"[-] File not found: {args.input_file}")
        sys.exit(1)
    
    ips = [line.strip() for line in input_path.read_text().splitlines() if line.strip()]
    
    print(f"[*] Looking up {len(ips)} IP addresses...")
    
    results = []
    for ip in ips:
        try:
            result = engine.locate_ip(ip)
            results.append({
                'ip': ip,
                'latitude': result.latitude,
                'longitude': result.longitude,
                'metadata': result.metadata
            })
            print(f"  [+] {ip}: {result.latitude}, {result.longitude}")
        except Exception as e:
            print(f"  [-] {ip}: Error - {e}")
    
    if args.output:
        Path(args.output).write_text(json.dumps(results, indent=2))
        print(f"\n[+] Results saved to: {args.output}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Geolocation OSINT Tool"
    )
    
    subparsers = parser.add_subparsers(dest='command')
    
    # IP command
    ip_parser = subparsers.add_parser('ip', help='IP geolocation')
    ip_parser.add_argument('ip', help='IP address')
    ip_parser.add_argument('--output', '-o', help='Output file')
    ip_parser.set_defaults(func=ip_command)
    
    # Image command
    image_parser = subparsers.add_parser('image', help='Extract GPS from image')
    image_parser.add_argument('image', help='Image file')
    image_parser.add_argument('--output', '-o', help='Output file')
    image_parser.set_defaults(func=image_command)
    
    # Batch command
    batch_parser = subparsers.add_parser('batch', help='Batch IP lookup')
    batch_parser.add_argument('input_file', help='File with IPs')
    batch_parser.add_argument('--output', '-o', help='Output file')
    batch_parser.set_defaults(func=batch_command)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)


if __name__ == '__main__':
    main()
