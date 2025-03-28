"""Checklist manager for tracking and updating project checklists"""
import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class ChecklistManager:
    """Manages project checklists stored in markdown format"""

    def __init__(self, checklist_file: Path):
        """
        Initialize the checklist manager
        
        Args:
            checklist_file: Path to the checklist markdown file
        """
        self.checklist_file = checklist_file
        self.content = self._read_file()
    
    def _read_file(self) -> str:
        """Read the checklist file content"""
        if not self.checklist_file.exists():
            print(f"Checklist file not found: {self.checklist_file}")
            return ""
        
        return self.checklist_file.read_text(encoding="utf-8")
    
    def _write_file(self, content: str) -> None:
        """Write content to the checklist file"""
        self.checklist_file.write_text(content, encoding="utf-8")
        self.content = content
    
    def list_checklists(self) -> List[str]:
        """
        List all checklists in the file
        
        Returns:
            List of checklist names
        """
        # Find all level 3 headers (###) which represent individual checklists
        pattern = r"^### (.+)$"
        matches = re.findall(pattern, self.content, re.MULTILINE)
        return matches
    
    def list_items(self, checklist_name: str) -> List[Tuple[bool, str]]:
        """
        List all items in a specific checklist
        
        Args:
            checklist_name: Name of the checklist
            
        Returns:
            List of tuples (is_checked, item_text)
        """
        # Find the checklist section
        pattern = rf"### {re.escape(checklist_name)}.*?(?=^##|\Z)"
        match = re.search(pattern, self.content, re.MULTILINE | re.DOTALL)
        
        if not match:
            print(f"Checklist not found: {checklist_name}")
            return []
        
        checklist_content = match.group(0)
        
        # Find all checklist items
        item_pattern = r"- \[([ x])\] (.+)$"
        items = re.findall(item_pattern, checklist_content, re.MULTILINE)
        
        # Convert to list of tuples (is_checked, item_text)
        return [(check == "x", text) for check, text in items]
    
    def add_checklist(self, checklist_name: str, section: str) -> None:
        """
        Add a new checklist to the file
        
        Args:
            checklist_name: Name of the new checklist
            section: Section to add the checklist to (e.g., "Core Implementation Checklists")
        """
        # Check if checklist already exists
        if checklist_name in self.list_checklists():
            print(f"Checklist already exists: {checklist_name}")
            return
        
        # Find the section
        section_pattern = rf"^## {re.escape(section)}.*?(?=^##|\Z)"
        match = re.search(section_pattern, self.content, re.MULTILINE | re.DOTALL)
        
        if not match:
            print(f"Section not found: {section}")
            return
        
        section_content = match.group(0)
        
        # Create new checklist content
        new_checklist = f"\n### {checklist_name}\n\n"
        
        # Insert the new checklist at the end of the section
        updated_section = section_content + new_checklist
        updated_content = self.content.replace(section_content, updated_section)
        
        # Write the updated content
        self._write_file(updated_content)
        print(f"Added checklist: {checklist_name}")
    
    def add_item(self, checklist_name: str, item_text: str, checked: bool = False) -> None:
        """
        Add a new item to a checklist
        
        Args:
            checklist_name: Name of the checklist
            item_text: Text of the new item
            checked: Whether the item is checked
        """
        # Find the checklist section
        pattern = rf"### {re.escape(checklist_name)}.*?(?=^##|\Z)"
        match = re.search(pattern, self.content, re.MULTILINE | re.DOTALL)
        
        if not match:
            print(f"Checklist not found: {checklist_name}")
            return
        
        checklist_content = match.group(0)
        
        # Create new item
        check_mark = "x" if checked else " "
        new_item = f"- [{check_mark}] {item_text}\n"
        
        # Add the item to the checklist
        if "- [ ]" in checklist_content or "- [x]" in checklist_content:
            # Add after the last item
            last_item_pattern = r"- \[[ x]\] .+$"
            last_item_match = re.search(last_item_pattern, checklist_content, re.MULTILINE)
            if last_item_match:
                last_item = last_item_match.group(0)
                updated_checklist = checklist_content.replace(
                    last_item, f"{last_item}\n{new_item.strip()}"
                )
            else:
                # Add after the checklist header
                updated_checklist = checklist_content + new_item
        else:
            # No items yet, add after the checklist header
            updated_checklist = checklist_content + new_item
        
        # Update the content
        updated_content = self.content.replace(checklist_content, updated_checklist)
        self._write_file(updated_content)
        print(f"Added item to {checklist_name}: {item_text}")
    
    def check_item(self, checklist_name: str, item_index: int, checked: bool = True) -> None:
        """
        Check or uncheck an item in a checklist
        
        Args:
            checklist_name: Name of the checklist
            item_index: Index of the item (0-based)
            checked: Whether to check or uncheck the item
        """
        # Get the items in the checklist
        items = self.list_items(checklist_name)
        
        if not items:
            return
        
        if item_index < 0 or item_index >= len(items):
            print(f"Invalid item index: {item_index}")
            return
        
        # Find the checklist section
        pattern = rf"### {re.escape(checklist_name)}.*?(?=^##|\Z)"
        match = re.search(pattern, self.content, re.MULTILINE | re.DOTALL)
        
        if not match:
            print(f"Checklist not found: {checklist_name}")
            return
        
        checklist_content = match.group(0)
        
        # Find all checklist items
        item_pattern = r"- \[([ x])\] (.+)$"
        item_matches = list(re.finditer(item_pattern, checklist_content, re.MULTILINE))
        
        if item_index >= len(item_matches):
            print(f"Item index out of range: {item_index}")
            return
        
        # Get the item to update
        item_match = item_matches[item_index]
        item_text = item_match.group(2)
        
        # Create updated item
        check_mark = "x" if checked else " "
        updated_item = f"- [{check_mark}] {item_text}"
        
        # Replace the item in the checklist
        start, end = item_match.span(0)
        updated_checklist = (
            checklist_content[:start] + updated_item + checklist_content[end:]
        )
        
        # Update the content
        updated_content = self.content.replace(checklist_content, updated_checklist)
        self._write_file(updated_content)
        
        status = "Checked" if checked else "Unchecked"
        print(f"{status} item {item_index} in {checklist_name}: {item_text}")


