from PIL import Image, ImageDraw, ImageFont

# Function to create an image representation of the script


def create_script_image(script_text, output_path="script_image.png"):
    font_size = 20
    padding = 10
    line_spacing = 5
    image_width = 1200
    background_color = (255, 255, 255)
    text_color = (0, 0, 0)

    try:
        font = ImageFont.truetype("DejaVuSansMono.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    lines = script_text.splitlines()
    image_height = padding * 2 + (font_size + line_spacing) * len(lines)
    img = Image.new("RGB", (image_width, image_height), background_color)
    draw = ImageDraw.Draw(img)

    y = padding
    for line in lines:
        draw.text((padding, y), line, fill=text_color, font=font)
        y += font_size + line_spacing

    img.save(output_path)
    return output_path


# Read your script
with open("Skills.py", "r") as script_file:
    script_content = script_file.read()

# Generate the image
output_image_path = create_script_image(
    script_content, "Skills_Script_Image.png")
print(f"Image saved to {output_image_path}")
