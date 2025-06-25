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
    def __init__(self, source_dir: str, output_dir: str, roles: List[str], include_location: bool = False):
        self.source_dir = Path(source_dir)
        self.output_dir = Path(output_dir)
        self.roles = set(roles)
        self.current_role = None
        self.include_location = include_location
        
        # Tag patterns
        self.start_tag_pattern = re.compile(r'\\begin\{rolecontent\}\{([^}]+)\}')
        self.end_tag_pattern = re.compile(r'\\end\{rolecontent\}')
        self.inline_tag_pattern = re.compile(r'\\rolecontent\{([^}]+)\}\{([^}]*)\}') # pattern matches \rolecontent{roles}{content}
        
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
        # Check for inline rolecontent tags
        inline_match = self.inline_tag_pattern.search(line)
        if inline_match:
            roles_str, content = inline_match.groups()
            content_roles = self.parse_role_list(roles_str)
            if self.should_include_content(content_roles):
                # Replace the tag with just the content
                return self.inline_tag_pattern.sub(lambda m: content, line)
            else:
                # Remove the entire line if content shouldn't be included
                return None
        
        return line
    
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
    
    def process_content(self, content: str) -> str:
        """Process content with role-based filtering."""
        lines = content.split('\n')
        processed_lines = []
        in_role_block = False
        current_block_roles = set()
        block_content = []
        
        for line in lines:
            # Check for start of rolecontent block
            start_match = self.start_tag_pattern.search(line)
            if start_match:
                in_role_block = True
                roles_str = start_match.group(1)
                current_block_roles = self.parse_role_list(roles_str)
                # Don't include the start tag line
                continue
            
            # Check for end of rolecontent block
            if self.end_tag_pattern.search(line):
                in_role_block = False
                # Include block content if it should be included
                if self.should_include_content(current_block_roles):
                    processed_lines.extend(block_content)
                block_content = []
                current_block_roles = set()
                # Don't include the end tag line
                continue
            
            # If we're in a role block, collect content
            if in_role_block:
                block_content.append(line)
            else:
                # Process regular line (check for inline tags)
                processed_line = self.process_line(line)
                if processed_line is not None:
                    processed_lines.append(processed_line)
        
        return '\n'.join(processed_lines)
    
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


def main():
    parser = argparse.ArgumentParser(description='Build role-based resumes from LaTeX source')
    parser.add_argument('--source-dir', default='tex-files', help='Source directory with LaTeX files')
    parser.add_argument('--output-dir', default='build', help='Output directory for processed files')
    parser.add_argument('--roles', nargs='+', default=['qr', 'qd', 'tech', 'soleng'], 
                       help='List of roles to build')
    parser.add_argument('--role', help='Build for specific role only')
    parser.add_argument('--include-location', action='store_true', 
                       help='Include location in header')
    
    args = parser.parse_args()
    
    builder = ResumeBuilder(args.source_dir, args.output_dir, args.roles, args.include_location)
    
    if args.role:
        if args.role not in args.roles:
            print(f"Error: Role '{args.role}' not in allowed roles: {args.roles}")
            sys.exit(1)
        builder.build_for_role(args.role)
    else:
        builder.build_all()


if __name__ == '__main__':
    main() 