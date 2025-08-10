#!/usr/bin/env python3
"""
Manual URL Entry System
Let user add exact URLs for specific files
"""

import json
from pathlib import Path

class ManualURLMapper:
    def __init__(self):
        self.project_root = Path.cwd().parent
        self.docs_root = self.project_root / "shopify-dev" / "docs"
        self.mapping_file = Path("manual_url_mapping.json")
        
        print(f"📝 Manual URL Entry System")
        print(f"📁 Docs root: {self.docs_root}")
    
    def add_single_mapping(self):
        """Add one URL mapping manually"""
        
        print("\n📋 Add Single URL Mapping")
        print("=" * 40)
        
        # Get file path
        file_path = input("📄 Enter file path (e.g., apps/build/getting-started/scaffold-an-app.md): ").strip()
        
        if not file_path:
            print("❌ Empty file path")
            return
        
        # Check if file exists
        full_path = self.docs_root / file_path
        if not full_path.exists():
            print(f"❌ File doesn't exist: {full_path}")
            create = input("Create empty file? (y/n): ").lower()
            if create == 'y':
                full_path.parent.mkdir(parents=True, exist_ok=True)
                full_path.touch()
                print(f"✅ Created: {full_path}")
            else:
                return
        
        # Get URL
        url = input("🔗 Enter Shopify docs URL: ").strip()
        
        if not url.startswith("https://shopify.dev/docs"):
            print("❌ Invalid URL - must start with https://shopify.dev/docs")
            return
        
        # Load existing mappings
        mappings = self.load_mappings()
        
        # Add new mapping
        mappings[file_path] = url
        
        # Save mappings
        self.save_mappings(mappings)
        
        print(f"✅ Added mapping:")
        print(f"   📄 {file_path}")
        print(f"   🔗 {url}")
        print(f"📊 Total mappings: {len(mappings)}")
    
    def convert_single_file(self):
        """Convert a single file immediately"""
        
        print("\n🔄 Convert Single File")
        print("=" * 40)
        
        # Get file path
        file_path = input("📄 Enter file path to convert: ").strip()
        
        if not file_path:
            print("❌ Empty file path")
            return
        
        # Get URL
        url = input("🔗 Enter Shopify docs URL: ").strip()
        
        if not url.startswith("https://shopify.dev/docs"):
            print("❌ Invalid URL")
            return
        
        # Convert immediately
        from ultimate_shopify_converter import LinuxUltimateConverter
        converter = LinuxUltimateConverter()
        
        success = converter.convert_page(url, file_path)
        if success:
            print(f"✅ Successfully converted: {file_path}")
        else:
            print(f"❌ Failed to convert: {file_path}")
    
    def convert_all_manual_mappings(self):
        """Convert all manually added mappings"""
        
        mappings = self.load_mappings()
        
        if not mappings:
            print("❌ No manual mappings found")
            return
        
        print(f"\n🚀 Converting {len(mappings)} manually mapped files...")
        
        from ultimate_shopify_converter import LinuxUltimateConverter
        converter = LinuxUltimateConverter()
        
        success_count = 0
        for i, (file_path, url) in enumerate(mappings.items(), 1):
            print(f"\n[{i}/{len(mappings)}] {file_path}")
            
            if converter.convert_page(url, file_path):
                success_count += 1
            
            progress = (i / len(mappings)) * 100
            print(f"📊 Progress: {progress:.1f}%")
        
        print(f"\n🏁 COMPLETE: {success_count}/{len(mappings)} successful")
    
    def show_mappings(self):
        """Show all manual mappings"""
        
        mappings = self.load_mappings()
        
        if not mappings:
            print("📭 No manual mappings found")
            return
        
        print(f"\n📊 Manual Mappings ({len(mappings)} total)")
        print("=" * 60)
        
        for i, (file_path, url) in enumerate(mappings.items(), 1):
            print(f"{i:3}. 📄 {file_path}")
            print(f"     🔗 {url}")
            print()
    
    def load_mappings(self):
        """Load existing manual mappings"""
        if self.mapping_file.exists():
            with open(self.mapping_file, 'r') as f:
                return json.load(f)
        return {}
    
    def save_mappings(self, mappings):
        """Save manual mappings"""
        with open(self.mapping_file, 'w') as f:
            json.dump(mappings, f, indent=2)

def main():
    """Main menu for manual URL entry"""
    mapper = ManualURLMapper()
    
    while True:
        print(f"\n📝 Manual URL Entry System")
        print("1. Add single URL mapping")
        print("2. Convert single file immediately")
        print("3. Show all manual mappings")
        print("4. Convert all manual mappings")
        print("5. Exit")
        
        choice = input("\nChoice: ").strip()
        
        if choice == "1":
            mapper.add_single_mapping()
        elif choice == "2":
            mapper.convert_single_file()
        elif choice == "3":
            mapper.show_mappings()
        elif choice == "4":
            mapper.convert_all_manual_mappings()
        elif choice == "5":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    main()