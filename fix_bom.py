def fix_bom(filepath):
    """Remove BOM from a file."""
    with open(filepath, 'rb') as file:
        content = file.read()
    
    # Remove BOM if present
    if content.startswith(b'\xef\xbb\xbf'):
        content = content[3:]
    
    # Write back without BOM
    with open(filepath, 'wb') as file:
        file.write(content)

# Fix the specific file
fix_bom(r".\src\ui\views\workflow_view.py")
print("BOM removed successfully")
