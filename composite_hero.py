from PIL import Image, ImageFilter
import numpy as np
from collections import deque

input_path = r"C:\Users\KIRUBAKARAN\.gemini\antigravity-ide\brain\ad587ee3-05af-44f2-a7a3-23ad3aa91e10\.user_uploaded\media_1788501596566.jpg"
bg_path = r"C:\Users\KIRUBAKARAN\.gemini\antigravity-ide\brain\ad587ee3-05af-44f2-a7a3-23ad3aa91e10\tvk_flag_background_1788501872754.jpg"
output_path = r"g:\TVK Projects\Nirmal Kumar\nirmal_tvk\public\Nirmlatvk.png"

print("Loading image...")
img = Image.open(input_path).convert("RGBA")
data = np.array(img, dtype=np.uint8)
h, w = data.shape[:2]

# Flood fill from ALL border pixels that are near-black
# This ensures only the connected background is removed, not the jacket
THRESHOLD = 40  # max brightness to consider "black background"

visited = np.zeros((h, w), dtype=bool)
to_remove = np.zeros((h, w), dtype=bool)

def is_dark(y, x):
    r, g, b = data[y, x, 0], data[y, x, 1], data[y, x, 2]
    return int(r) + int(g) + int(b) < THRESHOLD * 3

# BFS flood fill from border
queue = deque()

# Seed from all 4 borders
for x in range(w):
    if is_dark(0, x): queue.append((0, x))
    if is_dark(h-1, x): queue.append((h-1, x))
for y in range(h):
    if is_dark(y, 0): queue.append((y, 0))
    if is_dark(y, w-1): queue.append((y, w-1))

print("Flood filling background...")
while queue:
    y, x = queue.popleft()
    if visited[y, x]:
        continue
    visited[y, x] = True
    if is_dark(y, x):
        to_remove[y, x] = True
        for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)]:
            ny, nx = y+dy, x+dx
            if 0 <= ny < h and 0 <= nx < w and not visited[ny, nx]:
                queue.append((ny, nx))

print(f"Removing {to_remove.sum()} background pixels...")

# Apply mask - remove background pixels
data[to_remove, 3] = 0

# Slight feather at edges: pixels adjacent to removed area get softer alpha
fg = Image.fromarray(data, 'RGBA')

# Load and composite with background
print("Compositing with flag background...")
bg = Image.open(bg_path).convert("RGBA")
bg_aspect = bg.size[0] / bg.size[1]
new_bg_w = int(h * bg_aspect)
bg_resized = bg.resize((new_bg_w, h), Image.LANCZOS)

if new_bg_w > w:
    x_offset = (new_bg_w - w) // 2
    bg_cropped = bg_resized.crop((x_offset, 0, x_offset + w, h))
else:
    bg_cropped = bg_resized.resize((w, h), Image.LANCZOS)

composite = Image.alpha_composite(bg_cropped, fg)
composite.save(output_path, "PNG")
print(f"Done! Saved to {output_path}")
