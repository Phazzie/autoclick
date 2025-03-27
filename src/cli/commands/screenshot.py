"""Screenshot command handler"""
import argparse
import logging
from pathlib import Path
from typing import Optional

from src.core.automation_engine import AutomationEngine
from src.core.element_detector import ElementDetector


def screenshot_command(args: argparse.Namespace) -> int:
    """
    Handle the screenshot command
    
    Args:
        args: Command-line arguments
        
    Returns:
        Exit code
    """
    logger = logging.getLogger(__name__)
    
    # If no subcommand is specified, show help
    if not hasattr(args, "subcommand") or not args.subcommand:
        logger.error("No subcommand specified")
        return 2
    
    try:
        # Create configuration from arguments
        config = {
            "browser": args.browser,
            "headless": args.headless,
            "timeout": args.timeout,
            "screenshots_dir": args.output_dir,
        }
        
        # Initialize the automation engine
        engine = AutomationEngine()
        engine.initialize(config)
        
        # Initialize the driver
        engine.driver = engine.driver_manager.initialize_driver()
        
        # Handle the page subcommand
        if args.subcommand == "page":
            # Navigate to the URL
            logger.info(f"Navigating to {args.url}")
            engine.driver.get(args.url)
            
            # Wait for the page to load
            if args.wait:
                logger.info(f"Waiting for {args.wait} seconds")
                import time
                time.sleep(args.wait)
            
            # Take the screenshot
            screenshot_path = engine.take_screenshot(args.name)
            
            if screenshot_path:
                logger.info(f"Screenshot saved: {screenshot_path}")
                return 0
            else:
                logger.error("Failed to take screenshot")
                return 4
        
        # Handle the element subcommand
        elif args.subcommand == "element":
            # Navigate to the URL
            logger.info(f"Navigating to {args.url}")
            engine.driver.get(args.url)
            
            # Wait for the page to load
            if args.wait:
                logger.info(f"Waiting for {args.wait} seconds")
                import time
                time.sleep(args.wait)
            
            # Create an element detector
            detector = ElementDetector(engine.driver)
            
            # Find the element
            logger.info(f"Finding element: {args.selector}")
            element = detector.find_element(args.selector)
            
            if not element:
                logger.error(f"Element not found: {args.selector}")
                return 4
            
            # Take the element screenshot
            screenshot_path = engine.take_element_screenshot(element, args.name)
            
            if screenshot_path:
                logger.info(f"Element screenshot saved: {screenshot_path}")
                return 0
            else:
                logger.error("Failed to take element screenshot")
                return 4
        
        else:
            logger.error(f"Unknown subcommand: {args.subcommand}")
            return 2
    
    except KeyboardInterrupt:
        logger.info("Screenshot command interrupted by user")
        return 1
    except Exception as e:
        logger.error(f"Error in screenshot command: {str(e)}")
        return 4
    finally:
        # Clean up resources
        if 'engine' in locals() and engine:
            engine.cleanup()
