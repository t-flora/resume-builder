#!/usr/bin/env python3
"""
Resume Builder - Python Preprocessor for Role-Based Content

This script processes LaTeX files and filters content based on role tags.
Supports nested content blocks and individual line filtering.
"""

import argparse
import re
import sys
from pathlib import Path
from typing import List, Set, Optional


class ResumeBuilder:
    """
    ResumeBuilder class for processing LaTeX files and filtering content based on role tags.
    Supports nested content blocks and individual line filtering.
    """
    def __init__(self, source_dir: str, output_dir: str, roles: List[str], include_location: bool = False):
        self.source_dir = Path(source_dir) # source directory containing LaTeX files
        self.output_dir = Path(output_dir) # output directory for processed files - NEW LaTeX files will be written here
        self.roles = set(roles) # set of roles to build resumes for
        self.current_role = None # current role being processed
        self.include_location = include_location # whether to include location in header
        
        # Tag patterns
        self.start_tag_pattern = re.compile(r'\\begin\{rolecontent\}\{([^}]+)\}') # pattern matches \begin{rolecontent}{roles}
        self.end_tag_pattern = re.compile(r'\\end\{rolecontent\}')
        self.inline_tag_pattern = re.compile(r'\\rolecontent\{([^}]+)\}\{([^}]*)\}') # pattern matches \rolecontent{roles}{content}
        self.exclude_tag_pattern = re.compile(r'\\exclude\{([^}]*)\}') # pattern matches \exclude{content}
        self.exclude_start_pattern = re.compile(r'\\begin\{exclude\}') # pattern matches \begin{exclude}
        self.exclude_end_pattern = re.compile(r'\\end\{exclude\}') # pattern matches \end{exclude}
        
    def parse_role_list(self, role_string: str) -> Set[str]:
        """Parse comma-separated role list and return set of roles."""
        return {role.strip() for role in role_string.split(',')}
    
    def should_include_content(self, content_roles: Set[str]) -> bool:
        """Check if content should be included for current role."""
        if not content_roles:  # No tags = include for all roles
            return True
        return bool(content_roles & {self.current_role})
    
    def process_line(self, line: str) -> Optional[str]:
        """Process a single line and return filtered content."""
        # Check for exclude tags first - these always remove the line
        if self.exclude_tag_pattern.search(line):
            return None
        
        # Check for simple single-line rolecontent tags (not multi-line)
        # Only process tags that don't contain \begin or \end
        if '\\rolecontent{' in line and '\\begin{' not in line and '\\end{' not in line:
            processed_line = self.process_simple_rolecontent_tags(line)
            return processed_line
        
        return line
    
    def process_simple_rolecontent_tags(self, line: str) -> Optional[str]:
        """Process simple single-line rolecontent tags."""
        # Find all rolecontent tags in the line
        result = line
        while True:
            # Find the start of a rolecontent tag
            start_match = re.search(r'\\rolecontent\{([^}]+)\}\{', result)
            if not start_match:
                break
            
            start_pos = start_match.start()
            roles_str = start_match.group(1)
            
            # Find the matching closing brace by counting braces
            brace_count = 0
            content_start = result.find('{', start_pos) + 1
            content_end = content_start
            
            for i, char in enumerate(result[content_start:], content_start):
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    if brace_count == 0:
                        content_end = i
                        break
                    brace_count -= 1
            
            if content_end == content_start:
                # No closing brace found, skip this tag
                break
            
            # Extract the content and roles
            content = result[content_start:content_end]
            content_roles = self.parse_role_list(roles_str)
            
            # Replace the tag with content or remove it
            if self.should_include_content(content_roles):
                # Replace the entire tag with just the content
                tag_start = result.find('\\rolecontent{', start_pos)
                result = result[:tag_start] + content + result[content_end + 1:]
            else:
                # Remove the entire tag
                tag_start = result.find('\\rolecontent{', start_pos)
                result = result[:tag_start] + result[content_end + 1:]
        
        return result if result.strip() else None
    
    def process_file(self, input_file: Path, output_file: Path) -> None:
        """Process a single LaTeX file and write filtered output."""
        print(f"Processing {input_file} -> {output_file}")
        
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Process the content
        processed_content = self.process_content(content)
        
        # Write output
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(processed_content)
    
    def process_multiline_rolecontent(self, content: str) -> str:
        """Process rolecontent tags that span multiple lines."""
        # Use a regex to match from the start of the line, including whitespace
        pattern = re.compile(
            r'(^[ \t]*)?\\rolecontent\{([^}]+)\}\{', re.MULTILINE
        )
        result = content
        while True:
            start_match = pattern.search(result)
            if not start_match:
                break
            start_pos = start_match.start()
            leading_ws = start_match.group(1) or ''
            roles_str = start_match.group(2)
            
            # Find the matching closing brace for the content
            brace_count = 1
            i = start_match.end()
            while i < len(result) and brace_count > 0:
                if result[i] == '{':
                    brace_count += 1
                elif result[i] == '}':
                    brace_count -= 1
                i += 1
            
            content_inside = result[start_match.end():i-1]
            should_include = self.should_include_content(self.parse_role_list(roles_str))
            
            if should_include:
                replacement = content_inside
            else:
                replacement = ''
            
            # Replace from start_pos to i (end of closing brace)
            result = result[:start_pos] + replacement + result[i:]
        
        return result
    
    def process_content(self, content: str) -> str:
        """Process content with role-based filtering."""
        # First, process multi-line rolecontent tags
        content = self.process_multiline_rolecontent(content)
        lines = content.split('\n')
        processed_lines = []
        in_role_block = False
        in_exclude_block = False
        current_block_roles = set()
        block_content = []
        for line in lines:
            # Check for start of exclude block
            if self.exclude_start_pattern.search(line):
                in_exclude_block = True
                continue
            # Check for end of exclude block
            if self.exclude_end_pattern.search(line):
                in_exclude_block = False
                continue
            # Skip lines if we're in an exclude block
            if in_exclude_block:
                continue
            # Check for start of rolecontent block
            start_match = self.start_tag_pattern.search(line)
            if start_match:
                in_role_block = True
                roles_str = start_match.group(1)
                current_block_roles = self.parse_role_list(roles_str)
                continue
            # Check for end of rolecontent block
            if self.end_tag_pattern.search(line):
                in_role_block = False
                if self.should_include_content(current_block_roles):
                    processed_lines.extend(block_content)
                block_content = []
                current_block_roles = set()
                continue
            # If we're in a role block, collect content but also process inline tags
            if in_role_block:
                processed_line = self.process_line(line)
                if processed_line is not None:
                    block_content.append(processed_line)
            else:
                processed_line = self.process_line(line)
                if processed_line is not None:
                    processed_lines.append(processed_line)
        # Join lines and do a final pass to clean up any remaining inline tags
        result = '\n'.join(processed_lines)
        # Final cleanup: remove any remaining inline tags that weren't processed
        result = self.inline_tag_pattern.sub('', result)
        result = self.exclude_tag_pattern.sub('', result)
        # Remove empty highlights environments (no \item inside)
        result = re.sub(
            r'\\begin\{highlights\}\s*\\end\{highlights\}',
            '',
            result,
            flags=re.DOTALL
        )
        # Remove highlights environments that only contain whitespace/comments/newlines
        result = re.sub(
            r'\\begin\{highlights\}([\s%]*)\\end\{highlights\}',
            '',
            result,
            flags=re.DOTALL
        )
        # Remove highlights environments that contain only whitespace or comments (no \item)
        result = re.sub(
            r'\\begin\{highlights\}((?:\s|%.*|\n)*)\\end\{highlights\}',
            '',
            result,
            flags=re.DOTALL
        )
        return result
    
    def build_for_role(self, role: str) -> None:
        """Build resume for a specific role."""
        self.current_role = role
        print(f"\nBuilding resume for role: {role}")
        
        # Copy all source files to output directory
        for tex_file in self.source_dir.glob('*.tex'):
            output_file = self.output_dir / tex_file.name
            self.process_file(tex_file, output_file)
        
        # Copy style file
        style_file = self.source_dir.parent / 'templates' / 'resume-layout.sty'
        if style_file.exists():
            output_style = self.output_dir / 'resume-layout.sty'
            output_style.parent.mkdir(parents=True, exist_ok=True)
            with open(style_file, 'r', encoding='utf-8') as f:
                content = f.read()
            with open(output_style, 'w', encoding='utf-8') as f:
                f.write(content)
        
        # Create role definition file
        role_def_file = self.output_dir / 'role-def.tex'
        with open(role_def_file, 'w', encoding='utf-8') as f:
            f.write(f'\\def\\buildrole{{{role}}}\n')
            f.write(f'\\def\\includelocation{{{str(self.include_location).lower()}}}\n')
    
    def build_all(self) -> None:
        """Build resumes for all roles."""
        for role in self.roles:
            print(f"\nBuilding resume for role: {role}")
            self.current_role = role
            
            # Create role-specific output directory
            role_output_dir = self.output_dir / role
            role_output_dir.mkdir(parents=True, exist_ok=True)
            
            # Copy all source files to role-specific output directory
            for tex_file in self.source_dir.glob('*.tex'):
                output_file = role_output_dir / tex_file.name
                self.process_file(tex_file, output_file)
            
            # Copy style file
            style_file = self.source_dir.parent / 'templates' / 'resume-layout.sty'
            if style_file.exists():
                output_style = role_output_dir / 'resume-layout.sty'
                with open(style_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                with open(output_style, 'w', encoding='utf-8') as f:
                    f.write(content)
            
            # Create role definition file
            role_def_file = role_output_dir / 'role-def.tex'
            with open(role_def_file, 'w', encoding='utf-8') as f:
                f.write(f'\\def\\buildrole{{{role}}}\n')
                f.write(f'\\def\\includelocation{{{str(self.include_location).lower()}}}\n')


def main() -> None:
    """Main function to build role-based resumes from LaTeX source."""
    parser = argparse.ArgumentParser(description='Build role-based resumes from LaTeX source') # parser for command line arguments
    parser.add_argument('--source-dir', default='tex-files', help='Source directory containing LaTeX files') # source directory containing LaTeX files
    parser.add_argument('--output-dir', default='build', help='Output directory containing processed files') # output directory for processed files
    parser.add_argument('--roles', nargs='+', default=['qr', 'qd', 'tech', 'soleng'], 
                       help='List of roles to build') # pass a list of multiple roleS to build
    parser.add_argument('--role', help='Build for specific role only') # build for specific role only
    parser.add_argument('--include-location', action='store_true', 
                       help='Include location in header')
    
    args = parser.parse_args()
    
    # If --role is specified, override --roles to contain only that role
    if args.role:
        args.roles = [args.role]
    
    builder = ResumeBuilder(args.source_dir, args.output_dir, args.roles, args.include_location)
    
    if args.role:
        builder.build_for_role(args.role)
    else:
        builder.build_all()


if __name__ == '__main__':
    main() 