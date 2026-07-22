import os
from dotenv import load_dotenv
load_dotenv()
key = os.environ.get('GOOGLE_API_KEY')
print(repr(key))