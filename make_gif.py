import imageio.v3 as imageio
import os

# Thư mục chứa ảnh
folder = 'D:\\DLA\\simulation_images'
# Tên file GIF đầu ra
output_gif = 'Robot1.gif'

# Lấy danh sách file ảnh PNG, sắp xếp theo thứ tự
images = sorted([img for img in os.listdir(folder) if img.endswith('.png')],
                key=lambda x: int(x.split('_')[-1].split('.')[0]))

# Đọc ảnh và tạo GIF
frames = []
for filename in images:
    filepath = os.path.join(folder, filename)
    image = imageio.imread(filepath)
    frames.append(image)

# Lưu thành GIF
imageio.imwrite(output_gif, frames, duration=0.2)
print("GIF created:", output_gif)