import qrcode

def generate_qr(uri: str):
    # Generate QR code
    img = qrcode.make(uri)
    # Save QR code to a file
    img.save("qrcode.png")
