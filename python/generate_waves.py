import numpy as np
import matplotlib.pyplot as plt
import os

# ================= 配置部分 =================
# 1. 确定根目录下的 images 文件夹路径
# 逻辑：获取当前脚本所在目录 -> 上一级目录 -> images
BASE_IMAGES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'images')

# 2. 定义三个实验的子文件夹路径
DIRS = {
    'exp1': os.path.join(BASE_IMAGES_DIR, 'exp1'),
    'exp2': os.path.join(BASE_IMAGES_DIR, 'exp2'),
    'exp3': os.path.join(BASE_IMAGES_DIR, 'exp3')
}

# 3. 自动创建所有需要的文件夹
for dir_path in DIRS.values():
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print(f"Created directory: {dir_path}")

# 设置绘图风格，模仿示波器 (黑色背景，高亮线条)
plt.style.use('dark_background')

def create_oscilloscope_plot(t, input_signal, output_signal, title, save_path):
    """
    绘制双通道示波器波形图并保存到指定路径
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 绘制通道1 (输入) - 黄色
    ax.plot(t, input_signal, 'y', label='CH1 (Input)', linewidth=1.5)
    
    # 绘制通道2 (输出) - 青色
    if output_signal is not None:
        ax.plot(t, output_signal, 'c', label='CH2 (Output)', linewidth=1.5)
    
    ax.set_title(title, fontsize=14, color='white')
    ax.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.6)
    ax.legend(loc='upper right', fontsize=10)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Voltage (V)')
    
    # 保存图片
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()
    print(f"Saved: {save_path}")

# ================= 实验一：傅里叶级数与滤波器 (存入 exp1) =================
print("\nGenerating Exp 1 images...")
f1 = 100
T1 = 1 / f1
t1 = np.linspace(0, 3*T1, 1000)

square_wave = np.sign(np.sin(2 * np.pi * f1 * t1)) 

# 1. 低截止频率
output_low_cutoff = (4/np.pi) * np.sin(2 * np.pi * f1 * t1)
save_file = os.path.join(DIRS['exp1'], "exp1_low_cutoff.png")
create_oscilloscope_plot(t1, square_wave, output_low_cutoff, 
                        "Exp 1: Low Cutoff Frequency (Fundamental Only)", 
                        save_file)

# 2. 高截止频率
output_high_cutoff = (4/np.pi) * (np.sin(2 * np.pi * f1 * t1) + 
                                  (1/3)*np.sin(2 * np.pi * 3 * f1 * t1) + 
                                  (1/5)*np.sin(2 * np.pi * 5 * f1 * t1) +
                                  (1/7)*np.sin(2 * np.pi * 7 * f1 * t1))
save_file = os.path.join(DIRS['exp1'], "exp1_high_cutoff.png")
create_oscilloscope_plot(t1, square_wave, output_high_cutoff, 
                        "Exp 1: High Cutoff Frequency (Gibbs Phenomenon)", 
                        save_file)


# ================= 实验二：连续时间系统时域分析 (存入 exp2) =================
print("\nGenerating Exp 2 images...")
tau = 0.004
t2 = np.linspace(0, 0.06, 1000)
f2 = 50

# 1. 阶跃响应
step_input = np.where((t2 * f2) % 1 < 0.8, 1, 0) * 1.0 
step_output = np.zeros_like(t2)
v_cap = 0
for i in range(1, len(t2)):
    dt = t2[i] - t2[i-1]
    v_cap = v_cap + (step_input[i] - v_cap) * dt / tau
    step_output[i] = v_cap

save_file = os.path.join(DIRS['exp2'], "exp2_step_response.png")
create_oscilloscope_plot(t2, step_input, step_output, 
                        "Exp 2: Step Response (RC Circuit)", 
                        save_file)

# 2. 冲激响应
impulse_input = np.where((t2 * f2) % 1 < 0.05, 1, 0) * 1.0
impulse_output = np.zeros_like(t2)
v_cap = 0
for i in range(1, len(t2)):
    dt = t2[i] - t2[i-1]
    v_cap = v_cap + (impulse_input[i] - v_cap) * dt / tau
    impulse_output[i] = v_cap

save_file = os.path.join(DIRS['exp2'], "exp2_impulse_response.png")
create_oscilloscope_plot(t2, impulse_input, impulse_output, 
                        "Exp 2: Impulse Response (RC Circuit)", 
                        save_file)

# 3. 正弦稳态响应
t3 = np.linspace(0, 0.003, 1000)
f3 = 1000
sine_input = np.sin(2 * np.pi * f3 * t3)
w = 2 * np.pi * f3
H_mag = 1 / np.sqrt(1 + (w * tau)**2)
H_phase = -np.arctan(w * tau)
sine_output = H_mag * np.sin(2 * np.pi * f3 * t3 + H_phase)

save_file = os.path.join(DIRS['exp2'], "exp2_sine_response.png")
create_oscilloscope_plot(t3, sine_input, sine_output, 
                        "Exp 2: Sinusoidal Steady State Response (1000Hz)", 
                        save_file)


# ================= 实验三：采样与混叠 (存入 exp3) =================
print("\nGenerating Exp 3 images...")
f_sig = 1000
t4 = np.linspace(0, 0.005, 1000)

# 1. 正常采样
input_sig = np.sin(2 * np.pi * f_sig * t4)
recovered_normal = 0.9 * np.sin(2 * np.pi * f_sig * t4)
save_file = os.path.join(DIRS['exp3'], "exp3_sampling_normal.png")
create_oscilloscope_plot(t4, input_sig, recovered_normal, 
                        "Exp 3: Sampling at 4000Hz (Normal Recovery)", 
                        save_file)

# 2. 混叠采样
recovered_aliased = 0.5 * np.sin(2 * np.pi * 500 * t4 + np.pi) 
save_file = os.path.join(DIRS['exp3'], "exp3_sampling_aliased.png")
create_oscilloscope_plot(t4, input_sig, recovered_aliased, 
                        "Exp 3: Sampling at 500Hz (Aliasing Effect)", 
                        save_file)

print("\nDone! Check your 'images' folder.")