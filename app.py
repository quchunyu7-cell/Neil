from flask import Flask, render_template_string, request, send_file
import matplotlib.pyplot as plt
import io
import numpy as np

# 已经移除: from scipy.interpolate import make_interp_spline

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = request.form.get("points")
        points = []
        for line in data.strip().split("\n"):
            try:
                # 检查并处理可能的空格，确保正确分割
                parts = line.split(',')
                if len(parts) != 2:
                    continue
                x_str, y_str = parts[0].strip(), parts[1].strip()
                x, y = float(x_str), float(y_str)
                points.append((x, y))
            except:
                continue

        # 至少需要两个点才能绘图
        if len(points) < 2:
            return "❌ 输入的点太少，至少需要输入两个有效坐标点！"

        # 按 x 排序
        points.sort()
        x_values = np.array([p[0] for p in points])
        y_values = np.array([p[1] for p in points])

        # --- 【关键修改：使用 NumPy 线性插值替代 SciPy 样条插值】 ---
        # 生成更多的 x 轴点
        x_smooth = np.linspace(x_values.min(), x_values.max(), 300)
        # 使用 numpy.interp 进行线性插值
        y_smooth = np.interp(x_smooth, x_values, y_values)

        # 绘制图像
        plt.figure(figsize=(6, 4))
        # 绘制平滑（线性插值）曲线
        plt.plot(x_smooth, y_smooth, 'r-', label="线性插值曲线")
        # 绘制原始点
        plt.plot(x_values, y_values, 'bo', label="原始点")

        plt.xlabel("X 轴")
        plt.ylabel("Y 轴")
        plt.title("曲线图 (线性插值)")
        plt.grid(True)
        plt.legend()

        # 保存到内存
        img_io = io.BytesIO()
        plt.savefig(img_io, format='png')
        img_io.seek(0)
        plt.close()  # 确保关闭 Matplotlib 对象，释放内存

        return send_file(img_io, mimetype='image/png')

    # GET 方法显示输入表单 + 示例
    html_content = '''
    <h2>输入点坐标 (x,y)，每行一个点</h2>
    <p>例如：</p>
    <pre>
0,0
1,2
2,3
3,2
4,0
    </pre>
    <form method="post">
        <textarea name="points" rows="10" cols="30"></textarea><br>
        <input type="submit" value="生成曲线图">
    </form>
    '''
    return render_template_string(html_content)

# 确保在生产环境移除 app.run()
# if __name__ == "__main__":
#     app.run(debug=True)
