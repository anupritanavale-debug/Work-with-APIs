import time
from PIL import Image, ImageEnhance, ImageFilter
from huggingface_hub import InferenceClient
from config import HF_API_KEY


MODEL = "black-forest-labs/FLUX.1-schnell"


# Create Hugging Face client
client = InferenceClient(
    api_key=HF_API_KEY,
    provider="auto"
)


def generate_image_from_text(prompt):
    """Generate an image from a text prompt."""

    try:
        image = client.text_to_image(
            prompt=prompt,
            model=MODEL
        )

        return image.convert("RGB")

    except Exception as e:
        raise Exception(f"Image generation failed: {e}")


def post_process_image(image):
    """Apply brightness, contrast and blur effects."""

    image = ImageEnhance.Brightness(image).enhance(1.3)

    image = ImageEnhance.Contrast(image).enhance(1.4)

    image = image.filter(
        ImageFilter.GaussianBlur(radius=2)
    )

    return image


def main():

    print("Welcome to the Post-Processing Magic Workshop!")
    print("This program generates an image from text and applies")
    print("post-processing effects.")
    print("Type 'exit' to quit.\n")

    while True:

        user_input = input(
            "Enter a description for the image "
            "(or 'exit' to quit):\n"
        )

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        try:

            print("\nGenerating image...")

            image = generate_image_from_text(user_input)
            image.show()

            print("Applying post-processing effects...\n")

            processed_image = post_process_image(image)

            processed_image.show()

            save_option = input(
                "Do you want to save the processed image? (yes/no): "
            ).strip().lower()

            if save_option == "yes":

                file_name = input(
                    "Enter a name for the image file "
                    "(without extension): "
                ).strip()

                processed_image.save(
                    f"{file_name}.png"
                )

                print(
                    f"Image saved as {file_name}.png\n"
                )

            print("-" * 80)
            print()

        except Exception as e:

            print(f"An error occurred: {e}\n")


if __name__ == "__main__":
    main()