import matplotlib.pyplot as plt

# 1. 输入点的坐标
print("请输入点的坐标，例如：1,2 （输入 'q' 结束）")
points = []
while True:
    s = input("请输入一个点坐标 (x,y)：")
    if s.lower() == 'q':
        break
    try:
        x_str, y_str = s.split(',')
        x, y = float(x_str), float(y_str)
        points.append((x, y))
    except:
        print("❌ 输入格式错误，请重新输入，例如：1.5,2.3")

# 检查是否输入了数据
if not points:
    print("未输入任何点，程序结束。")
    exit()

# 2. 分离X、Y坐标
points.sort()  # 按x排序，曲线会更平滑
x_values = [p[0] for p in points]
y_values = [p[1] for p in points]

# 3. 绘制曲线图
plt.figure(figsize=(8,6))

# 绘制曲线和点
plt.plot(x_values, y_values, 'bo-', label="输入点曲线")  # 蓝色圆点+连线

# 4. 添加坐标轴标签和标题
plt.xlabel("X 轴")
plt.ylabel("Y 轴")
plt.title("输入点生成的曲线图")

# 5. 显示网格
plt.grid(True, which='both', linestyle='--', linewidth=0.5)

# 6. 显示刻度值
plt.xticks(x_values)  # X 轴刻度对应输入点
plt.yticks(sorted(list(set(y_values))))  # Y 轴刻度去重并排序

# 7. 显示图例
plt.legend()

# 8. 显示图像
plt.show()
