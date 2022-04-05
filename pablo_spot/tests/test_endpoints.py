from unittest import TestCase, mock

from fastapi.testclient import TestClient
from fastapi import HTTPException, status
from app.main import app, Thumbnail, create_thumbnail

client = TestClient(app)

class TestEndpoints(TestCase):
    @mock.patch("workers.thumbnail.create.delay")
    def test_backend_main(self, mock_worker):
        tn = Thumbnail(
            url="https://jpeg.org/images/aic-home.jpg",
            filename="filefrombackendmain"
        )
        self.assertEqual(create_thumbnail(tn), tn)
        mock_worker.assert_called()

    @mock.patch("workers.thumbnail.create.delay")
    def test_create_thumbnail(self, mock_create):
        source_url = "https://jpeg.org/images/jpeg2000-home.jpg"
        response = client.post('/thumbnail/', json={"url": source_url})
        self.assertEqual(response. status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.json(), None)
        mock_create.assert_called()

        output = response.json()
        self.assertEqual(output["url"], source_url)
        self.assertNotEqual(output["filename"], None)

        # response = client.get(f"/static/{output['filename']}")
        # self.assertEqual(response.status_code, 200)


    def test_create_thumbnail_exceptions(self):
        tn = Thumbnail(url="bad url",
                       filename="some_new_file_name")
        self.assertRaises(
            HTTPException,
            create_thumbnail,
            tn
        )

        sourceurl = "https://www.google.com"
        response = client.post("/thumbnail/", json={"url": sourceurl})
        self.assertEqual(response.status_code, 500)



