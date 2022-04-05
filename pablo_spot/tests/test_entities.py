from unittest import TestCase
from pathlib import Path

from requests.models import MissingSchema
import pytest
from PIL import UnidentifiedImageError

from entities.thumbnail import Thumbnail

class TestEntities(TestCase):
    def test_entities(self):
        url = "http://personal.psu.edu/xqz5228/jpg.jpg"
        filename = "some_filename"
        thumbnail = Thumbnail(url, filename)
        self.assertEqual(thumbnail.url, url)
        self.assertEqual(thumbnail.filename, filename)

        thumbnail.create()
        path = Path(f"/tmp/static/{filename}")
        self.assertTrue(path.is_file())
    
    def test_thumbnail_exceptions(self):
        with pytest.raises(UnidentifiedImageError):
            url = "https://www.google.com"
            thumbnail = Thumbnail(url, "somefile")
            thumbnail.create()
        with pytest.raises(MissingSchema):
            url = "someurl"
            thumbnail = Thumbnail(url, "somefile")
            thumbnail.create()

