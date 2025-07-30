import pyqrcode
import png
from pyqrcode import QRCode

s = "https://accounts.google.com/SignOutOptions?hl=en&continue=https://www.google.com/webhp%3Fauthuser%3D2&ec=GBRAmgQ"
url = pyqrcode.create(s)

url.png("myqr.png", scale = 8)
