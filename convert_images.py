#!/usr/bin/env python3
"""
Convert Docsify image syntax to MkDocs Material attr_list format
Converts: ![alt](path ':size=X :no-zoom') -> ![alt](path){ width="X" }
"""

import re
import glob
from pathlib import Path

def convert_image_syntax(content):
    """Convert Docsify image syntax to MkDocs format"""
    # Pattern: ![alt](path ':size=123 :no-zoom')
    # Capture groups: 1=alt text, 2=path, 3=size value
    pattern = r'!\[([^\]]*)\]\(([^\s)]+)\s+[\'"]?:size=(\d+)\s+:no-zoom[\'"]?\)'
    
    # Replace with: ![alt](path){ width="123" }
    replacement = r'![\1](\2){ width="\3" }'
    
    return re.sub(pattern, replacement, content)

def process_file(file_path):
    """Process a single markdown file"""
    print(f"Processing: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if file has any Docsify image syntax
    if ':size=' not in content and ':no-zoom' not in content:
        print(f"  Skipped (no Docsify image syntax)")
        return False
    
    # Convert the syntax
    new_content = convert_image_syntax(content)
    
    # Count changes
    original_count = content.count(':size=')
    new_count = new_content.count(':size=')
    changes = original_count - new_count
    
    if changes > 0:
        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  ✓ Converted {changes} images")
        return True
    else:
        print(f"  No changes needed")
        return False

def main():
    """Main function to process all markdown files"""
    docs_dir = Path(__file__).parent / 'docs'
    md_files = list(docs_dir.glob('*.md'))
    
    print(f"Found {len(md_files)} markdown files\n")
    
    converted_count = 0
    for file_path in sorted(md_files):
        if process_file(file_path):
            converted_count += 1
    
    print(f"\n{'='*50}")
    print(f"Conversion complete!")
    print(f"Files modified: {converted_count}/{len(md_files)}")
    print(f"{'='*50}")

if __name__ == '__main__':
    main()
