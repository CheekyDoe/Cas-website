Put your photos and videos in this folder, then list them in works.json.

Tips
- Photos: JPG, around 2000 px on the long side, under 1 MB each loads fast.
- Videos: MP4 (H.264), short clips under 20 MB. Longer reels are better on YouTube.
- Use simple file names with no spaces, e.g. pitt-town-acreage.jpg

Example works.json with two items:

[
  {
    "file": "images/pitt-town-acreage.jpg",
    "title": "Riverside acreage",
    "place": "Pitt Town",
    "category": "Real estate",
    "wide": true,
    "hero": true
  },
  {
    "file": "images/windsor-flythrough.mp4",
    "title": "Flythrough reel",
    "place": "Windsor",
    "category": "Video"
  }
]

Fields
- file      (required) path to the photo or video
- title     shown on the tile
- place     suburb, shown next to the category
- category  one of: Real estate, Construction, Landscape, Video
- wide      true makes it a wide tile on the home page
- hero      true uses this photo as the big background at the top (pick one)

The first 6 items show on the home page. All of them show in the full gallery.
Until works.json has at least one item, the site shows drawn preview tiles.
