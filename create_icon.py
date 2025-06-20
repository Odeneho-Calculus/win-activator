#!/usr/bin/env python3
"""
Simple icon creator for Windows Activator Pro
Creates a basic icon using PIL (Pillow)
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    import os

    def create_icon():
        """Create a simple application icon"""
        # Create a 256x256 image with transparent background
        size = 256
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Draw background circle with gradient effect
        center = size // 2
        radius = center - 20

        # Create gradient background
        for i in range(radius):
            alpha = int(255 * (1 - i / radius))
            color = (70, 130, 180, alpha)  # Steel blue with varying alpha
            draw.ellipse([center - radius + i, center - radius + i,
                         center + radius - i, center + radius - i],
                        fill=color)

        # Draw main circle
        draw.ellipse([center - radius, center - radius,
                     center + radius, center + radius],
                    fill=(70, 130, 180, 255), outline=(25, 25, 112, 255), width=4)

        # Draw Windows logo-like squares
        square_size = 30
        gap = 8
        start_x = center - square_size - gap // 2
        start_y = center - square_size - gap // 2

        # Top-left square (red)
        draw.rectangle([start_x, start_y, start_x + square_size, start_y + square_size],
                      fill=(220, 20, 60, 255))

        # Top-right square (green)
        draw.rectangle([start_x + square_size + gap, start_y,
                       start_x + 2 * square_size + gap, start_y + square_size],
                      fill=(34, 139, 34, 255))

        # Bottom-left square (blue)
        draw.rectangle([start_x, start_y + square_size + gap,
                       start_x + square_size, start_y + 2 * square_size + gap],
                      fill=(30, 144, 255, 255))

        # Bottom-right square (yellow)
        draw.rectangle([start_x + square_size + gap, start_y + square_size + gap,
                       start_x + 2 * square_size + gap, start_y + 2 * square_size + gap],
                      fill=(255, 215, 0, 255))

        # Add activation symbol (checkmark)
        check_points = [
            (center - 15, center + 20),
            (center - 5, center + 30),
            (center + 15, center + 10)
        ]
        draw.line(check_points, fill=(255, 255, 255, 255), width=6)

        # Save as ICO file
        # Convert to different sizes for ICO format
        sizes = [16, 32, 48, 64, 128, 256]
        images = []

        for size in sizes:
            resized = img.resize((size, size), Image.Resampling.LANCZOS)
            images.append(resized)

        # Save as ICO
        img.save('icon.ico', format='ICO', sizes=[(s, s) for s in sizes])
        print("✅ Icon created successfully: icon.ico")

        # Also save as PNG for other uses
        img.save('icon.png', format='PNG')
        print("✅ PNG version created: icon.png")

        return True

    if __name__ == "__main__":
        print("🎨 Creating application icon...")
        if create_icon():
            print("🎉 Icon creation completed!")
        else:
            print("❌ Icon creation failed!")

except ImportError:
    print("📦 PIL (Pillow) not found. Installing...")
    import subprocess
    import sys

    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
        print("✅ Pillow installed successfully!")
        print("🔄 Please run this script again to create the icon.")
    except subprocess.CalledProcessError:
        print("❌ Failed to install Pillow.")
        print("💡 You can manually install it with: pip install Pillow")
        print("🎨 Or create your own icon.ico file manually.")

except Exception as e:
    print(f"❌ Error creating icon: {e}")
    print("🎨 You can create your own icon.ico file manually.")