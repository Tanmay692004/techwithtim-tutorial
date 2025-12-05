from dotenv import load_dotenv
from imagekitio import ImageKit
import os

load_dotenv()
imagekit = ImageKit(
    private_key = os.getenv("imagekit_private_key"),
    public_key = os.getenv("imagekit_public_key"),
    url_endpoint= os.getenv("imagekit_url_endpoint")
)