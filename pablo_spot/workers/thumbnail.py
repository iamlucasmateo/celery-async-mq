from workers.config import app
from entities.thumbnail import Thumbnail

# This will set the function as a celery worker task
# we add self as an argument in this case because bind = True 
@app.task(bind=True, name="create_thumbnail")
def create(self, url, filename):
    thumbnail = Thumbnail(url, filename)
    thumbnail.create()