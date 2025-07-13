import socket
import logging
from typing import Optional, Tuple, Callable
from email_parser import EmailParser, ParsedEmail
import os
from datetime import datetime

class SMTPServer:
    def __init__(self, host: str = '0.0.0.0', port: int = 25, 
                 email_callback: Optional[Callable[[ParsedEmail], None]] = None):
        self.host = host
        self.port = port
        self.email_parser = EmailParser()
        self.email_callback = email_callback
        self._setup_logging()
    
    def _setup_logging(self):
        """Configure logging for the SMTP server."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('SMTPServer')
    
    def _handle_client(self, client_socket: socket.socket, addr: Tuple[str, int]):
        """Handle a single client connection."""
        self.logger.info(f"New connection from {addr}")
        client_socket.sendall(b"220 mail.example.com SMTP SimpleServer\r\n")
        
        data_buffer = b""
        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break
                
                data_buffer += data
                self.logger.debug(f"[{addr}] {data.decode(errors='ignore').strip()}")
                
                if data.startswith(b"HELO") or data.startswith(b"EHLO"):
                    client_socket.sendall(b"250 Hello\r\n")
                elif data.startswith(b"MAIL FROM"):
                    client_socket.sendall(b"250 OK\r\n")
                elif data.startswith(b"RCPT TO"):
                    client_socket.sendall(b"250 OK\r\n")
                elif data.startswith(b"DATA"):
                    client_socket.sendall(b"354 End with <CR><LF>.<CR><LF>\r\n")
                elif b"\r\n.\r\n" in data:
                    self._process_email(data_buffer, addr)
                    client_socket.sendall(b"250 Message accepted\r\n")
                    data_buffer = b""
                elif data.startswith(b"QUIT"):
                    client_socket.sendall(b"221 Bye\r\n")
                    break
                else:
                    client_socket.sendall(b"250 OK\r\n")
            
            except Exception as e:
                self.logger.error(f"Error handling client {addr}: {str(e)}")
                break
        
        client_socket.close()
        self.logger.info(f"Disconnected {addr}")
    
    def _process_email(self, raw_email: bytes, addr: Tuple[str, int]):
        """Process received email and trigger callback if set."""
        try:
            parsed_email = self.email_parser.parse(raw_email)
            self.logger.info(f"Received email from {parsed_email.headers.from_addr} to {parsed_email.headers.to_addr}")
            
            if self.email_callback:
                self.email_callback(parsed_email)
        
        except Exception as e:
            self.logger.error(f"Error processing email from {addr}: {str(e)}")
    
    def start(self):
        """Start the SMTP server."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind((self.host, self.port))
            server.listen(5)
            self.logger.info(f"SMTP Server listening on {self.host}:{self.port}")
            
            while True:
                try:
                    client_socket, addr = server.accept()
                    self._handle_client(client_socket, addr)
                except KeyboardInterrupt:
                    self.logger.info("Server shutting down...")
                    break
                except Exception as e:
                    self.logger.error(f"Server error: {str(e)}")
                    continue 