def parse_args() -> argparse.Namespace:
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Manage project checklists")
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # List checklists
    list_parser = subparsers.add_parser("list", help="List checklists")
    
    # List items in a checklist
    items_parser = subparsers.add_parser("items", help="List items in a checklist")
    items_parser.add_argument("checklist", help="Name of the checklist")
    
    # Add a new checklist
    add_checklist_parser = subparsers.add_parser("add-checklist", help="Add a new checklist")
    add_checklist_parser.add_argument("name", help="Name of the checklist")
    add_checklist_parser.add_argument("section", help="Section to add the checklist to")
    
    # Add a new item to a checklist
    add_item_parser = subparsers.add_parser("add-item", help="Add a new item to a checklist")
    add_item_parser.add_argument("checklist", help="Name of the checklist")
    add_item_parser.add_argument("item", help="Text of the item")
    add_item_parser.add_argument("--checked", action="store_true", help="Mark the item as checked")
    
    # Check or uncheck an item
    check_parser = subparsers.add_parser("check", help="Check or uncheck an item")
    check_parser.add_argument("checklist", help="Name of the checklist")
    check_parser.add_argument("item", type=int, help="Index of the item (0-based)")
    check_parser.add_argument("--uncheck", action="store_true", help="Uncheck the item")
    
    return parser.parse_args()


def main() -> None:
    """Main entry point"""
    args = parse_args()
    
    # Get the checklist file path
    checklist_file = Path("checklists.md")
    
    # Create the checklist manager
    manager = ChecklistManager(checklist_file)
    
    # Execute the command
    if args.command == "list":
        checklists = manager.list_checklists()
        print("Available checklists:")
        for i, checklist in enumerate(checklists):
            print(f"{i}: {checklist}")
    
    elif args.command == "items":
        items = manager.list_items(args.checklist)
        print(f"Items in {args.checklist}:")
        for i, (checked, text) in enumerate(items):
            status = "✓" if checked else "☐"
            print(f"{i}: [{status}] {text}")
    
    elif args.command == "add-checklist":
        manager.add_checklist(args.name, args.section)
    
    elif args.command == "add-item":
        manager.add_item(args.checklist, args.item, args.checked)
    
    elif args.command == "check":
        manager.check_item(args.checklist, args.item, not args.uncheck)
    
    else:
        print("No command specified. Use --help for usage information.")


if __name__ == "__main__":
    main()
