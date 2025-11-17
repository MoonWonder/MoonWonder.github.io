---
title: CUDA 安装配置与工具链
subtitle:
date: 2025-11-17T17:35:34+08:00
description:
keywords:
draft: false
---

> 要开始 CUDA 开发，首先需要搭建好软件和硬件环境，包括安装 NVIDIA 显卡驱动、CUDA Toolkit 开发包，并配置相应的编译器和开发工具。在本章中，我们将分别介绍在 **Linux** 和 **Windows** 平台下安装配置 CUDA 的方法，并讨论如何使用 VSCode 与 NVIDIA Nsight 工具来进行 CUDA 程序的开发、调试和分析。

### 2.1 硬件与软件需求

**GPU 硬件：** CUDA 只能运行在带有 NVIDIA CUDA 支持的 GPU 上。因此，您需要一块 NVIDIA 显卡（支持 Compute Capability 3.0 或更高的型号较佳，这包括 Kepler 架构及以后的 GPU）。开发机器应安装对应的 NVIDIA 显卡驱动。如果是笔记本电脑或工作站，请确保安装有 NVIDIA GPU 且驱动已正确配置。

**操作系统：** CUDA Toolkit 支持 Windows、Linux 和 MacOS（但 MacOS 从 CUDA 10 开始已不再官方支持新的版本）。本书重点介绍 Windows 和 Linux 下的安装。通常科研和服务器环境多用 Linux，桌面用户和很多初学者则习惯 Windows，因此我们分别介绍。需要注意，不同版本的 CUDA Toolkit 对 OS 版本有一定要求，请在 NVIDIA 官网上查看兼容矩阵。

**CUDA Toolkit：** 这是 NVIDIA 提供的开发包，包含编译器 `nvcc`、CUDA 库（如 cuBLAS、cuDNN 等）、示例代码、文档和调试工具等。截至撰写时较新的版本是 CUDA 12.x 系列。选择 CUDA Toolkit 版本时，一般建议使用相对新的版本但也要兼容您的 GPU 驱动版本。通常先安装 GPU 驱动，再安装 CUDA Toolkit。

**开发工具：** 您可以选择使用命令行工具（如 Linux 下用 `nvcc` 编译）或者集成开发环境 IDE（如 Visual Studio、VSCode 等）进行 CUDA 开发。NVIDIA 提供 Nsight 系列工具用于调试和分析 CUDA 程序。另外，CMake 等构建工具能够方便地配置跨平台 CUDA 工程。

下面分别介绍 Linux 和 Windows 下的 CUDA 安装步骤。

### 2.2 在 Linux 下安装 CUDA

**步骤 1：安装 NVIDIA 驱动：** 在 Linux (Ubuntu 为例) 上，可以通过 apt 包管理安装受支持版本的 NVIDIA 驱动。例如，首先确保系统有支持 GPU 的驱动库：

```sh
sudo apt update
sudo apt install nvidia-driver-530
```

上面安装的是版本 530 的驱动（具体版本号可能因 GPU 型号和发行版不同）。安装完成后重启系统，并用 `nvidia-smi` 命令确认驱动正常运行及 GPU 被识别。

**步骤 2：下载并安装 CUDA Toolkit：** 访问 NVIDIA 开发者官网下载 CUDA Toolkit 的. run 安装包或 deb 包。例如，对于 Ubuntu，可以使用 deb 网络安装方式：

```sh
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-repo-ubuntu2204_12.2.0-1_amd64.deb
sudo dpkg -i cuda-repo-ubuntu2204_12.2.0-1_amd64.deb
sudo apt update
sudo apt install cuda-12-2
```

上述以 CUDA 12.2 为例。安装过程会将 CUDA 工具链安装到 `/usr/local/cuda-12.2/` 目录（默认）。安装完成后，在 `.bashrc` 中添加环境变量：

```sh
export PATH=/usr/local/cuda-12.2/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda-12.2/lib64:$LD_LIBRARY_PATH
```

保存并 `source .bashrc`。然后执行 `nvcc --version` 应该可以看到 CUDA 编译器版本信息。如果有多个版本 CUDA，可以通过修改 PATH 来切换默认版本。

**步骤 3：安装 CUDA 库（可选）和 cuDNN 等：** CUDA Toolkit 通常包含基础的 CUDA 库。如果需要深度学习加速库 cuDNN、TensorRT 等，则需单独下载安装。例如 cuDNN 可以从 NVIDIA 开发者网站下载，与对应 CUDA 版本匹配的压缩包，将包含的 `libcudnn.so` 等拷贝到 `/usr/local/cuda/lib64/` 并运行 `ldconfig` 注册。

**步骤 4：验证安装：** CUDA Toolkit 自带一些 samples，可以复制到主目录编译运行。例如：

