# SMTPServer

A lightweight Python SMTP server for receiving and parsing emails, with customizable callbacks for further processing. Useful for development, testing, or building custom mail processing pipelines.

---

## ✨ Features

- Minimal SMTP server implementation using raw sockets
- Supports core SMTP commands: `HELO`, `MAIL FROM`, `RCPT TO`, `DATA`, `QUIT`
- Parses raw email headers and multipart content (plain text & HTML)
- Built-in callback mechanism for custom email handling
- Logs all server activity for debugging and observability

---

## 📁 Project Structure

```
SMTPServer/
├── smtp_server.py      # Core SMTP server logic
├── email_parser.py     # Email header and body parser
└── example.py          # Example usage with console callback
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/SMTPServer.git
cd SMTPServer
```

### 2. Run the server

```bash
python example.py
```

The server will start on port `25` and listen for incoming SMTP connections. On receiving an email, it will parse it and print the details to the console.

---

## 🧠 How It Works

- `smtp_server.py`: Sets up a socket-based SMTP server. On receiving complete email data, it uses `EmailParser` to decode and structure the content.
- `email_parser.py`: Extracts common headers (`From`, `To`, `Subject`, etc.) and separates multipart content into plain text and HTML.
- `example.py`: Demonstrates how to instantiate the server and print parsed email details using a callback.

---

## 🛠️ Configuration

You can customize the server in `example.py`:

```python
server = SMTPServer(
    host='0.0.0.0',     # Change to '127.0.0.1' if you only want localhost access
    port=25,            # Make sure port 25 is available or use a different one
    email_callback=email_callback  # Your handler for incoming parsed emails
)
```

---

## 📦 Dependencies

- Standard Python 3 libraries only (no external packages required)

---

## 🧪 Example Output

```
Starting SMTP server...
Received new email:
From: Jane <jane@example.com>
To: John <john@example.com>
Subject: Hello!
Date: Sun, 13 Jul 2025 10:15:00 +0000
Message ID: abc123@example.com

Content:
Plain text version:
This is a test email sent to your SMTP server.
```

---

## 📜 License

MIT License. See `LICENSE` for more details.

---

## 🙌 Credits

Developed by Bastian Carou.
