from smtp_server import SMTPServer
from email_parser import ParsedEmail

def email_callback(parsed_email: ParsedEmail):
    """Example callback function to handle received emails."""
    print("\nReceived new email:")
    print(f"From: {parsed_email.headers.from_addr}")
    print(f"To: {parsed_email.headers.to_addr}")
    print(f"Subject: {parsed_email.headers.subject}")
    print(f"Date: {parsed_email.headers.date}")
    print(f"Message ID: {parsed_email.headers.message_id}")
    
    print("\nContent:")
    if parsed_email.content.text_plain:
        print("Plain text version:")
        print(parsed_email.content.text_plain)
    if parsed_email.content.text_html:
        print("\nHTML version:")
        print(parsed_email.content.text_html)
    print("-" * 50)

def main():
    # Create and start the SMTP server
    server = SMTPServer(
        host='0.0.0.0',  # Listen on all interfaces
        port=25,         # Standard SMTP port
        email_callback=email_callback
    )
    
    print("Starting SMTP server...")
    try:
        server.start()
    except KeyboardInterrupt:
        print("\nServer stopped by user")

if __name__ == "__main__":
    main() 