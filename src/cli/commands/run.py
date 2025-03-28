"""Run command handler"""
import argparse
import logging
import os
from pathlib import Path
from typing import List

from src.core.automation_engine import AutomationEngine
from src.core.sequence_runner import SequenceRunner
from src.core.parallel_runner import ParallelRunner


def run_command(args: argparse.Namespace) -> int:
    """
    Handle the run command
    
    Args:
        args: Command-line arguments
        
    Returns:
        Exit code
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Running script(s): {args.script_path}")
    
    # Create configuration from arguments
    config = {
        "browser": args.browser,
        "headless": args.headless,
        "timeout": args.timeout,
        "max_workers": args.max_workers,
    }
    
    # If a config file is specified, load it
    if args.config:
        try:
            import json
            with open(args.config, "r") as f:
                file_config = json.load(f)
                config.update(file_config)
        except Exception as e:
            logger.error(f"Error loading config file: {str(e)}")
            return 3
    
    # Initialize the automation engine
    engine = AutomationEngine()
    engine.initialize(config)
    
    # Get the script paths
    script_path = Path(args.script_path)
    scripts = []
    
    if script_path.is_file():
        scripts = [script_path]
    elif script_path.is_dir():
        scripts = list(script_path.glob("*.py"))
    else:
        logger.error(f"Script path not found: {script_path}")
        return 2
    
    if not scripts:
        logger.error(f"No scripts found at: {script_path}")
        return 2
    
    logger.info(f"Found {len(scripts)} script(s)")
    
    try:
        # Choose the appropriate runner
        if args.parallel:
            logger.info("Using parallel runner")
            runner = ParallelRunner()
        else:
            logger.info("Using sequence runner")
            runner = SequenceRunner()
        
        # Initialize the runner
        runner.initialize(config)
        
        # Run the scripts
        results = runner.run(engine, scripts)
        
        # Process the results
        success_count = sum(1 for result in results["results"] if result.get("status") == "success")
        error_count = sum(1 for result in results["results"] if result.get("status") == "error")
        
        logger.info(f"Execution completed: {success_count} succeeded, {error_count} failed")
        
        # Print detailed results if not in quiet mode
        if not args.quiet:
            for i, result in enumerate(results["results"]):
                status = result.get("status", "unknown")
                script = result.get("script", f"Script {i+1}")
                message = result.get("message", "")
                
                if status == "success":
                    logger.info(f"{script}: Success")
                else:
                    logger.error(f"{script}: Error - {message}")
        
        # Return appropriate exit code
        if error_count > 0:
            return 4
        return 0
    
    except KeyboardInterrupt:
        logger.info("Execution interrupted by user")
        return 1
    except Exception as e:
        logger.error(f"Error during execution: {str(e)}")
        return 4