```sh
cuda-install-samples-12.2.sh ~/
cd ~/NVIDIA_CUDA-12.2_Samples/1_Utilities/deviceQuery
make
./deviceQuery
```

deviceQuery 程序将输出检测到的 GPU 及 CUDA 支持信息，如成功运行则说明环境 OK。还可以运行 `bandwidthTest` 检查主机到设备的带宽等。

**常见问题：** 如果安装过程中遇到旧版驱动冲突，需要卸载旧驱动。确保驱动版本与 CUDA 版本匹配，否则可能 deviceQuery 会报错。Ubuntu 上也可以使用 `ubuntu-drivers devices` 查看可用驱动版本并自动安装。

### 2.3 在 Windows 下安装 CUDA(不推荐)

** 步骤 1：安装 NVIDIA 显卡驱动：** 前往 NVIDIA 官网下载适用于您 GPU 的最新 Windows 驱动程序，按照向导安装并重启。也可以通过 GeForce Experience 软件自动安装更新驱动。确保在 Windows 设备管理器中 GPU 正常。

** 步骤 2：安装 CUDA Toolkit：** 从 NVIDIA 官网上下载适用于 Windows 的 CUDA Toolkit 安装包（exe）。运行安装程序时，一般选择 “快速安装（Express）” 即可，它会安装 CUDA Toolkit、示例、驱动（如果需要）以及 Visual Studio 集成组件等。在安装过程中请注意勾选 Visual Studio 集成。如果未安装 Visual Studio，则可以选择只安装 NVCC 编译工具，后续可使用 VSCode。

** 步骤 3：安装开发环境：**Windows 上常用 Visual Studio (Community 版即可) 进行 CUDA 开发，因为 CUDA 安装包通常集成 VS 插件，方便创建和编译 CUDA 工程。如果使用 VSCode，需要安装 NVIDIA 提供的 CUDA 扩展（后面介绍）。确保 Visual Studio 能识别 CUDA：安装完 CUDA 后，新建项目应能看到 “CUDA Runtime” 库选项。

** 步骤 4：验证：** 打开 “NVIDIA CUDA Samples” 项目，编译运行 deviceQuery 示例。在命令行中也可以执行 `nvcc --version` 查看。如果 nvcc 未加入 PATH，可以手动将 `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.2\bin` 加入系统 PATH。

**VSCode 配置：** 许多开发者喜欢使用 VSCode 编写 CUDA，这需要一些配置：

*   安装 **CUDA Toolkit Extension**：在 VSCode 扩展市场搜索 "CUDA" 安装官方扩展。它提供了语法高亮、代码片段和调试支持。
    
*   配置编译任务：可使用 VSCode 的`tasks.json`来调用 nvcc 编译 .cu 文件，或使用 CMake 工程。稍后 2.5 节会详述 CMake 的使用。
    

**Nsight 工具：**NVIDIA Nsight 包括 Nsight Compute（性能分析）和 Nsight Systems（系统级分析）以及 Nsight Graphics 等。Windows 上可以通过 CUDA 安装包附带的 Nsight Visual Studio Edition 来在 Visual Studio 中调试 GPU 核函数（类似 CPU 调试）。也可以安装独立的 Nsight Systems/Compute GUI 版本，用于分析 GPU 执行时间、内存带宽等。后面第十章会介绍这些工具的具体用法。

### 2.4 VSCode 与 Visual Studio 开发 CUDA

**使用 Visual Studio：** 如果您偏好 Visual Studio，在安装 CUDA Toolkit 后，可以直接在 VS 中创建 CUDA 工程。模板会生成 .cu 源文件和 .cpp 主机代码文件。按 F5 编译运行即可调试主机代码；要调试核函数，可借助 Nsight VS 插件。在 VS 中，设置断点于核函数并使用 Nsight 调试，能够单步跟踪 GPU 线程（需要在 CUDA 工程调试模式下，并安装 Nsight VS Edition）。

**使用 VSCode + CMake：** 现代 CMake 对 CUDA 有原生支持，我们可以用 CMake 构建跨平台 CUDA 项目。示例如下 CMakeLists.txt：

```cmake
cmake_minimum_required(VERSION 3.18)
project(MyCudaProject LANGUAGES CXX CUDA)

add_executable(my_program main.cu)
set_target_properties(my_program PROPERTIES 
    CUDA_ARCHITECTURES "75" # 根据GPU架构设置
    CUDA_SEPARABLE_COMPILATION ON)
```

这里 `project(... LANGUAGES CXX CUDA)` 声明开启 CUDA 支持。然后添加可执行目标时直接包含 `.cu` 文件，CMake 会调用 NVCC 编译 CUDA 代码。可以通过 `CUDA_ARCHITECTURES` 指定目标 GPU 架构（如 75 代表 Turing 架构），`CUDA_SEPARABLE_COMPILATION` 开启设备端代码的分离编译支持。如果需要链接 CUDA 库，比如 cuBLAS, cuDNN，可以使用 `find_package(CUDAToolkit)` 或手动链接对应库。

