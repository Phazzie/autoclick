"""Element selector for visual element selection"""
import json
import logging
from typing import Any, Dict

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.ui.interfaces import ElementSelectorInterface

class VisualElementSelector(ElementSelectorInterface):
    """Allows visual selection of elements on a page"""
    
    def __init__(self) -> None:
        """Initialize the visual element selector"""
        self.logger = logging.getLogger(__name__)
        self.selection_script = """
        // JavaScript to inject into the page for element selection
        return new Promise((resolve) => {
            // Add a highlight effect when hovering over elements
            const style = document.createElement('style');
            style.innerHTML = `
                ._autoclick_hover { 
                    outline: 2px dashed red !important; 
                    outline-offset: 2px !important;
                }
                ._autoclick_selected { 
                    outline: 2px solid blue !important; 
                    outline-offset: 2px !important;
                }
            `;
            document.head.appendChild(style);
            
            let currentElement = null;
            
            // Add hover effect
            document.addEventListener('mouseover', function(e) {
                if (currentElement) {
                    currentElement.classList.remove('_autoclick_hover');
                }
                currentElement = e.target;
                currentElement.classList.add('_autoclick_hover');
            }, true);
            
            // Handle click to select an element
            document.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                const element = e.target;
                
                // Remove hover effect
                if (currentElement) {
                    currentElement.classList.remove('_autoclick_hover');
                }
                
                // Add selected effect
                element.classList.add('_autoclick_selected');
                
                // Get element properties
                const props = {
                    tag_name: element.tagName.toLowerCase(),
                    id: element.id,
                    class: element.className,
                    name: element.getAttribute('name'),
                    type: element.getAttribute('type'),
                    value: element.value,
                    text: element.innerText || element.textContent,
                    html: element.outerHTML,
                    attributes: {},
                };
                
                // Get all attributes
                for (let i = 0; i < element.attributes.length; i++) {
                    const attr = element.attributes[i];
                    props.attributes[attr.name] = attr.value;
                }
                
                // Generate CSS selector
                let cssSelector = '';
                if (element.id) {
                    cssSelector = '#' + element.id;
                } else if (element.className) {
                    const classes = element.className.split(' ')
                        .filter(c => c && !c.startsWith('_autoclick_'));
                    if (classes.length > 0) {
                        cssSelector = '.' + classes.join('.');
                    }
                }
                
                if (!cssSelector) {
                    // Generate a more complex selector
                    let path = '';
                    let el = element;
                    while (el && el.tagName) {
                        let selector = el.tagName.toLowerCase();
                        if (el.id) {
                            selector += '#' + el.id;
                            path = selector + (path ? ' > ' + path : '');
                            break;
                        } else {
                            let sibling = el;
                            let nth = 1;
                            while (sibling = sibling.previousElementSibling) {
                                if (sibling.tagName === el.tagName) nth++;
                            }
                            if (nth > 1) selector += ':nth-of-type(' + nth + ')';
                        }
                        path = selector + (path ? ' > ' + path : '');
                        el = el.parentNode;
                    }
                    cssSelector = path;
                }
                
                props.css_selector = cssSelector;
                
                // Generate XPath
                let xpath = '';
                let node = element;
                while (node && node.nodeType === 1) {
                    let index = 1;
                    let sibling = node;
                    while (sibling = sibling.previousSibling) {
                        if (sibling.nodeType === 1 && sibling.tagName === node.tagName) {
                            index++;
                        }
                    }
                    const xpathPart = node.tagName.toLowerCase() + 
                        (index > 1 ? '[' + index + ']' : '');
                    xpath = '/' + xpathPart + xpath;
                    node = node.parentNode;
                }
                props.xpath = '/html/body' + xpath;
                
                // Clean up
                element.classList.remove('_autoclick_selected');
                document.head.removeChild(style);
                
                // Return the element properties
                resolve(props);
            }, true);
        });
        """
    
    def select_element(self, browser_instance: Any) -> Dict[str, Any]:
        """Allow user to select an element and return its properties"""
        self.logger.info("Starting element selection")
        
        # Display instructions
        browser_instance.execute_script("""
            const div = document.createElement('div');
            div.id = '_autoclick_instructions';
            div.style.cssText = 'position: fixed; top: 0; left: 0; right: 0; background: rgba(0,0,0,0.8); color: white; padding: 10px; z-index: 9999; text-align: center;';
            div.innerHTML = '<b>Click on an element to select it</b>';
            document.body.appendChild(div);
        """)
        
        try:
            # Execute the selection script and wait for the result
            element_props = browser_instance.execute_script(self.selection_script)
            
            self.logger.info(f"Selected element: {element_props['tag_name']} ({element_props['css_selector']})")
            return element_props
        finally:
            # Remove the instructions
            browser_instance.execute_script("""
                const div = document.getElementById('_autoclick_instructions');
                if (div) div.parentNode.removeChild(div);
            """)
    
    def highlight_element(self, browser_instance: Any, selector: str) -> None:
        """Highlight an element on the page"""
        self.logger.info(f"Highlighting element: {selector}")
        
        # Inject highlighting script
        browser_instance.execute_script(f"""
            const element = document.querySelector('{selector}');
            if (element) {{
                const originalOutline = element.style.outline;
                const originalOutlineOffset = element.style.outlineOffset;
                
                element.style.outline = '2px solid red';
                element.style.outlineOffset = '2px';
                
                setTimeout(() => {{
                    element.style.outline = originalOutline;
                    element.style.outlineOffset = originalOutlineOffset;
                }}, 3000);
            }}
        """)
