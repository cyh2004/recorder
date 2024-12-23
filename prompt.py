import tkinter as tk

result = False

def ask_retry():
    global result
    # 创建根窗口
    root = tk.Tk()
    root.title("重试询问")  # 设置窗口标题

    # 获取屏幕宽度和高度
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # 设置窗口大小
    window_width = 300
    window_height = 150

    # 计算窗口位置，使其居中
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)

    # 设置窗口的初始位置和大小
    root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

    # 定义按钮点击事件
    def on_yes():
        global result
        result = True
        root.quit()  # 退出主循环

    def on_no():
        global result
        result = False
        root.quit()  # 退出主循环

    # 创建标签，显示问题
    label = tk.Label(root, text="是否重试?", font=("Arial", 14))
    label.pack(pady=20)  # 设置标签的间距

    # 创建“是”按钮
    yes_button = tk.Button(root, text="是", width=10, command=on_yes)
    yes_button.pack(side=tk.LEFT, padx=30, pady=10)

    # 创建“否”按钮
    no_button = tk.Button(root, text="否", width=10, command=on_no)
    no_button.pack(side=tk.RIGHT, padx=30, pady=10)

    # 启动 tkinter 事件循环
    root.mainloop()

    return result

if __name__ == '__main__':
    result = ask_retry()
    print(f"选择了：{result}")