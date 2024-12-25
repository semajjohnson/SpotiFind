from PIL import Image
import requests
from io import BytesIO
import matplotlib.pyplot as plt

# Function to create a collage
def create_collage(image_urls, collage_name="assets/top_tracks_collage.jpg", size=(500, 500)):
    images = []
    for url in image_urls:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        images.append(img)

    # Create a blank canvas for the collage
    collage = Image.new("RGB", size, "white")

    # Define grid layout (e.g., 4x4 for 16 album covers)
    grid_size = (4, 4)
    img_width = size[0] // grid_size[0]
    img_height = size[1] // grid_size[1]

    for i, img in enumerate(images[:grid_size[0] * grid_size[1]]):
        img = img.resize((img_width, img_height))
        x = (i % grid_size[0]) * img_width
        y = (i // grid_size[0]) * img_height
        collage.paste(img, (x, y))

    collage.save(collage_name)
    print(f"Collage saved as {collage_name}")

# Function to create a genre pie chart
def create_genre_pie_chart(genres, file_name="assets/top_genres_pie_chart.png"):
    genre_counts = {}
    for genre in genres:
        genre_counts[genre] = genre_counts.get(genre, 0) + 1

    labels = list(genre_counts.keys())
    sizes = list(genre_counts.values())

    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140)
    plt.title("Top Genres")
    plt.savefig(file_name)
    plt.show()
    print(f"Pie chart saved as {file_name}")
