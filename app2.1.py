import time
import random
import os
import sys
import threading

# Windows系统编码设置
if sys.platform.startswith("win"):
    import locale
    # 设置控制台编码为UTF-8
    os.system("chcp 65001 > nul")
    # 设置环境变量
    os.environ["PYTHONIOENCODING"] = "utf-8"
# 版本号：2.1
# 算是最完善的一版了，适配了不同的操作系统，包括macOS、Linux和Windows
# 优化了进度条显示

# 获取脚本所在目录的绝对路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def play_sound_async(sound_type):
    """异步播放提示音"""
    def _play():
        # macOS系统使用afplay
        if sys.platform == "darwin":
            if sound_type == "beep":
                # 进入长休息音效
                os.system(f"afplay {os.path.join(SCRIPT_DIR, 'long_rest_start.mp3')}")
            elif sound_type == "start_focus":
                # 开始专注的音效
                os.system(f"afplay {os.path.join(SCRIPT_DIR, 'short_rest_end.mp3')}")
            elif sound_type == "rest_start":
                # 进入短休息的音效 - macOS专用.aiff格式
                os.system(f"afplay {os.path.join(SCRIPT_DIR, 'short_rest_start.aiff')}")
            else:
                # 结束短休息的音效
                os.system(f"afplay {os.path.join(SCRIPT_DIR, 'short_rest_end.mp3')}")
        # Linux系统使用系统音频播放器播放指定的音频文件
        elif sys.platform.startswith("linux"):
            if sound_type == "beep":
                # 进入长休息音效
                os.system(f"paplay {os.path.join(SCRIPT_DIR, 'long_rest_start.mp3')} 2>/dev/null || aplay {os.path.join(SCRIPT_DIR, 'long_rest_start.mp3')} 2>/dev/null || echo -e '\a'")
            elif sound_type == "start_focus":
                # 开始专注的音效
                os.system(f"paplay {os.path.join(SCRIPT_DIR, 'short_rest_end.mp3')} 2>/dev/null || aplay {os.path.join(SCRIPT_DIR, 'short_rest_end.mp3')} 2>/dev/null || echo -e '\a'")
            elif sound_type == "rest_start":
                # 进入短休息的音效 - Linux使用.mp3格式
                os.system(f"paplay {os.path.join(SCRIPT_DIR, 'short_rest_start.mp3')} 2>/dev/null || aplay {os.path.join(SCRIPT_DIR, 'short_rest_start.mp3')} 2>/dev/null || echo -e '\a'")
            else:
                # 结束短休息的音效
                os.system(f"paplay {os.path.join(SCRIPT_DIR, 'short_rest_end.mp3')} 2>/dev/null || aplay {os.path.join(SCRIPT_DIR, 'short_rest_end.mp3')} 2>/dev/null || echo -e '\a'")
        # Windows系统（包括win32/win64/win10+/win11）使用系统音频播放器
        elif sys.platform in ("win32", "win64", "cygwin") or sys.platform.startswith("win"):
            try:
                # 方法1：使用Windows内置的start命令播放音频（推荐，无需额外模块）
                if sound_type == "beep":
                    # 进入长休息音效
                    os.system(f'start "" /min wmplayer "{os.path.join(SCRIPT_DIR, "long_rest_start.mp3")}"')
                elif sound_type == "start_focus":
                    # 开始专注的音效
                    os.system(f'start "" /min wmplayer "{os.path.join(SCRIPT_DIR, "short_rest_end.mp3")}"')
                elif sound_type == "rest_start":
                    # 进入短休息的音效 - Windows使用.mp3格式
                    os.system(f'start "" /min wmplayer "{os.path.join(SCRIPT_DIR, "short_rest_start.mp3")}"')
                else:
                    # 结束短休息的音效
                    os.system(f'start "" /min wmplayer "{os.path.join(SCRIPT_DIR, "short_rest_end.mp3")}"')
                    
            except Exception as e:
                # 如果start命令失败，尝试使用winsound播放系统提示音
                try:
                    import winsound
                    if sound_type == "beep":
                        # 进入长休息音效
                        winsound.Beep(800, 300)  # 频率800Hz，持续300毫秒
                    elif sound_type == "start_focus":
                        # 开始专注的音效
                        winsound.Beep(1000, 400)  # 频率1000Hz，持续400毫秒
                    elif sound_type == "rest_start":
                        # 进入短休息的音效
                        winsound.Beep(1000, 500)  # 频率1000Hz，持续500毫秒
                    else:
                        # 结束短休息的音效
                        winsound.Beep(1200, 700)  # 频率1200Hz，持续700毫秒
                except ImportError:
                    # 如果没有winsound模块，使用控制台蜂鸣
                    if sound_type == "rest_end":
                        print("\a\a", end='', flush=True)
                    else:
                        print("\a", end='', flush=True)
        # 如果都不是以上系统，使用控制台蜂鸣作为最后手段
        else:
            if sound_type == "rest_end":
                print("\a\a", end='', flush=True)
            else:
                print("\a", end='', flush=True)
    
    # 创建并启动线程来异步播放音效
    sound_thread = threading.Thread(target=_play, daemon=True)
    sound_thread.start()

