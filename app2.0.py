import time
import random
import os
import sys

# 版本号：2.0
# 新增了对于剩余时间的可视化进度条🕒█░

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
    """倒计时功能 - 实现四种状态机显示效果"""
    total_seconds = minutes * 60
    rest_interval = random.randint(sound_range_a * 60, sound_range_b * 60)
    elapsed_seconds = 0
    
    # 状态定义
    STATE_FOCUS = 1  # 专注状态
    STATE_REST_ALERT = 2  # 短休息时间到
    STATE_RESTING = 3  # 休息中
    STATE_BACK_TO_FOCUS = 4  # 休息结束重新专注
    
    current_state = STATE_FOCUS
    
    def print_focus_line(remaining_seconds):
        """打印专注状态行 - 使用\r覆盖同一行"""
        mins, secs = divmod(remaining_seconds, 60)
        progress = elapsed_seconds / (minutes * 60)
        bar_length = 20
        filled = int(round(bar_length * progress))
        bar = '🕒' + '█' * filled + '░' * (bar_length - filled) + '🕔'
        time_format = f'{mins:02d}:{secs:02d}'
        print(f'\r⏳ 专注时间剩余：{time_format}  {bar}', end='', flush=True)
    
    def print_rest_alert():
        """打印短休息时间到 - 新起一行"""
        print('\n短暂休息时间到！', end='', flush=True)
    
    def print_resting_line(rest_seconds):
        """打印休息中状态 - 新起一行"""
        print(f'\n休息时间剩余：{rest_seconds}秒', end='', flush=True)
    
    def print_back_to_focus():
        """打印休息结束重新专注 - 新起一行"""
        print('\n休息结束，继续专注！', end='', flush=True)
    
    def clear_line():
        """清除当前行"""
        print('\r\033[K', end='', flush=True)
    
    def clear_n_lines(n):
        """清除n行内容"""
        for _ in range(n):
            print('\033[F\033[K', end='', flush=True)
    
    while total_seconds >= 0:
        if current_state == STATE_FOCUS:
            # 状态1：专注状态
            print_focus_line(total_seconds)
            
            # 检查是否需要切换到状态2（短休息时间到）
            if total_seconds > 0 and elapsed_seconds >= rest_interval:
                # 状态1 -> 状态2：短休息时间到
                current_state = STATE_REST_ALERT
                print_rest_alert()
                play_sound("rest_start")
                
                # 状态2 -> 状态3：进入休息中
                time.sleep(1)  # 给用户一点时间看到提醒
                clear_n_lines(1)  # 清除"短暂休息时间到！"这一行
                current_state = STATE_RESTING
                
                # 状态3：休息中
                rest_seconds = rest_duration
                while rest_seconds > 0:
                    print_focus_line(total_seconds)  # 保持显示专注时间
                    print_resting_line(rest_seconds)  # 显示休息倒计时
                    time.sleep(1)
                    rest_seconds -= 1
                    if rest_seconds > 0:
                        clear_n_lines(1)  # 清除"休息时间剩余"这一行
                
                # 状态3 -> 状态4：休息结束
                clear_n_lines(1)  # 清除"休息时间剩余"这一行
                current_state = STATE_BACK_TO_FOCUS
                print_focus_line(total_seconds)  # 重新显示专注时间
                print_back_to_focus()
                play_sound("rest_end")
                
                time.sleep(1)  # 给用户一点时间看到提示
                clear_n_lines(1)  # 清除"休息结束，继续专注！"这一行
                current_state = STATE_FOCUS
                
                # 重新设置下一个休息时间间隔
                rest_interval = elapsed_seconds + random.randint(sound_range_a * 60, sound_range_b * 60)
                
        elif current_state == STATE_REST_ALERT:
            # 状态2：短休息时间到
            print_focus_line(total_seconds)
            print_rest_alert()
            
        elif current_state == STATE_RESTING:
            # 状态3：休息中
            print_focus_line(total_seconds)
            print_resting_line(rest_duration)
            
        elif current_state == STATE_BACK_TO_FOCUS:
            # 状态4：休息结束重新专注
            print_focus_line(total_seconds)
            print_back_to_focus()
        
        # 等待1秒并更新计时
        time.sleep(1)
        total_seconds -= 1
        elapsed_seconds += 1
    
    # 专注时间结束
    print('\n🎉恭喜你！专注时间结束，进入长休息！')
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