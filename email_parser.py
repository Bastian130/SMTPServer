import re
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class EmailHeader:
    from_addr: str
    to_addr: str
    subject: str
    date: str
    message_id: str
    content_type: str
    mime_version: str

@dataclass
class EmailContent:
    text_plain: Optional[str] = None
    text_html: Optional[str] = None

@dataclass
class ParsedEmail:
    headers: EmailHeader
    content: EmailContent
    raw_headers: Dict[str, str]

class EmailParser:
    def __init__(self):
        self.header_patterns = {
            'from': re.compile(r'^From:\s*([^<\r\n]*<[^>]+>|\S+@\S+)\s*$', re.IGNORECASE | re.MULTILINE),
            'to': re.compile(r'^To:\s*([^<\r\n]*<[^>]+>|\S+@\S+)\s*$', re.IGNORECASE | re.MULTILINE),
            'subject': re.compile(r'^Subject:\s*([^\r\n]+)', re.IGNORECASE | re.MULTILINE),
            'date': re.compile(r'^Date:\s*([^\r\n]+)', re.IGNORECASE | re.MULTILINE),
            'message_id': re.compile(r'^Message-ID:\s*<([^>]+)>', re.IGNORECASE | re.MULTILINE),
            'content_type': re.compile(r'^Content-Type:\s*([^;\r\n]+)', re.IGNORECASE | re.MULTILINE),
            'mime_version': re.compile(r'^MIME-Version:\s*([^\r\n]+)', re.IGNORECASE | re.MULTILINE)
        }
        
    def _extract_header(self, data: str, pattern: re.Pattern) -> str:
        match = pattern.search(data)
        if not match:
            return ""
        
        # For message ID, we want the content between < >
        if pattern == self.header_patterns['message_id']:
            return match.group(1).strip()
        
        # For other headers, we want the full match
        return match.group(1).strip()

    def _parse_headers(self, data: str) -> Dict[str, str]:
        headers = {}
        for key, pattern in self.header_patterns.items():
            headers[key] = self._extract_header(data, pattern)
        return headers

    def _parse_content(self, data: str, boundary: str) -> EmailContent:
        content = EmailContent()
        
        # Split the content into parts using the boundary
        parts = data.split(f'--{boundary}')
        
        for part in parts:
            if not part.strip():
                continue
                
            # Extract content type and content
            content_type_match = re.search(r'Content-Type:\s*([^;\r\n]+)', part, re.IGNORECASE)
            if not content_type_match:
                continue
                
            content_type = content_type_match.group(1).strip()
            
            # Find the actual content (after the headers)
            content_start = part.find('\r\n\r\n')
            if content_start == -1:
                continue
                
            part_content = part[content_start:].strip()
            
            if content_type == 'text/plain':
                content.text_plain = part_content
            elif content_type == 'text/html':
                content.text_html = part_content
                
        return content

    def parse(self, raw_email: bytes) -> ParsedEmail:
        email_str = raw_email.decode('utf-8', errors='ignore')
        
        # Extract boundary if it's a multipart message
        boundary_match = re.search(r'boundary="([^"]+)"', email_str)
        boundary = boundary_match.group(1) if boundary_match else None
        
        # Parse headers
        headers = self._parse_headers(email_str)
        
        # Create EmailHeader object
        email_header = EmailHeader(
            from_addr=headers['from'],
            to_addr=headers['to'],
            subject=headers['subject'],
            date=headers['date'],
            message_id=headers['message_id'],
            content_type=headers['content_type'],
            mime_version=headers['mime_version']
        )
        
        # Parse content
        content = self._parse_content(email_str, boundary) if boundary else EmailContent(
            text_plain=email_str.split('\r\n\r\n', 1)[1] if '\r\n\r\n' in email_str else ""
        )
        
        return ParsedEmail(
            headers=email_header,
            content=content,
            raw_headers=headers
        ) 