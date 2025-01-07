import argparse
from PIL import Image
import math

def nearest_power_of_2(value):
    """Calculate the nearest power of 2 for a given value."""
    return 2 ** math.ceil(math.log2(value))

def resize_to_power_of_2(image):
    """Resize an image to the nearest power of 2 dimensions."""
    width, height = image.size
    new_width = nearest_power_of_2(width)
    new_height = nearest_power_of_2(height)
    return image.resize((new_width, new_height), Image.BICUBIC)

def slice_image(input_file, output_file, left, right, top, bottom, resize=False, compress_level=9):
    """
    Slices an image based on normalized coordinates and optionally resizes it.

    Args:
        input_file (str): Path to the input image file.
        output_file (str): Path to save the output image.
        left (float): Normalized left coordinate (0-1).
        right (float): Normalized right coordinate (0-1).
        top (float): Normalized top coordinate (0-1).
        bottom (float): Normalized bottom coordinate (0-1).
        resize (bool): Whether to resize the output to the nearest power of 2.
        compress_level (int): Compression level for saving PNG files (0-9).
    """
    # Open the image
    with Image.open(input_file) as img:
        print(f"Original image mode: {img.mode}, size: {img.size}")

        # Check for multiple frames (mipmap layers) in the BLP file
        try:
            if hasattr(img, "n_frames") and img.n_frames > 1:
                print(f"Image has {img.n_frames} frames (mipmap layers). Selecting the highest resolution layer.")
                img.seek(0)  # Go to the first (highest resolution) frame
        except EOFError:
            print("No additional frames found; using the default frame.")

        # Ensure the image is in RGBA mode
        if img.mode != "RGBA":
            img = img.convert("RGBA")
            print(f"Converted image mode to: {img.mode}")
        
        width, height = img.size

        # Convert normalized coordinates to pixel values
        left_px = int(left * width)
        right_px = int(right * width)
        top_px = int(top * height)
        bottom_px = int(bottom * height)

        # Crop the image
        cropped_img = img.crop((left_px, top_px, right_px, bottom_px))

        # Resize if needed
        if resize:
            cropped_img = resize_to_power_of_2(cropped_img)
        
        # Save the output image
        if output_file.endswith(".blp"):
            print("Saving as BLP format... (badly supported)")
            cropped_img = cropped_img.convert("P")
            cropped_img.save(output_file, blp_version="BLP2")
        else:
            # Save as PNG with compression level
            cropped_img.save(output_file, format="PNG", compress_level=compress_level)
        
        print(f"Output image saved to {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Slice an image and optionally resize to nearest power of 2.")
    parser.add_argument("input_file", help="Path to the input image file.")
    parser.add_argument("output_file", help="Path to save the output image file.")
    parser.add_argument("left", type=float, help="Normalized left coordinate (0-1).")
    parser.add_argument("right", type=float, help="Normalized right coordinate (0-1).")
    parser.add_argument("top", type=float, help="Normalized top coordinate (0-1).")
    parser.add_argument("bottom", type=float, help="Normalized bottom coordinate (0-1).")
    parser.add_argument("--resize", action="store_true", help="Resize the output image to the nearest power of 2.")
    parser.add_argument("--compress-level", type=int, default=9, help="Compression level for saving PNG files (0-9).")

    args = parser.parse_args()
    slice_image(args.input_file, args.output_file, args.left, args.right, args.top, args.bottom, args.resize, args.compress_level)

if __name__ == "__main__":
    main()