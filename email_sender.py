import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from markdown import markdown

def send_email_with_attachment(subject, body, from_email, to_email, markdown_result, file_paths):
    # Mailtrap SMTP credentials
    smtp_host = "smtp.mailtrap.io"  # Replace with your Mailtrap SMTP host
    smtp_port = 587                 # Common ports: 25, 2525, 587
    smtp_username = "15fec4d7e2f9c5" # Replace with your Mailtrap username
    smtp_password = "abd8d2d73ca664" # Replace with your Mailtrap password

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    
    email_content = markdown(markdown_result, extensions=['markdown.extensions.tables', 'markdown.extensions.extra', 'markdown.extensions.nl2br'])
    
    styled_html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    color: #333;
                    margin: 0;
                    padding: 0;
                    background-color: #f5f5f5;
                }}
                .email-container {{
                    max-width: 600px;
                    margin: 20px auto;
                    background-color: #fff;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                }}
                .logo {{
                    display: block;
                    margin: 0 auto 20px auto;
                    width: 150px;
                    height: auto;
                }}
                h3 {{
                    color: #2c3e50;
                    margin-top: 20px;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                }}
                th, td {{
                    border: 1px solid #ddd;
                    padding: 10px;
                    text-align: left;
                }}
                th {{
                    background-color: #f4f4f4;
                    color: #2c3e50;
                    font-weight: bold;
                }}
                td {{
                    background-color: #fff;
                }}
                tr:nth-child(odd) td {{
                    background-color: #f9f9f9;
                }}
                p, li {{
                    line-height: 1.6;
                    margin: 10px 0;
                }}
                ol {{
                    padding-left: 20px;
                }}
                .separator {{
                    margin: 20px 0;
                    border-top: 1px solid #ddd;
                    padding-top: 10px;
                    font-style: italic;
                    color: #666;
                }}
                .confidentiality {{
                    margin-top: 30px;
                    padding: 10px;
                    border-top: 2px solid #e74c3c;
                    font-size: 12px;
                    color: #e74c3c;
                    text-align: center;
                    font-style: italic;
                }}
            </style>
        </head>
        <body>
            <div class="email-container">
                <img src="https://careers.smartosc.com/wp-content/uploads/2021/12/logo-2023_update-removebg-preview.png" alt="Levi's Logo" class="logo">
                <h1>Smart Competitors Analysis</h1>
                {email_content}
                <div class="confidentiality">
                    <p>CONFIDENTIAL: This email contains proprietary information intended solely for the recipients listed. Unauthorized distribution or disclosure is prohibited.</p>
                </div>
            </div>
        </body>
        </html>
        """

    # Attach the email body
    msg.attach(MIMEText(styled_html, "html"))

   
    for file_path in file_paths:
        if os.path.exists(file_path):
            with open(file_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(file_path)}')
                msg.attach(part)
        else:
            print(f"File not found: {file_path}")
            return

    # Send the email via Mailtrap's SMTP server
    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()  # Enable TLS
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
            print("Email with attachment sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")