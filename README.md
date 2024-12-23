# Usage
```python
python record.py
```

运行程序后，**连续**按两下‘ctrl’键可开始录制轨迹；再次连续按下两次‘ctrl’键后，任意按下一个键并移动一下鼠标即可退出录制（是为了给键鼠的 listener 分别发送信号）

# Note

每次完成动作后，会等待 1 秒再截图

# Action 格式

- `type`: `mouse` or `keyboard`
- `action`: 
    
    - 对于 `mouse` 有 `click`, `drag`, `scroll`, `hover`。
        - `hover` 的记录要求鼠标移动后静止 3s
        - `drag` 则是抬起鼠标即可捕获
    - 对于 `keyboard` 有 `hotkey`, `text_input`, `press`
        - 如果有 {'ctrl', 'alt', 'cmd', 'shift'} 中的键被按下，则其它无论哪个键被按下，都视为 hotkey
        - 否则如果有能输入文本的键被按下，则视为 text_input，当 enter 被按下，或一定时间没有输入后，记录一段 text_input
        - 否则记录一次 press

- `point`: { `x`: 1000, `y`: 500, `relative_x`: 0.5, `relative_y`: 0.3} 
    - `click` 和 `hover` 拥有此项
    - 以像素为单位，屏幕左上角为原点，向右为 x 轴，向下为 y 轴
- `point_from`: { `x`: 1000, `y`: 500, `relative_x`: 0.5, `relative_y`: 0.3} 
    - `drag` 拥有此项
- `point_to`: { `x`: 1000, `y`: 500, `relative_x`: 0.5, `relative_y`: 0.3} 
    - `drag` 拥有此项
- `scroll`: {`point`: `delta_x`: `delta_y`: }
    - `point`: 进行滚动时鼠标所在的位置, 值与上述 `point` 一致
    - `delta_x`:  横向滚动量，正数表示向右滚动，负数向左
    - `delta_y`:  纵向滚动量，正数表示向上滚动，负数向下
- `keys_pressed`: ["ctrl", "c"]
    - `hotkey` 和 `press` 拥有此项，`action` 为 `press` 时，此值长度恒为 1
- `text`: "1145141919810"
    - `text_input` 拥有此项

- `screenshot_before`: "000010_key_press_esc_before.png"
- `screenshot_after`: "000010_key_press_esc_after.png"
- `width`: 窗口宽度
- `height`: 窗口高度
