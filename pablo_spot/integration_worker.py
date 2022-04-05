from workers import thumbnail

filename="somefilenamefromtest"
thumbnail.create.delay("https://jpeg.org/images/jpegai-home.jpg", filename)