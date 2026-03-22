#!/usr/bin/env python3
"""Generate QR code PNG for the Grimasso Chinese parent guide."""

import io
import os
import qrcode
from qrcode.constants import ERROR_CORRECT_H

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, "grimasso-qr.png")

qr = qrcode.QRCode(
    version=None,
    error_correction=ERROR_CORRECT_H,
    box_size=10,
    border=2,
)
qr.add_data("https://apps.apple.com/us/app/grimasso/id6758241652")
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")
img.save(OUTPUT_PATH)
print(f"QR code saved → {OUTPUT_PATH}")
