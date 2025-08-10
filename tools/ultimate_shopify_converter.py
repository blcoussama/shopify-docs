#!/usr/bin/env python3
"""
FIXED Ultimate Shopify Documentation Converter
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
        
        # Create directory if it doesn't exist
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        print(f"\n🔄 Converting: {shopify_url}")
        print(f"📄 To: {file_path}")
        
        try:
            # Fetch content
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
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
        
        # Find main content area
        main_content = None
        for selector in [
            'main',
            '[role="main"]', 
            '.content',
            '.main-content',
            'article',
            '.docs-content'
        ]:
            main_content = soup.select_one(selector)
            if main_content:
                break
        
        if main_content:
            soup = main_content
        
        # Remove unwanted elements
        for selector in ['nav', 'header', 'footer', 'aside', 'script', 'style', '.navigation', '.sidebar']:
            for elem in soup.select(selector):
                elem.decompose()
        
        # Process images for Claude Code
        for img in soup.find_all('img'):
            self.convert_image_to_description(img)
        
        # Process code blocks
        for pre in soup.find_all('pre'):
            self.enhance_code_block(pre)
        
        # Process info boxes
        for box in soup.find_all(['div', 'aside'], class_=lambda x: x and any(
            cls in ' '.join(x).lower() for cls in ['warning', 'caution', 'tip', 'note', 'info']
        )):
            self.convert_info_box(box)
        
        # Convert to markdown
        try:
            markdown = self.h.handle(str(soup))
        except Exception as e:
            print(f"⚠️ Markdown conversion issue: {e}")
            markdown = str(soup)  # Fallback to raw HTML
        
        # Add frontmatter and analysis
        return self.add_metadata(markdown, url)
    
    def convert_image_to_description(self, img):
        """Convert image to detailed description for Claude Code"""
        
        alt = img.get('alt', '')
        src = img.get('src', '')
        
        # Generate contextual description
        if 'terminal' in src.lower() or 'cli' in src.lower():
            desc = "Terminal/CLI interface showing command execution and output"
        elif 'admin' in src.lower() or 'dashboard' in src.lower():
            desc = "Shopify Admin dashboard interface showing configuration options"
        elif 'code' in src.lower() or 'editor' in src.lower():
            desc = "Code editor interface showing file structure and code examples"
        elif 'diagram' in src.lower():
            desc = "Technical diagram illustrating system architecture or workflow"
        elif alt:
            desc = f"Interface screenshot: {alt}"
        else:
            desc = "Documentation illustration showing relevant UI or workflow"
        
        # Replace with enhanced description
        new_p = img.parent.new_tag('p') if img.parent else BeautifulSoup('<p></p>', 'html.parser').p
        new_p.string = f"\n**[IMAGE: {desc}]**\n"
        img.replace_with(new_p)
    
    def enhance_code_block(self, pre):
        """Enhance code blocks for Claude Code understanding"""
        
        code_text = pre.get_text()
        
        # Detect language from content
        if code_text.strip().startswith(('$', '>', 'npm', 'shopify', 'cd ', 'mkdir')):
            lang = 'bash'
        elif 'import ' in code_text and ('from ' in code_text or 'react' in code_text.lower()):
            lang = 'javascript'
        elif 'function' in code_text and ('{' in code_text or '=>' in code_text):
            lang = 'javascript'
        elif code_text.strip().startswith(('{', '[')):
            lang = 'json'
        elif '=' in code_text and ('[' in code_text or 'name =' in code_text):
            lang = 'toml'
        elif 'query' in code_text.lower() and ('{' in code_text or 'mutation' in code_text.lower()):
            lang = 'graphql'
        else:
            lang = None
        
        # Look for filename hints
        filename = None
        prev_elem = pre.find_previous_sibling()
        if prev_elem:
            text = prev_elem.get_text()
            if any(ext in text for ext in ['.js', '.json', '.toml', '.md', '.tsx', '.jsx']):
                filename = text.strip()
        
        # Create enhanced block
        enhanced_html = ""
        
        if filename:
            enhanced_html += f"<p><strong>File: <code>{filename}</code></strong></p>\n"
        
        if lang:
            enhanced_html += f"<pre><code class='language-{lang}'>{code_text}</code></pre>"
        else:
            enhanced_html += f"<pre><code>{code_text}</code></pre>"
        
        # Replace with enhanced version
        new_soup = BeautifulSoup(enhanced_html, 'html.parser')
        pre.replace_with(new_soup)
    
    def convert_info_box(self, box):
        """Convert info boxes to Claude Code format"""
        
        classes = ' '.join(box.get('class', [])).lower()
        
        if 'warning' in classes:
            box_type = '⚠️ WARNING'
        elif 'caution' in classes:
            box_type = '⚠️ CAUTION'  
        elif 'tip' in classes:
            box_type = '💡 TIP'
        elif 'info' in classes:
            box_type = '📝 INFO'
        else:
            box_type = '📝 NOTE'
        
        content = box.get_text().strip()
        
        # Create blockquote format
        quote_html = f"<blockquote><strong>{box_type}</strong><br>{content}</blockquote>"
        new_soup = BeautifulSoup(quote_html, 'html.parser')
        box.replace_with(new_soup)
    
    def add_metadata(self, content, url):
        """Add metadata for Claude Code optimization"""
        
        # Extract title from URL
        title = url.split('/')[-1].replace('-', ' ').title()
        
        # Count elements for analysis
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
        
        # Add Claude Code analysis
        analysis = f"""## 🤖 Claude Code Analysis

**Content optimized for AI assistance:**
- {code_blocks} code examples ready for analysis
- {images} visual elements converted to descriptions  
- Structured markdown with enhanced formatting
- Cross-reference ready internal links

**Perfect for Claude Code to help with:**
- Code review and optimization
- Implementation guidance
- Troubleshooting and debugging
- Best practices recommendations

---

"""
        
        return frontmatter + analysis + content
    
    def batch_convert(self, mapping_file="manual_url_mapping.json"):
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
            else:
                print(f"❌ Failed: {file_path}")
            
            # Brief pause to be respectful to the server
            time.sleep(1)
            
            progress = (i / total) * 100
            print(f"📊 Progress: {progress:.1f}%")
        
        print(f"\n🏁 COMPLETE: {success}/{total} successful")
        print("🤖 Files ready for Claude Code!")

def main():
    """Main execution"""
    converter = LinuxUltimateConverter()
    
    # Check if mapping file exists
    if Path("manual_url_mapping.json").exists():
        print("📋 Found manual_url_mapping.json")
        converter.batch_convert()
    else:
        print("❌ No manual_url_mapping.json found")
        print("💡 Use the manual_url_mapper.py to create mappings first")

if __name__ == "__main__":
    main()