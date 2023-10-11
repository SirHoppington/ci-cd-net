from waitress import serve
from app import create_app
import os
from dotenv import load_dotenv

load_dotenv()

print(f'ENVIRONMENT: {os.environ["ENVIRONMENT"]}')
try:
    flask_app = create_app(os.environ["ENVIRONMENT"])
    serve(flask_app,port=os.environ["PORT"])
except Exception as err:
    print(f"Failed to start app: {err}")
