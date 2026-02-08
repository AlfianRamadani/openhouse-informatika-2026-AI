import os
import cloudinary
import cloudinary.uploader
import qrcode
from io import BytesIO
from PIL import Image
from datetime import datetime

# Konfigurasi Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_NAME") or os.getenv("CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY") or os.getenv("API_KEY"),
    api_secret=os.getenv("CLOUDINARY_SECRET_KEY") or os.getenv("API_SECRET")
)

def upload_image_to_cloudinary(image_pil, style_name="unknown"):
    """
    Upload image ke Cloudinary dan return public URL
    
    Args:
        image_pil: PIL Image object
        style_name: nama style yang digunakan (anime/ghibli/zootopia)
    
    Returns:
        str: Public URL dari image yang diupload
    """
    try:
        # Convert PIL Image ke bytes
        buf = BytesIO()
        image_pil.save(buf, format='PNG')
        buf.seek(0)
        
        # Generate unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        public_id = f"openhouse_informatika_2026/{style_name}_{timestamp}"
        
        # Upload ke Cloudinary
        response = cloudinary.uploader.upload(
            buf,
            public_id=public_id,
            folder="openhouse_informatika_2026",
            resource_type="image",
            overwrite=True,
            transformation=[
                {'quality': 'auto:best'},
                {'fetch_format': 'auto'}
            ]
        )
        
        public_url = response['secure_url']
        print(f"Image uploaded successfully: {public_url}")
        
        return public_url
        
    except Exception as e:
        print(f"Error uploading to Cloudinary: {str(e)}")
        raise e


def generate_qr(public_url):
    """
    Generate QR Code dari public URL
    
    Args:
        public_url: URL publik dari Cloudinary
    
    Returns:
        BytesIO: QR Code image dalam format BytesIO
    """
    try:
        # Generate QR Code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        
        qr.add_data(public_url)
        qr.make(fit=True)
        
        # Create image
        qr_image = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to BytesIO
        qr_buf = BytesIO()
        qr_image.save(qr_buf, format='PNG')
        qr_buf.seek(0)
        
        print(f"QR Code generated for URL: {public_url}")
        
        return qr_buf
        
    except Exception as e:
        print(f"Error generating QR Code: {str(e)}")
        raise e


def generate_qr_pil(public_url):
    """
    Generate QR Code dan return sebagai PIL Image
    
    Args:
        public_url: URL publik dari Cloudinary
    
    Returns:
        PIL.Image: QR Code sebagai PIL Image
    """
    qr_buf = generate_qr(public_url)
    qr_image = Image.open(qr_buf)
    return qr_image


def upload_and_generate_qr(image_pil, style_name="unknown"):
    """
    Upload image dan generate QR Code dalam satu fungsi
    
    Args:
        image_pil: PIL Image object
        style_name: nama style yang digunakan
    
    Returns:
        tuple: (public_url, qr_code_pil)
    """
    # Upload image
    public_url = upload_image_to_cloudinary(image_pil, style_name)
    
    # Generate QR Code
    qr_code = generate_qr_pil(public_url)
    
    return public_url, qr_code
