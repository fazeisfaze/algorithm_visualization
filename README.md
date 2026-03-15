# Optimization Algorithm Visualizations with Manim

Dự án này sử dụng thư viện **Manim** (Mathematical Animation Engine) để trực quan hóa cách hoạt động của các thuật toán tối ưu hóa phổ biến. Các thuật toán được mô phỏng trong không gian 2D và 3D, giúp người xem dễ dàng hiểu được cơ chế hội tụ và tìm kiếm tối ưu toàn cục.

## Các thuật toán đã triển khai

| Thuật toán | File | Không gian | Hàm mục tiêu |
| :--- | :--- | :---: | :--- |
| **TLBO** (Teaching-Learning-Based Optimization) | `start.py` | 3D | Rastrigin |
| **PSO** (Particle Swarm Optimization) | `pso.py` | 3D | Rastrigin |
| **DE** (Differential Evolution) | `de.py` | 3D | Rastrigin |
| **Simulated Annealing** | `simulate_anneling.py` | 3D | Custom Multimodal |
| **Hill Climbing** | `hill_climbing.py` | 2D | Custom Multimodal |

## Yêu cầu hệ thống

Để chạy được các script này, bạn cần cài đặt:

1. **Python 3.7+**
2. **Manim** (và các phụ thuộc như FFmpeg, LaTeX)
3. **NumPy**

### Cài đặt thư viện

Bạn có thể cài đặt các thư viện cần thiết bằng lệnh:

```bash
pip install -r requirements.txt
```

## Cách chạy

Sử dụng lệnh `manim` để render video hoặc xem trực tiếp.

### 1. Xem chất lượng thấp (Nhanh)

```bash
manim -pql <file_name>.py <ClassName>
```

*Ví dụ: `manim -pql pso.py PSOSections`*

### 2. Xuất video chất lượng cao

```bash
manim -pqh <file_name>.py <ClassName>
```

### Các lớp (Class) tương ứng trong file

- **PSO**: `PSOSections` trong `pso.py`
- **DE**: `DESections` trong `de.py`
- **TLBO**: `TLBOSections` trong `start.py`
- **Simulated Annealing**: `SA` trong `simulate_anneling.py`
- **Hill Climbing**: `HC` trong `hill_climbing.py`



## Cấu trúc thư mục

- `*.py`: Các file mã nguồn thuật toán.
- `media/`: Chứa các file ảnh và video sau khi render.

