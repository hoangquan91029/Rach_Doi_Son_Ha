"""Rasterize authored whole-clothed SVG guides; never edits source character PNGs."""
import hashlib
import json
import pathlib
import sys

import cairo
import gi
from PIL import Image, ImageDraw

gi.require_version("Rsvg", "2.0")
from gi.repository import Rsvg


def render(directory):
    directory = pathlib.Path(directory).resolve()
    landmarks = json.loads((directory / "landmarks.json").read_text())
    width, height = landmarks["canvas"]
    frames, records = [], []
    for index in range(8):
        source = directory / f"F{index}.svg"
        svg = source.read_bytes()
        handle = Rsvg.Handle.new_from_data(svg)
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        rectangle = Rsvg.Rectangle()
        rectangle.x = rectangle.y = 0
        rectangle.width, rectangle.height = width, height
        assert handle.render_document(cairo.Context(surface), rectangle)
        output = directory / f"F{index}.png"
        surface.write_to_png(str(output))
        with Image.open(output) as image:
            frame = image.convert("RGBA")
        frames.append(frame)
        bounds = frame.getchannel("A").getbbox()
        records.append({"frame": index, "svgSHA256": hashlib.sha256(svg).hexdigest(),
                        "pngSHA256": hashlib.sha256(output.read_bytes()).hexdigest(),
                        "alphaBounds": bounds,
                        "touchesCanvas": bounds is not None and
                        (bounds[0] == 0 or bounds[1] == 0 or bounds[2] == width or bounds[3] == height)})
    # Fixed whole-canvas presentation; never individual bounding-box fitting.
    small = [frame.resize((71, 71), Image.Resampling.LANCZOS) for frame in frames]
    small[0].save(directory / "guide-game-size.apng", save_all=True,
                  append_images=small[1:], duration=landmarks["cycleMs"] / 8,
                  loop=0, disposal=0, blend=0)
    sheet = Image.new("RGBA", (8 * 83, 93), (48, 52, 48, 255))
    text = ImageDraw.Draw(sheet)
    for index, frame in enumerate(small):
        sheet.alpha_composite(frame, (index * 83 + 6, 2))
        text.text((index * 83 + 6, 77), f"F{index}", fill="white")
    sheet.save(directory / "guide-sheet.png")
    receipt = {"status": "VERIFIED_AUTHORING_RASTER_ONLY", "frames": records,
               "sourcePixelsUsed": False, "imageCalls": 0,
               "presentation": "71px rounded whole canvas; fixed transform for all frames",
               "limits": ["Not finished art, image-provider pose success or motion approval",
                          "Alpha bounds diagnose guide clipping only; body/camera geometry is hand authored"]}
    (directory / "raster-receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    return receipt


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python3 scripts/render-clothed-guide.py GUIDE_DIRECTORY")
    print(json.dumps(render(sys.argv[1])))
