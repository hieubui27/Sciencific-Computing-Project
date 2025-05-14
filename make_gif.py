import imageio
import os

# Thư mục chứa ảnh
folder = 'D:\DLA\Images'
# Tên file GIF đầu ra
output_gif = 'dla_simulation1.gif'

# Lấy danh sách file ảnh PNG, sắp xếp theo thứ tự
images = sorted([img for img in os.listdir(folder) if img.endswith('.png')],
                key=lambda x: int(x.split('.')[0]))

# Đọc ảnh và tạo GIF
frames = []
for filename in images:
    filepath = os.path.join(folder, filename)
    image = imageio.imread(filepath)
    frames.append(image)

# Lưu thành GIF
imageio.mimsave(output_gif, frames, duration=0.2)  # duration: thời gian giữa các frame (giây)
print("GIF created:", output_gif)
