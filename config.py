import dotenv  # type: ignore
import os

dotenv.load_dotenv()

API_KEY = os.getenv("API_KEY")
AWS_ID = os.getenv("AWS_ID")
AWS_SECRET = os.getenv("AWS_SECRET")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
