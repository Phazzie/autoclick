"""Browser action recorder"""
import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from src.ui.interfaces import RecorderInterface

class BrowserRecorder(RecorderInterface):
    """Records user actions in a browser"""
    
    def __init__(self) -> None:
        """Initialize the browser recorder"""
        self.logger = logging.getLogger(__name__)
        self.driver = None
        self.is_recording = False
        self.recording_script = """
        // JavaScript to inject into the page for recording user actions
        (function() {
            if (window._autoClickRecorder) return window._autoClickRecorderActions;
            
            window._autoClickRecorderActions = [];
            window._autoClickRecorder = true;
            
            // Record clicks
            document.addEventListener('click', function(e) {
                const element = e.target;
                const selector = getSelector(element);
                window._autoClickRecorderActions.push({
                    type: 'click',
                    selector: selector,
                    timestamp: Date.now()
                });
            }, true);
            
            // Record inputs
            document.addEventListener('change', function(e) {
                const element = e.target;
                if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA' || element.tagName === 'SELECT') {
                    const selector = getSelector(element);
                    window._autoClickRecorderActions.push({
                        type: 'input',
                        selector: selector,
                        value: element.value,
                        timestamp: Date.now()
                    });
                }
            }, true);
            
            // Helper function to get a unique selector for an element
            function getSelector(element) {
                if (element.id) return '#' + element.id;
                if (element.className) {
                    const classes = element.className.split(' ').filter(c => c);
                    if (classes.length > 0) return '.' + classes.join('.');
                }
                
                // Fallback to a more complex selector
                let path = '';
                while (element && element.tagName) {
                    let selector = element.tagName.toLowerCase();
                    if (element.id) {
                        selector += '#' + element.id;
                        path = selector + (path ? ' > ' + path : '');
                        break;
                    } else {
                        let sibling = element;
                        let nth = 1;
                        while (sibling = sibling.previousElementSibling) {
                            if (sibling.tagName === element.tagName) nth++;
                        }
                        if (nth > 1) selector += ':nth-of-type(' + nth + ')';
                    }
                    path = selector + (path ? ' > ' + path : '');
                    element = element.parentNode;
                }
                return path;
            }
            
            return window._autoClickRecorderActions;
        })();
        """
    
    def start_recording(self) -> None:
        """Start recording user actions"""
        self.logger.info("Starting browser recording")
        
        # Initialize Chrome driver
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        
        # Inject the recording script
        self.driver.execute_script(self.recording_script)
        
        self.is_recording = True
        self.logger.info("Recording started")
    
    def stop_recording(self) -> List[Dict[str, Any]]:
        """Stop recording and return captured actions"""
        if not self.is_recording or not self.driver:
            self.logger.warning("No active recording to stop")
            return []
        
        self.logger.info("Stopping browser recording")
        
        # Get the recorded actions
        actions = self.driver.execute_script("return window._autoClickRecorderActions;")
        
        # Close the browser
        self.driver.quit()
        self.driver = None
        self.is_recording = False
        
        self.logger.info(f"Recording stopped, captured {len(actions)} actions")
        return actions
