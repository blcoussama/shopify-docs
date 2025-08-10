#!/usr/bin/env python3
"""
Linux Smart URL Mapper
Creates perfect mappings for Shopify docs conversion
"""

import json
from pathlib import Path
import re

class LinuxSmartMapper:
    def __init__(self):
        self.project_root = Path.cwd().parent
        self.docs_root = self.project_root / "shopify-dev" / "docs"
        self.mapping_file = Path("url_mapping.json")
        
        print(f"🧠 Smart Mapper for Linux")
        print(f"📁 Scanning: {self.docs_root}")
    
    def create_auto_mapping(self):
        """Auto-create mappings from existing files"""
        
        empty_files = []
        for md_file in self.docs_root.rglob("*.md"):
            if md_file.stat().st_size == 0:
                rel_path = md_file.relative_to(self.docs_root)
                empty_files.append(str(rel_path))
        
        print(f"📋 Found {len(empty_files)} empty files")
        
        mappings = {}
        for file_path in empty_files:
            # Convert file path to Shopify URL
            url_path = file_path.replace('.md', '')
            shopify_url = f"https://shopify.dev/docs/{url_path}"
            mappings[file_path] = shopify_url
            
            print(f"📄 {file_path}")
        
        # Save mappings
        with open(self.mapping_file, 'w') as f:
            json.dump(mappings, f, indent=2)
        
        print(f"\n💾 Saved {len(mappings)} mappings to url_mapping.json")
        return mappings
    
    def show_status(self):
        """Show current status"""
        mappings = self.load_mappings()
        
        if not mappings:
            print("📭 No mappings found")
            return
        
        print(f"📊 Status: {len(mappings)} mapped files")
        print("-" * 50)
        
        ready = 0
        missing = 0
        
        for file_path, url in mappings.items():
            full_path = self.docs_root / file_path
            
            if full_path.exists():
                size = full_path.stat().st_size
                if size == 0:
                    status = "✅ Ready"
                    ready += 1
                else:
                    status = f"📝 Has content ({size}b)"
            else:
                status = "❌ Missing"
                missing += 1
            
            print(f"{status:15} {file_path}")
        
        print("-" * 50)
        print(f"✅ Ready: {ready} | ❌ Missing: {missing}")
    
    def load_mappings(self):
        """Load existing mappings"""
        if self.mapping_file.exists():
            with open(self.mapping_file, 'r') as f:
                return json.load(f)
        return {}

def main():
    """Main menu"""
    mapper = LinuxSmartMapper()
    
    while True:
        print(f"\n🧠 Smart URL Mapper")
        print("1. Auto-create mappings from files")
        print("2. Show mapping status")
        print("3. Run conversion")
        print("4. Exit")
        
        choice = input("\nChoice: ").strip()
        
        if choice == "1":
            mapper.create_auto_mapping()
        elif choice == "2":
            mapper.show_status()
        elif choice == "3":
            print("🚀 Running conversion...")
            import subprocess
            subprocess.run(["python3", "ultimate_shopify_converter.py"])
        elif choice == "4":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    main()