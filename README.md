# PDF Inverter - Deployment Guide

A modern web application that inverts PDF colors for comfortable dark mode reading.

![PDF Inverter](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## Features

- ⚡ **Lightning Fast**: Process PDFs in seconds
- 🎨 **High Quality**: Maintains 300 DPI resolution
- 🔒 **Secure**: Files are never stored on the server
- 📱 **Responsive**: Works on all devices
- ✨ **Modern UI**: Beautiful dark theme with smooth animations

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **PDF Processing**: PyMuPDF (fitz) + Pillow (PIL)
- **Styling**: Custom CSS with modern design principles

## Local Development

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd "c:\Users\masud\OneDrive\Documents\MY Project\PDF_INVERT"
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # source venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

## Deployment to Hostinger

### Option 1: Shared Hosting with Python Support

1. **Check Python Support**: Ensure your Hostinger plan supports Python applications
2. **Upload Files**: Use FTP/SFTP to upload all project files
3. **Install Dependencies**: SSH into your server and run:
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure WSGI**: Create a `passenger_wsgi.py` file:
   ```python
   from app import app as application
   ```
5. **Set Python Version**: Use Hostinger control panel to set Python 3.8+

### Option 2: VPS Hosting (Recommended for Python Apps)

1. **Connect to VPS via SSH**

2. **Install System Dependencies**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv nginx
   ```

3. **Clone/Upload Your Project**
   ```bash
   cd /var/www
   mkdir pdf-inverter
   # Upload your files here
   ```

4. **Set up Virtual Environment**
   ```bash
   cd /var/www/pdf-inverter
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

5. **Install Gunicorn** (Production WSGI Server)
   ```bash
   pip install gunicorn
   ```

6. **Create Systemd Service** (`/etc/systemd/system/pdfinverter.service`)
   ```ini
   [Unit]
   Description=PDF Inverter Flask App
   After=network.target

   [Service]
   User=www-data
   WorkingDirectory=/var/www/pdf-inverter
   Environment="PATH=/var/www/pdf-inverter/venv/bin"
   ExecStart=/var/www/pdf-inverter/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:5000 app:app

   [Install]
   WantedBy=multi-user.target
   ```

7. **Configure Nginx** (`/etc/nginx/sites-available/pdfinverter`)
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;

       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }

       location /static {
           alias /var/www/pdf-inverter/static;
       }
   }
   ```

8. **Enable and Start Services**
   ```bash
   sudo systemctl enable pdfinverter
   sudo systemctl start pdfinverter
   sudo systemctl enable nginx
   sudo systemctl restart nginx
   ```

9. **Configure SSL with Let's Encrypt** (Optional but Recommended)
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d yourdomain.com
   ```

### Domain Configuration

1. **Point Your Domain**: In your domain registrar (Hostinger), point your domain to your server's IP
2. **DNS Settings**: Add an A record pointing to your server IP
3. **Wait for Propagation**: DNS changes can take 24-48 hours

## Project Structure

```
PDF_INVERT/
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/
│   └── index.html        # Main HTML template
└── static/
    ├── css/
    │   └── style.css     # Styles
    └── js/
        └── main.js       # JavaScript logic
```

## API Endpoints

- `GET /` - Main application page
- `POST /invert` - Upload and invert PDF
- `GET /health` - Health check endpoint

## Troubleshooting

### Issue: "ModuleNotFoundError"
**Solution**: Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Issue: "Permission Denied" on VPS
**Solution**: Check file permissions:
```bash
sudo chown -R www-data:www-data /var/www/pdf-inverter
```

### Issue: Large PDFs timeout
**Solution**: Increase timeout in Nginx config:
```nginx
proxy_read_timeout 300;
proxy_connect_timeout 300;
```

## Performance Tips

- For large PDFs, consider implementing queue-based processing
- Add Redis caching for frequently inverted PDFs
- Use CDN for static assets
- Enable gzip compression in Nginx

## Security Considerations

- File size limits are enforced (50MB max)
- Only PDF files are accepted
- Files are processed in memory and never stored
- CORS is configured appropriately

## License

MIT License - feel free to use this project for personal or commercial purposes.

## Support

For issues or questions, please check the troubleshooting section or contact your hosting provider's support team.

---

**Made with ❤️ for better reading experiences**
