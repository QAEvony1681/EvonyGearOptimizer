"""
make_icon.py -- Convert icon.svg to icon.ico for PyInstaller and Inno Setup.

Run this ONCE from the evony_tool folder:
    py -3.11 make_icon.py

Requirements (pure Python, no Cairo/GTK needed):
    py -3.11 -m pip install svglib reportlab Pillow

Output:
    icon.ico  (multi-resolution: 16, 32, 48, 64, 128, 256 px)
"""

import sys, os, io

def make_icon():
    # Install dependencies if missing
    for pkg in ('svglib', 'reportlab', 'Pillow'):
        try:
            __import__(pkg.lower().replace('-', '_'))
        except ImportError:
            print(f'Installing {pkg}...')
            os.system(f'"{sys.executable}" -m pip install {pkg}')

    from svglib.svglib import svg2rlg
    from reportlab.graphics import renderPM
    from PIL import Image

    script_dir = os.path.dirname(os.path.abspath(__file__))
    svg_path   = os.path.join(script_dir, 'icon.svg')
    ico_path   = os.path.join(script_dir, 'icon.ico')

    if not os.path.exists(svg_path):
        print(f'ERROR: icon.svg not found at {svg_path}')
        sys.exit(1)

    # Get original SVG dimensions
    ref = svg2rlg(svg_path)
    orig_w, orig_h = ref.width, ref.height

    sizes = [16, 32, 48, 64, 128, 256]
    images = []

    print('Converting icon.svg to icon.ico...')
    for size in sizes:
        drawing = svg2rlg(svg_path)
        scale = size / max(orig_w, orig_h)
        drawing.width  = orig_w * scale
        drawing.height = orig_h * scale
        drawing.transform = (scale, 0, 0, scale, 0, 0)
        png_data = renderPM.drawToString(drawing, fmt='PNG', dpi=72)
        img = Image.open(io.BytesIO(png_data)).convert('RGBA')
        images.append(img)
        print(f'  Rendered {size}x{size}')

    images[-1].save(
        ico_path,
        format='ICO',
        sizes=[(i.width, i.height) for i in images],
        append_images=images[:-1]
    )

    print(f'\nSuccess! icon.ico saved ({os.path.getsize(ico_path):,} bytes)')
    print('\nNext steps:')
    print('  1. PyInstaller:  py -3.11 -m PyInstaller evony_tool.spec --clean')
    print('  2. Inno Setup:   open evony_installer.iss and compile')

if __name__ == '__main__':
    make_icon()
