@echo off
echo ========================================
echo 专注时间管理器 - 依赖检查
echo ========================================
echo.

echo 好消息！此程序现在使用Windows原生方法播放音频
echo 无需安装任何额外的Python包！
echo.

echo 检查Python环境...
python --version > nul 2>&1
if errorlevel 1 (
    echo 错误：Python未安装或不在PATH中
    echo 请安装Python并确保在PATH中
    pause
    exit /b 1
)

echo Python环境正常！
echo.

echo 检查音频文件...
if exist "*.mp3" (
    echo 音频文件存在 ✓
) else (
    echo 警告：未找到音频文件
)

echo.
echo 所有依赖都已满足！
echo 现在可以直接运行 run.bat 来启动程序
echo.
pause
