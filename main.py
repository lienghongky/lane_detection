from edge import canny,hough_transform
from skimage import io
import matplotlib.pyplot as plt
import numpy as np

# Change the image path to test on a different image
imagepath = 'test.png'
# imagepath = 'road.jpg'


print(f"[1/5] .Lane Detection Loading Image...")
print(f"-Image Path: {imagepath}")
# Load image
img = io.imread(imagepath,as_gray=True)

fig, axs = plt.subplots(3, 2)

print("[2/5] .Perfrom Canny Edge detection...")
# Run Canny edge detector
edges = canny(img, kernel_size=5, sigma=1.4, high=0.5, low=0.02)
# axs[0, 0].subplot(211)
axs[0, 0].imshow(img)
axs[0, 0].axis('off')
axs[0, 0].set_title("Image")

# axs[1, 0].subplot(212)
axs[0, 1].imshow(edges)
axs[0, 1].axis('off')
axs[0, 1].set_title("Edge")


H, W = img.shape

# Generate mask for ROI (Region of Interest)
mask = np.zeros((H, W))
for i in range(H):
    for j in range(W):
        if i > (H / W) * j and i > -(H / W) * j + H:
            mask[i, j] = 1

# Extract edges in ROI
roi = edges * mask

# axs[0, 1].plot(1,2,1)
axs[1, 0].imshow(mask)
axs[1, 0].set_title('Mask')
axs[1, 0].axis('off')

# axs[1, 1].plot(1,2,2)
axs[1, 1].imshow(roi)
axs[1, 1].set_title('Edges in ROI')
axs[1, 1].axis('off')

print("[3/5] .Perform Hough Transform...")
# Perform Hough transform on the ROI
acc, rhos, thetas = hough_transform(roi)

# Coordinates for right lane
xs_right = []
ys_right = []

# Coordinates for left lane
xs_left = []
ys_left = []

for i in range(20):
    idx = np.argmax(acc)
    r_idx = idx // acc.shape[1]
    t_idx = idx % acc.shape[1]
    acc[r_idx, t_idx] = 0 # Zero out the max value in accumulator

    rho = rhos[r_idx]
    theta = thetas[t_idx]

    # Transform a point in Hough space to a line in xy-space.
    a = - (np.cos(theta)/np.sin(theta)) # slope of the line
    b = (rho/np.sin(theta)) # y-intersect of the line

    # Break if both right and left lanes are detected
    if xs_right and xs_left:
        break

    if a < 0: # Left lane
        if xs_left:
            continue
        xs = xs_left
        ys = ys_left
    else: # Right Lane
        if xs_right:
            continue
        xs = xs_right
        ys = ys_right

    for x in range(img.shape[1]):
        y = a * x + b
        if y > img.shape[0] * 0.6 and y < img.shape[0]:
            xs.append(x)
            ys.append(int(round(y)))
print ("[4/5] .Plotting Detected Lane...")
axs[2,1].imshow(img)
axs[2,1].set_title('Detected Lane')
if xs_left and ys_left:
    axs[2,1].plot(xs_left, ys_left, linewidth=1, color='blue', label='Left Lane')
if xs_right and ys_right:
    axs[2,1].plot(xs_right, ys_right, linewidth=1, color='red', label='Right Lane')
axs[2,1].axis('off')
fig.tight_layout()
print("[5/5] .Showing Detected Lane...")

axs[2,0].set_title('')
axs[2,0].axis('off')
plt.show()