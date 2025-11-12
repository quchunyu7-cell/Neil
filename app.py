from flask import Flask, render_template_string, request, send_file
import matplotlib.pyplot as plt
import io
import numpy as np
from scipy.interpolate import make_interp_spline

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = request.form.get("points")
        points = []
        for line in data.strip().split("\n"):
            try:
                x_str, y_str = line.split(",")
                x, y = float(x_str), float(y_str)
                points.append((x, y))
            except:
                continue
        if not points:
            return "❌ 输入无效，请按照格式输入有效坐标！"

        # 按 x 排序
        points.sort()
        x_values = [p[0] for p in points]
        y_values = [p[1] for p in points]

        # 平滑曲线
        x_smooth = np.linspace(min(x_values), max(x_values), 300)
        spl = make_interp_spline(x_values, y_values, k=3)
        y_smooth = spl(x_smooth)

        # 绘制图像
        plt.figure(figsize=(6, 4))
        plt.plot(x_smooth, y_smooth, 'r-', label="平滑曲线")
        plt.plot(x_values, y_values, 'bo', label="原始点")
        plt.xlabel("X 轴")
        plt.ylabel("Y 轴")
        plt.title("曲线图")
        plt.grid(True)
        plt.legend()

        # 保存到内存
        img_io = io.BytesIO()
        plt.savefig(img_io, format='png')
        img_io.seek(0)
        plt.close()

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


if __name__ == "__main__":
    app.run(debug=True)
