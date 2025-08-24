import time
import random
import os
import sys

# 版本号：1.0

def play_sound(sound_type="beep"):
    """播放提示音"""
    # macOS系统使用系统声音
    if sys.platform == "darwin":
        if sound_type == "beep":
            # 进入长休息音效
            os.system("afplay /System/Library/Sounds/Glass.aiff")
        elif sound_type == "start_focus":
            # 开始专注的音效
            os.system("afplay /System/Library/Sounds/Submarine.aiff")
        elif sound_type == "rest_start":
            # 进入短休息的音效
            os.system("afplay /System/Library/Sounds/Blow.aiff")
        else:
            # 结束短休息的音效
            os.system("afplay /System/Library/Sounds/Pop.aiff")
    # Linux系统使用系统声音
    elif sys.platform.startswith("linux"):
        if sound_type == "rest_start":
            os.system("paplay /usr/share/sounds/freedesktop/stereo/message-new-instant.oga 2>/dev/null || echo -e '\a'")
        elif sound_type == "rest_end":
            os.system("paplay /usr/share/sounds/freedesktop/stereo/complete.oga 2>/dev/null || echo -e '\a\a'")
        else:
            os.system("paplay /usr/share/sounds/freedesktop/stereo/bell.oga 2>/dev/null || echo -e '\a'")
    # Windows系统使用系统声音
    elif sys.platform == "win32":
        try:
            import winsound
            if sound_type == "beep":
                winsound.Beep(800, 300)  # 频率800Hz，持续300毫秒
            elif sound_type == "rest_start":
                winsound.Beep(1000, 500)  # 频率1000Hz，持续500毫秒
            else:
                winsound.Beep(1200, 700)  # 频率1200Hz，持续700毫秒
        except ImportError:
            if sound_type == "rest_end":
                print("\a\a", end='', flush=True)
            else:
                print("\a", end='', flush=True)
    # 其他系统使用系统蜂鸣
    else:
        if sound_type == "rest_end":
            print("\a\a", end='', flush=True)
        else:
            print("\a", end='', flush=True)

def countdown(minutes, rest_duration, sound_range_a, sound_range_b):
    """倒计时功能"""
    total_seconds = minutes * 60
    # 将分钟转换为秒
    rest_interval = random.randint(sound_range_a * 60, sound_range_b * 60)
    # 记录已过去的秒数
    elapsed_seconds = 0
    
    while total_seconds >= 0:
        # 显示剩余时间
        mins, secs = divmod(total_seconds, 60)
        progress = elapsed_seconds / (minutes * 60)
        bar_length = 20
        filled = int(round(bar_length * progress))
        bar = '🕒' + '█' * filled + '░' * (bar_length - filled) + '🕔'
        percent = f'{progress:.0%}'
        time_format = f'{mins:02d}:{secs:02d}'
        print(f'\r⏳ 专注时间剩余：{time_format}  {bar}', end='', flush=True)
        
        # 等待1秒
        time.sleep(1)
        total_seconds -= 1
        elapsed_seconds += 1
        
        # 检查是否需要播放休息提示音
        if total_seconds > 0 and elapsed_seconds >= rest_interval:
            print("\n短暂休息时间到！")
            play_sound("rest_start")  # 进入短休息的音效
            
            # 等待微休息时间
            rest_seconds = rest_duration
            while rest_seconds > 0:
                print(f'\r休息时间剩余: {rest_seconds:02d}秒', end='', flush=True)
                time.sleep(1)
                rest_seconds -= 1
            
            print("\r", end='', flush=True)  # 清除休息时间显示
            print("休息结束，继续专注！")
            play_sound("rest_end")  # 结束短休息的音效
            
            # 重新设置下一个休息时间间隔（每次都重新随机生成）
            rest_interval = elapsed_seconds + random.randint(sound_range_a * 60, sound_range_b * 60)
    
    print("\n恭喜你！专注时间结束，进入长休息！")
    # 连续播放6声提示音
    for i in range(6):
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