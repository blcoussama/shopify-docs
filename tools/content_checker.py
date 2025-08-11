#!/usr/bin/env python3
"""
Content Checker - Automated detection and fixing of Unicode/file icon issues
This script MUST be run before writing any markdown file to prevent recurring issues.
"""

import re
import sys
from pathlib import Path

class ContentChecker:
    def __init__(self):
        # Patterns for problematic Unicode characters
        self.unicode_patterns = [
            r'\x1c\x00\x00',  # FS NULNUL
            r'\x02',           # STX
            r'\x14\x00\x00',  # DLE NULNUL
        ]
        
        # Patterns for corrupted file icons
        self.file_icon_patterns = [
            r'\*\*=�[^*]*\*\*',      # **=� filename**
            r'\*\*=\\ufffd[^*]*\*\*', # **=\ufffd filename**
            r'\*\*=[^📁][^*]*\*\*',   # Any **=X filename** that's not 📁
        ]
        
        # Unicode tree characters to replace with ASCII
        self.unicode_tree_replacements = {
            '├': '├──',
            '│': '│',
            '└': '└──',
            '┌': '├──',
            '┐': '├──',
            '┘': '└──',
            '┴': '└──',
        }

    def check_content(self, content: str) -> dict:
        """Check content for issues and return findings"""
        issues = {
            'unicode_issues': [],
            'file_icon_issues': [],
            'directory_structure_issues': [],
            'has_issues': False
        }
        
        # Check for Unicode character issues
        for i, line in enumerate(content.split('\n'), 1):
            # Check for binary unicode characters (hexdump would show these)
            if any(char in line for char in ['\x1c', '\x02', '\x14']):
                issues['unicode_issues'].append(f"Line {i}: Binary Unicode characters detected")
                issues['has_issues'] = True
            
            # Check for corrupted file icons
            for pattern in self.file_icon_patterns:
                if re.search(pattern, line):
                    issues['file_icon_issues'].append(f"Line {i}: Corrupted file icon - {line.strip()}")
                    issues['has_issues'] = True
            
            # Check for Unicode tree characters in directory structures
            if any(char in line for char in self.unicode_tree_replacements.keys()):
                if '```' in content and 'extensions/' in line:  # Likely directory structure
                    issues['directory_structure_issues'].append(f"Line {i}: Unicode tree characters in directory structure")
                    issues['has_issues'] = True
        
        return issues

    def fix_content(self, content: str) -> str:
        """Automatically fix detected issues"""
        fixed_content = content
        
        # Fix file icon issues - replace corrupted icons with 📁
        for pattern in self.file_icon_patterns:
            def replace_icon(match):
                # Extract the filename part and replace with proper format
                line = match.group(0)
                # Extract filename between ** **
                filename_match = re.search(r'\*\*[^*]+\*\*', line)
                if filename_match:
                    old_format = filename_match.group(0)
                    filename = old_format.replace('**=�', '').replace('**=\\ufffd', '').replace('**', '').strip()
                    new_format = f"**📁 {filename}**"
                    return line.replace(old_format, new_format)
                return line
            
            fixed_content = re.sub(pattern, replace_icon, fixed_content)
        
        # Fix Unicode tree characters
        for unicode_char, ascii_replacement in self.unicode_tree_replacements.items():
            fixed_content = fixed_content.replace(unicode_char, ascii_replacement)
        
        # Remove any binary Unicode characters
        fixed_content = re.sub(r'[\x00-\x08\x0b-\x1f\x7f-\xff]', '', fixed_content)
        
        return fixed_content

    def validate_file(self, file_path: str) -> tuple[bool, dict, str]:
        """Complete validation and fixing of a file"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
        except UnicodeDecodeError:
            # File has binary corruption - needs complete recreation
            return False, {'binary_corruption': True, 'has_issues': True}, ""
        
        issues = self.check_content(content)
        
        if issues['has_issues']:
            fixed_content = self.fix_content(content)
            return False, issues, fixed_content
        
        return True, issues, content

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 content_checker.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    checker = ContentChecker()
    
    is_clean, issues, fixed_content = checker.validate_file(file_path)
    
    if is_clean:
        print(f"✅ {file_path} is clean - no issues detected")
        sys.exit(0)
    else:
        print(f"❌ {file_path} has issues:")
        for category, issue_list in issues.items():
            if issue_list and category != 'has_issues':
                print(f"  {category}: {len(issue_list)} issues")
                for issue in issue_list[:3]:  # Show first 3 issues
                    print(f"    - {issue}")
        
        if 'binary_corruption' in issues:
            print("🔧 File has binary corruption - requires complete recreation")
        else:
            print("🔧 Auto-fixed content available")
            # Optionally write fixed content back
            # with open(file_path, 'w', encoding='utf-8') as f:
            #     f.write(fixed_content)
        
        sys.exit(1)

if __name__ == "__main__":
    main()