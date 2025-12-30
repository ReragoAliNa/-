# 信号处理综合课程设计

本项目为基于 NI ELVIS III 平台的信号处理课程设计报告及相关代码。

## 目录结构

*   **`docs/`**: 文档目录
    *   **`src/`**: LaTeX 源码目录
        *   `report.tex`: 主文件
        *   `content.tex`: 正文内容
    *   **`drafts/`**: 原始草稿目录 (`report.md`)
    *   **`build/`**: 编译中间文件及输出目录
    *   **`references/`**: 参考资料
    *   **`report.pdf`**: 最终生成的报告 PDF
*   **`python/`**: 仿真代码目录
    *   `generate_waves.py`: 生成报告所需波形图的脚本
*   **`images/`**: 图片资源目录

## 如何编译报告

为了保持目录整洁，建议将编译产生的中间文件输出到 `texCache` 目录。

### 前置要求
*   安装 TeX Live (包含 XeLaTeX 引擎)
*   安装 Python (用于生成仿真图)

### 编译步骤

1.  **进入源码目录**：
    ```bash
    cd docs/src
    ```

2.  **创建构建目录**（首次运行时）：
    ```bash
    mkdir -p ../build
    ```

3.  **运行编译命令**（指定输出目录）：
    ```bash
    xelatex -output-directory=../build report.tex
    # 再次运行以生成目录和引用
    xelatex -output-directory=../build report.tex
    ```

4.  **查看结果**：
    编译完成后，PDF 文件位于 `docs/build/report.pdf`。
    
    *(可选) 将 PDF 复制回 docs 根目录方便查看：*
    ```bash
    cp ../build/report.pdf ../report.pdf
    ```

## Python 仿真

运行以下命令生成波形图：
```bash
cd python
python generate_waves.py
```
生成的图片将保存在 `images/` 目录下。