VSCode 中安装 CMake Tools 扩展后，可配置 `launch.json` 和 `tasks.json` 来编译运行。也可以不用 CMake，直接写简单 tasks 来调用 nvcc。例如 tasks.json:

```json
{
  "label": "Build CUDA",
  "command": "nvcc",
  "args": ["-o", "main.exe", "main.cu", "-arch=sm_75"],
  "problemMatcher": "$gcc"
}
```

这样按 Ctrl+Shift+B 即可编译。

**IntelliSense 配置：** 需要让 VSCode 识别 CUDA 语法，需在 `.cu` 文件头添加：

```cpp
#if defined(__INTELLISENSE__)
#include "cuda_runtime.h"
#endif
```

或在 `c_cpp_properties.json` 中加入 CUDA 包含路径。

### 2.5 Nsight 调试与分析简介

_NVIDIA Nsight_ 是 NVIDIA 提供的一系列 GPU 开发工具的统称：

*   **Nsight Visual Studio Edition：** 集成在 VS 中的 GPU 调试工具。可设置断点调试核函数，查看 GPU 内存和线程状态。
    
*   **Nsight Systems：** 系统级时间轴分析工具，显示 CPU 和 GPU 各个任务的时间线，帮助识别瓶颈（如数据传输占用时间、核函数执行时间等）。
    
*   **Nsight Compute：** 详细的内核性能分析工具，收集每个核函数的执行统计（例如指令吞吐、内存访存效率、占用率等），用于优化代码性能。
    

在 Windows 平台，Nsight VS 已随 CUDA Toolkit 安装，可以通过菜单 “Nsight -> Start CUDA Debugging” 来启动 GPU 调试。在 Linux 或需要更强分析时，可以使用独立的 Nsight Systems/Compute。例如，在 Linux 下运行 Nsight Systems:

```
nsys profile --stats=true ./my_program
```

这会生成 .nsys-rep 报告文件，用 GUI 打开可查看详细时间轴。

Nsight Compute 可通过命令行 `ncu` 采集内核的硬件计数器，例如：

```
ncu --metrics sm__throughput.avg.pct_of_peak_sustained_active ./my_program
```

这些工具将在第十章详细介绍。本章重点在于安装配置，它们的目的是让您能够顺利编译、运行并初步调试 CUDA 程序。如果您完成了以上安装步骤，现在您的开发环境已经搭建完毕，可以开始 CUDA 编程实践了。

#### 本章小结

*   Linux 平台下通过包管理或. run 文件可安装 NVIDIA 驱动和 CUDA Toolkit，需配置 PATH 和 LD_LIBRARY_PATH 环境变量。使用官方 Samples 可以验证安装正确。
    
*   Windows 平台下使用 NVIDIA 提供的安装包安装 CUDA Toolkit，建议安装 Visual Studio 或使用 VSCode+CMake 等方式进行开发。安装 CUDA 后应验证 nvcc 和示例程序的运行。
    
*   VSCode 需要安装 CUDA 扩展，并配置编译任务或 CMake 工程以支持 CUDA 开发。CMake 3.8+ 已原生支持 CUDA 语言，可用 `project(... LANGUAGES CUDA)` 启用。
    
*   NVIDIA Nsight 工具有助于 CUDA 程序的调试与性能分析，包括 VS 集成调试、Systems 时间轴分析和 Compute 内核分析。熟悉基本用法将有助于后续优化工作。
    

#### 练习题

1.  在您的操作系统上安装正确版本的 CUDA Toolkit，并编译运行 CUDA Samples 中的 `vectorAdd` 或 `matrixMul` 示例，观察输出结果。如果过程中遇到困难，例如驱动不匹配或环境变量问题，请记录并解决。
    
2.  编写一个简单的 CUDA 程序，例如计算数组元素平方值，尝试使用 VSCode 配合 CMake 或 tasks.json 进行编译运行。确保能够成功调用 `nvcc` 生成可执行文件。
    
3.  尝试使用 Nsight Systems 或 `nvprof`（CUDA 10 及以前版本提供）对上述程序进行简单分析，看看 CPU<->GPU 的执行顺序。在程序中插入 `cudaDeviceSynchronize()` 来对比同步与异步执行的时间差异。
    
4.  如果使用 Visual Studio，创建一个新的 CUDA 工程，编写并调试一个简单核函数（例如对数组加常数）。在调试模式下单步跟踪核函数执行，并观察线程变量值。这可以帮助理解 GPU 上的大量线程是如何调度的。
