import segno

class QRCode:
    def __init__(self, payload: str):
        self.payload = payload
        self.qrcode = None
        self.make_qrcode()
    
    def make_qrcode(self):
        """Generates the QR Code from the given payload
        """
        self.qrcode = segno.make_qr(self.payload)
        
    
    def save_qrcode(self, path: str, scale: int = 5, border: int = 0):
        """Saves the QR Code on the given path.

        Args:
            path (str): the path to save the QR Code.
            scale (int, optional): the scale of the QR Code. Defaults to 5.
            border (int, optional): the border size of the QR Code. Defaults to 0
        """
        self.qrcode.save(path, scale=scale, border=border)