import os
import requests
from pathlib import Path


def download_image(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"Downloaded {filename}")
    else:
        print(f"Failed to download {filename}")


def main():
    # Create images directory if it doesn't exist
    images_dir = Path("static/images")
    images_dir.mkdir(parents=True, exist_ok=True)

    # Image URLs
    images = {
        # About page images
        "about-hero.jpg": "https://images.unsplash.com/photo-1497366216548-37526070297c",
        "team-1.jpg": "https://images.unsplash.com/photo-1560250097-0b93528c311a",
        "team-2.jpg": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2",
        "team-3.jpg": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e",
        "team-4.jpg": "https://images.unsplash.com/photo-1580489944761-15a19d654956",
        # Landing page slider images
        "slider-1.jpg": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c",
        "slider-2.jpg": "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c",
        "slider-3.jpg": "https://images.unsplash.com/photo-1600566753086-00f18fb6b3ea",
        # Featured properties images
        "property-1.jpg": "https://images.unsplash.com/photo-1600585154526-990dced4db0d",
        "property-2.jpg": "https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3",
        "property-3.jpg": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c",
        # Background images
        "hero-bg.jpg": "https://images.unsplash.com/photo-1560518883-ce09059eeffa",
        "pattern-bg.jpg": "https://images.unsplash.com/photo-1600607687920-4e2a09cf159d",
    }

    # Download images
    for filename, url in images.items():
        filepath = images_dir / filename
        download_image(url, filepath)


if __name__ == "__main__":
    main()
