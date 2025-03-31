import os
import codecs

def verify_file_encoding(filepath):
    """Verify file encoding and check for BOM."""
    print(f"\nVerifying file: {filepath}")
    print("=" * 50)
    
    if not os.path.exists(filepath):
        print("❌ ERROR: File not found!")
        return False
        
    # Check raw bytes for BOM
    with open(filepath, 'rb') as file:
        raw_content = file.read()
        has_bom = raw_content.startswith(b'\xef\xbb\xbf')
        print(f"BOM present: {'❌ Yes' if has_bom else '✅ No'}")
        
    # Try reading with different encodings
    encodings = ['utf-8', 'utf-8-sig', 'utf-16', 'utf-16le', 'utf-16be']
    successful_encodings = []
    
    for encoding in encodings:
        try:
            with codecs.open(filepath, 'r', encoding=encoding) as file:
                file.read()
            successful_encodings.append(encoding)
        except UnicodeError:
            continue
            
    print(f"\nFile can be read with these encodings: {', '.join(successful_encodings)}")
    
    # Check first few bytes
    print("\nFirst 10 bytes of file (hex):")
    print(' '.join(f'{b:02x}' for b in raw_content[:10]))
    
    # Final verdict
    is_valid = not has_bom and 'utf-8' in successful_encodings
    print("\nFinal verdict:", "✅ File is correctly encoded" if is_valid else "❌ File needs fixing")
    
    return is_valid

# Quick final verification
def verify_git_encoding():
    """Verify that Git settings will maintain correct encoding."""
    import subprocess
    
    filepath = r".\src\ui\views\workflow_view.py"
    
    try:
        # Check Git attributes for the file
        result = subprocess.run(['git', 'check-attr', 'encoding', filepath], 
                              capture_output=True, text=True)
        
        print("\nGit Attribute Check:")
        print("=" * 50)
        if "encoding: utf-8" in result.stdout:
            print("✅ Git attributes correctly set (encoding=utf-8)")
        else:
            print("❌ Warning: Git encoding attribute not set")
            
        # Verify the file one last time
        verify_file_encoding(filepath)
        
    except Exception as e:
        print(f"Error checking Git attributes: {str(e)}")

if __name__ == '__main__':
    verify_git_encoding()
