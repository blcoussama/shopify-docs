#!/usr/bin/env python3
"""
Linux-Optimized Ultimate Shopify Documentation Converter
Perfect for Claude Code interaction
"""

import requests
from bs4 import BeautifulSoup
import html2text
import re
import json
import time
from pathlib import Path

class LinuxUltimateConverter:
    def __init__(self):
        self.project_root = Path.cwd().parent
        self.docs_root = self.project_root / "shopify-dev" / "docs"
        
        # Setup HTML to Markdown converter
        self.h = html2text.HTML2Text()
        self.h.ignore_links = False
        self.h.ignore_images = False
        self.h.body_width = 0
        self.h.single_line_break = True
        
        print(f"🚀 Linux Ultimate Converter Ready")
        print(f"📁 Project: {self.project_root}")
        print(f"📄 Docs: {self.docs_root}")
    
    def convert_page(self, shopify_url, file_path):
        """Convert single page with ultimate formatting"""
        
        full_path = self.docs_root / file_path
        if not full_path.exists():
            print(f"❌ File not found: {full_path}")
            return False
        
        print(f"\n🔄 Converting: {shopify_url}")
        print(f"📄 To: {file_path}")
        
        try:
            # Fetch content
            headers = {'User-Agent': 'Mozilla/5.0 (Linux; Ubuntu) AppleWebKit/537.36'}
            response = requests.get(shopify_url, headers=headers, timeout=30)
            response.raise_for_status()
            
            # Parse and process
            soup = BeautifulSoup(response.content, 'html.parser')
            processed_content = self.process_content(soup, shopify_url)
            
            # Write to file
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(processed_content)
            
            print(f"✅ Success! ({len(processed_content)} chars)")
            return True
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def process_content(self, soup, url):
        """Process content for Claude Code optimization"""
        
        # Find main content
        main = (soup.find('main') or 
               soup.find('article') or 
               soup.find('[role="main"]') or 
               soup.find('.content'))
        
        if main:
            soup = main
        
        # Remove navigation elements
        for elem in soup.find_all(['nav', 'header', 'footer', 'aside', 'script', 'style']):
            elem.decompose()
        
        # Process images for Claude Code
        for img in soup.find_all('img'):
            self.convert_image(soup, img)
        
        # Process code blocks
        for pre in soup.find_all('pre'):
            self.enhance_code_block(soup, pre)
        
        # Process info boxes
        for box in soup.find_all(['div'], class_=lambda x: x and any(
            cls in ' '.join(x).lower() for cls in ['warning', 'caution', 'tip', 'note']
        )):
            self.convert_info_box(soup, box)
        
        # Convert to markdown
        markdown = self.h.handle(str(soup))
        
        # Add frontmatter and analysis
        return self.add_metadata(markdown, url)
    
    def convert_image(self, soup, img):
        """Convert image to description for Claude Code"""
        
        alt = img.get('alt', '')
        src = img.get('src', '')
        
        # Generate description
        if 'terminal' in src.lower() or 'cli' in src.lower():
            desc = "Terminal/CLI interface showing command execution"
        elif 'admin' in src.lower():
            desc = "Shopify Admin dashboard interface"
        elif 'code' in src.lower():
            desc = "Code example or file structure illustration"
        elif alt:
            desc = alt
        else:
            desc = "Documentation illustration"
        
        # Replace with description
        desc_elem = soup.new_tag('p')
        desc_elem.string = f"\n**[IMAGE: {desc}]**\n"
        img.replace_with(desc_elem)
    
    def enhance_code_block(self, soup, pre):
        """Enhance code blocks for Claude Code"""
        
        code = pre.get_text()
        
        # Detect language
        if code.strip().startswith(('$', '>', 'npm', 'shopify')):
            lang = 'terminal'
        elif 'import ' in code and 'from ' in code:
            lang = 'javascript'
        elif code.strip().startswith('{'):
            lang = 'json'
        elif '[' in code and ']' in code and '=' in code:
            lang = 'toml'
        else:
            lang = None
        
        # Find filename
        prev = pre.find_previous_sibling()
        filename = None
        if prev:
            text = prev.get_text()
            if any(ext in text for ext in ['.js', '.json', '.toml', '.md']):
                filename = text.strip()
        
        # Create enhanced block
        enhanced = soup.new_tag('div')
        
        if filename:
            file_p = soup.new_tag('p')
            file_p.string = f"**File: `{filename}`**"
            enhanced.append(file_p)
        
        code_p = soup.new_tag('pre')
        if lang:
            code_p.string = f"```{lang}\n{code}\n```"
        else:
            code_p.string = f"```\n{code}\n```"
        enhanced.append(code_p)
        
        pre.replace_with(enhanced)
    
    def convert_info_box(self, soup, box):
        """Convert info boxes to Claude Code format"""
        
        classes = ' '.join(box.get('class', [])).lower()
        
        if 'warning' in classes:
            box_type = '⚠️ WARNING'
        elif 'caution' in classes:
            box_type = '⚠️ CAUTION'  
        elif 'tip' in classes:
            box_type = '💡 TIP'
        else:
            box_type = '📝 NOTE'
        
        content = box.get_text().strip()
        lines = content.split('\n')
        
        # Create blockquote
        quote_text = f"\n> **{box_type}**\n"
        for line in lines:
            if line.strip():
                quote_text += f"> {line.strip()}\n"
        quote_text += ">\n"
        
        quote_elem = soup.new_tag('div')
        quote_elem.string = quote_text
        box.replace_with(quote_elem)
    
    def add_metadata(self, content, url):
        """Add metadata for Claude Code"""
        
        # Extract title
        title = url.split('/')[-1].replace('-', ' ').title()
        
        # Count elements
        word_count = len(content.split())
        code_blocks = content.count('```') // 2
        images = content.count('[IMAGE:')
        
        # Create frontmatter
        frontmatter = f"""---
title: "{title}"
source: "{url}"
converted_for: "Claude Code"
conversion_date: "{time.strftime('%Y-%m-%d %H:%M:%S')}"
stats:
  words: {word_count}
  code_blocks: {code_blocks}
  images: {images}
---

"""
        
        # Add analysis
        analysis = f"""## 🤖 Claude Code Analysis

**Content optimized for AI assistance with:**
- {code_blocks} code examples
- {images} visual elements (converted to descriptions)
- Structured markdown formatting
- Cross-reference ready links

---

"""
        
        return frontmatter + analysis + content
    
    def batch_convert(self, mapping_file="url_mapping.json"):
        """Convert all files from mapping"""
        
        if not Path(mapping_file).exists():
            print(f"❌ No mapping file: {mapping_file}")
            return
        
        with open(mapping_file, 'r') as f:
            mappings = json.load(f)
        
        total = len(mappings)
        success = 0
        
        print(f"\n🚀 BATCH CONVERSION: {total} files")
        print("=" * 50)
        
        for i, (file_path, url) in enumerate(mappings.items(), 1):
            print(f"\n[{i}/{total}] {file_path}")
            
            if self.convert_page(url, file_path):
                success += 1
            
            progress = (i / total) * 100
            print(f"📊 Progress: {progress:.1f}%")
        
        print(f"\n🏁 COMPLETE: {success}/{total} successful")
        print("🤖 Files ready for Claude Code!")

def main():
    """Main execution"""
    converter = LinuxUltimateConverter()
    
    # Check if mapping file exists
    if Path("url_mapping.json").exists():
        print("📋 Found url_mapping.json")
        converter.batch_convert()
    else:
        print("❌ No url_mapping.json found")
        print("💡 Run the smart_url_mapper.py first")

if __name__ == "__main__":
    main()