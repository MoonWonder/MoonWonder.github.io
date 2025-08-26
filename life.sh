#!/bin/zsh

# 生成每日日记的脚本
# 使用方法: ./life.sh [YYYY-MM-DD] (如果不提供日期，则使用当天日期)
# 示例: ./life.sh 2025-08-26

# 基准日期: 2025-06-28 是 week1/day1
REFERENCE_DATE="2025-06-28"

# 获取输入日期，如果没有提供则使用当前日期
if [ $# -eq 0 ]; then
    TARGET_DATE=$(date +%Y-%m-%d)
else
    TARGET_DATE=$1
fi

echo "创建日期为 $TARGET_DATE 的日记..."

# 将日期转换为自纪元以来的天数
reference_epoch=$(date -d "$REFERENCE_DATE" +%s)
target_epoch=$(date -d "$TARGET_DATE" +%s)

# 计算天数差
days_diff=$(( (target_epoch - reference_epoch) / 86400 ))

if [ $days_diff -lt 0 ]; then
    echo "错误：目标日期早于基准日期 $REFERENCE_DATE"
    exit 1
fi

# 计算周数和天数
# 每周5个工作日，从周一到周五
week_num=$(( days_diff / 5 + 1 ))
day_num=$(( days_diff % 5 + 1 ))

# 计算文件所在的目录段 (1-100)
segment=$(( (week_num - 1) / 100 + 1 ))
segment_start=$(( (segment - 1) * 100 + 1 ))
segment_end=$(( segment * 100 ))

# 构建目录路径
dir_path="content/posts/life/${segment_start}-${segment_end}/week$(printf "%d" $week_num)"
file_path="${dir_path}/day$(printf "%d" $day_num).md"

echo "周数: week$(printf "%03d" $week_num)"
echo "天数: day$(printf "%03d" $day_num)"
echo "目录段: ${segment_start}-${segment_end}"
echo "文件路径: $file_path"

# 创建目录
mkdir -p "$dir_path"

# 检查文件是否已存在
if [ -f "$file_path" ]; then
    echo "警告：文件 $file_path 已存在！"
    read -p "是否要覆盖？(y/N): " confirm
    if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
        echo "操作已取消"
        exit 1
    fi
fi

# 使用 Hugo 创建新文件
hugo new "$file_path" --kind=life

if [ $? -eq 0 ]; then
    echo "✅ 成功创建日记文件: $file_path"
    echo "📝 你可以开始编辑你的日记了！"
    
    # 询问是否立即打开文件编辑
    read -p "是否立即打开文件编辑？(y/N): " open_file
    if [ "$open_file" = "y" ] || [ "$open_file" = "Y" ]; then
        # 尝试使用 VS Code 打开，如果没有则使用默认编辑器
        if command -v code >/dev/null 2>&1; then
            code "$file_path"
        elif command -v vim >/dev/null 2>&1; then
            vim "$file_path"
        elif command -v nano >/dev/null 2>&1; then
            nano "$file_path"
        else
            echo "没有找到合适的编辑器，请手动打开文件: $file_path"
        fi
    fi
else
    echo "❌ 创建文件失败"
    exit 1
fi