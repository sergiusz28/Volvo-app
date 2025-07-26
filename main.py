#!/usr/bin/env python3
"""
Volvo Car Integration App - Main Entry Point
===========================================

This is the main entry point for the Volvo car integration application.
"""

import asyncio
import logging
import sys
from typing import Optional
from volvo_app.api_client import VolvoAPIClient
from volvo_app.config import config


def setup_logging():
    """Setup logging configuration."""
    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('volvo_app.log')
        ]
    )


async def main():
    """Main application function."""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("Starting Volvo Integration App...")
    
    # Initialize the API client
    client = VolvoAPIClient()
    
    try:
        # Authenticate with Volvo API
        if await client.authenticate():
            logger.info("Successfully authenticated with Volvo API")
            
            # Get vehicles
            vehicles = await client.get_vehicles()
            if vehicles:
                logger.info(f"Found {len(vehicles.get('data', []))} vehicles")
                
                # Example: Get status of first vehicle
                if vehicles.get('data'):
                    vin = vehicles['data'][0].get('vin')
                    if vin:
                        status = await client.get_vehicle_status(vin)
                        if status:
                            logger.info(f"Vehicle status: {status}")
            else:
                logger.warning("No vehicles found or failed to retrieve vehicles")
        else:
            logger.error("Failed to authenticate with Volvo API")
            
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        logger.info("Application shutting down...")


def cli():
    """Command line interface entry point."""
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nApplication terminated by user.")
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    cli()
