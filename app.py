from flask import Flask, render_template, request, send_file, jsonify
from flask_cors import CORS
import fitz  # PyMuPDF
from PIL import Image, ImageOps
import io
import os
from werkzeug.utils import secure_filename
import tempfile
from config import Config
from payment import (
    init_database,
    create_checkout_session,
    verify_premium_token,
    handle_stripe_webhook,
    get_pricing_info
)

app = Flask(__name__)
CORS(app)

# Configuration
app.secret_key = Config.SECRET_KEY
app.config['MAX_CONTENT_LENGTH'] = Config.MAX_CONTENT_LENGTH
ALLOWED_EXTENSIONS = {'pdf'}

# Initialize database
init_database()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def invert_pdf(input_file_bytes):
    """
    Inverts colors in a PDF file.
    Black becomes White, White becomes Black.
    """
    try:
        # Open the original PDF from bytes
        pdf_doc = fitz.open(stream=input_file_bytes, filetype="pdf")
        new_pdf = fitz.open()

        total_pages = len(pdf_doc)
        
        for page_num in range(total_pages):
            page = pdf_doc.load_page(page_num)

            # Render page to a high-res image (300 DPI for clarity)
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))

            # Convert to PIL Image
            img = Image.open(io.BytesIO(pix.tobytes()))

            # Invert the colors
            inverted_img = ImageOps.invert(img.convert("RGB"))

            # Convert back to PDF page
            img_byte_arr = io.BytesIO()
            inverted_img.save(img_byte_arr, format='PDF')

            # Append to the new PDF
            with fitz.open("pdf", img_byte_arr.getvalue()) as img_pdf:
                new_pdf.insert_pdf(img_pdf)

        # Save to bytes
        output_bytes = io.BytesIO()
        new_pdf.save(output_bytes)
        new_pdf.close()
        pdf_doc.close()
        
        output_bytes.seek(0)
        return output_bytes
    
    except Exception as e:
        raise Exception(f"Error processing PDF: {str(e)}")

@app.route('/')
def index():
    # Check if user has premium
    token = request.cookies.get('premium_token')
    is_premium = verify_premium_token(token) if token else False
    
    return render_template(
        'index.html',
        adsense_client_id=Config.ADSENSE_CLIENT_ID,
        stripe_publishable_key=Config.STRIPE_PUBLISHABLE_KEY,
        is_premium=is_premium
    )

@app.route('/invert', methods=['POST'])
def invert():
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Check if file is allowed
        if not allowed_file(file.filename):
            return jsonify({'error': 'Only PDF files are allowed'}), 400
        
        # Read file content
        file_content = file.read()
        
        # Process the PDF
        inverted_pdf = invert_pdf(file_content)
        
        # Generate output filename
        original_filename = secure_filename(file.filename)
        output_filename = f"inverted_{original_filename}"
        
        # Send the inverted PDF
        return send_file(
            inverted_pdf,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=output_filename
        )
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'}), 200

@app.route('/check-premium', methods=['POST'])
def check_premium():
    """Check if a premium token is valid"""
    try:
        data = request.get_json()
        token = data.get('token')
        
        is_premium = verify_premium_token(token)
        return jsonify({'is_premium': is_premium})
    except Exception as e:
        return jsonify({'is_premium': False}), 400

@app.route('/create-checkout', methods=['POST'])
def create_checkout():
    """Create a Stripe checkout session"""
    try:
        data = request.get_json()
        plan = data.get('plan', 'lifetime')
        
        # Get price ID for the selected plan
        pricing = get_pricing_info()
        price_id = pricing.get(plan, {}).get('price_id')
        
        if not price_id:
            return jsonify({'error': 'Invalid plan selected'}), 400
        
        # Create checkout session
        session = create_checkout_session(price_id, plan)
        
        if not session:
            return jsonify({'error': 'Failed to create checkout session'}), 500
        
        return jsonify(session)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/stripe-webhook', methods=['POST'])
def stripe_webhook():
    """Handle Stripe webhook events"""
    payload = request.get_data()
    sig_header = request.headers.get('Stripe-Signature')
    
    try:
        result = handle_stripe_webhook(payload, sig_header)
        return jsonify(result[0]), result[1]
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/payment-success', methods=['GET'])
def payment_success():
    """Handle successful payment and return premium token"""
    try:
        session_id = request.args.get('session_id')
        
        if not session_id:
            return jsonify({'error': 'No session ID provided'}), 400
        
        # In a real implementation, you would:
        # 1. Verify the session with Stripe
        # 2. Get the token from your database based on session metadata
        # For now, we'll return a placeholder
        # This should be properly implemented with session verification
        
        return jsonify({
            'success': True,
            'token': 'temp_token_replace_with_real_implementation'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