def play_sound(sound_type="beep"):
    """保持向后兼容的播放提示音函数"""
    play_sound_async(sound_type)

def countdown(minutes, rest_duration, sound_range_a, sound_range_b):
    """倒计时功能 - 状态机实现"""
    total_seconds = minutes * 60
    # 将分钟转换为秒
    rest_interval = random.randint(sound_range_a * 60, sound_range_b * 60)
    # 记录已过去的秒数
    elapsed_seconds = 0
    
    # 状态定义
    STATE_FOCUS = 1      # 专注状态
    STATE_REST_ALERT = 2 # 短休息时间到
    STATE_RESTING = 3    # 休息中
    STATE_REST_END = 4   # 休息结束重新专注
    
    current_state = STATE_FOCUS  # 初始状态为状态1
    lines_to_clear = 0  # 需要清除的行数
    judge = False        # 是否需要和状态4同步
    
    def clear_lines(n):
        """清除n行输出"""
        for _ in range(n):
            print('\033[1A\033[K', end='')  # 上移一行并清除
    
    def print_focus_line():
        """打印专注时间行"""
        mins, secs = divmod(total_seconds, 60)
        progress = elapsed_seconds / (minutes * 60)
        # 根据总时长动态计算进度条长度，最少5
        bar_length = max(5, minutes // 2)
        filled = int(round(bar_length * progress))
        bar = '🕒' + '█' * filled + '░' * (bar_length - filled) + '🕔'
        time_format = f'{mins:02d}:{secs:02d}'
        print(f'⏳ 专注时间剩余：{time_format}  {bar}')
    
    while total_seconds >= 0:
        if current_state == STATE_FOCUS:
            # 状态1：专注情况
            if lines_to_clear > 0:
                clear_lines(lines_to_clear)
                lines_to_clear = 0
            
            print_focus_line()
            lines_to_clear = 1
            if judge:
                print("休息结束，继续专注！")
                lines_to_clear = 2
            
            # 检查是否需要切换到休息状态
            if total_seconds > 0 and elapsed_seconds >= rest_interval:
                current_state = STATE_REST_ALERT
                lines_to_clear = 1  # 下一状态会打印新内容
                if judge:
                    lines_to_clear = 2
                
                
        elif current_state == STATE_REST_ALERT:
            # 状态2：短休息时间到
            judge = True
            if lines_to_clear > 0:
                clear_lines(lines_to_clear)
                lines_to_clear = 0
            
            print_focus_line()
            print("短暂休息时间到！")
            lines_to_clear = 2
            
            play_sound("rest_start")  # 进入短休息的音效
            current_state = STATE_RESTING
            rest_seconds = rest_duration
            
            
        elif current_state == STATE_RESTING:
            # 状态3：休息中
            if lines_to_clear > 0:
                clear_lines(lines_to_clear)
                lines_to_clear = 0
            
            print_focus_line()
            print(f"休息时间剩余：{rest_seconds}秒")
            lines_to_clear = 2
            
            rest_seconds -= 1
            if rest_seconds <= 0:
                current_state = STATE_REST_END
                lines_to_clear = 2  # 下一状态会打印新内容
                
                
        elif current_state == STATE_REST_END:
            # 状态4：休息结束重新专注
            if lines_to_clear > 0:
                clear_lines(lines_to_clear)
                lines_to_clear = 0
            
            print_focus_line()
            print("休息结束，继续专注！")
            lines_to_clear = 2
            
            play_sound("rest_end")  # 结束短休息的音效
            current_state = STATE_FOCUS
            
            # 重新设置下一个休息时间间隔（每次都重新随机生成）
            rest_interval = elapsed_seconds + random.randint(sound_range_a * 60, sound_range_b * 60)

        
        # 等待1秒（所有状态都需要等待）
        time.sleep(1)
        total_seconds -= 1
        elapsed_seconds += 1
    

    print("恭喜你！专注时间结束，进入长休息！")
    play_sound("beep")
    


def main():
    """主函数"""
    print("欢迎使用专注时间管理器！")
    
    # 获取用户输入
    try:
        focus_time = int(input("请输入专注时间（分钟）: "))
        sound_range = input("请输入提示音随机范围（分钟），用空格分隔，例如 3 5 : ")
        # 解析随机范围输入
        try:
            sound_range_a, sound_range_b = map(int, sound_range.split())
        except ValueError:
            print("请输入有效的范围格式，例如: 3 5")
            return
        rest_duration = int(input("请输入微休息时间（秒）: "))
        
        # 检查输入的有效性
        if focus_time <= 0 or rest_duration <= 0 or sound_range_a <= 0 or sound_range_b <= 0:
            print("输入值必须为正整数！")
            return
        
        if sound_range_a > sound_range_b:
            print("提示音随机范围左边界必须小于等于右边界！")
            return
        
        # 播放开始专注的提示音
        play_sound("start_focus")
        
        # 开始倒计时
        countdown(focus_time, rest_duration, sound_range_a, sound_range_b)
        
    except ValueError:
        print("请输入有效的整数！")
    except KeyboardInterrupt:
        print("\n程序被用户中断")

if __name__ == "__main__":
    main()