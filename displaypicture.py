import cv2
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from matplotlib.font_manager import FontProperties

class ImageViewer:
    def __init__(self, image_path):
        # 使用Path处理路径,支持中文路径
        self.image_path = Path(image_path)
        self.img = self._load_image()
        self.img_rgb = self._convert_to_rgb()
        self.fig = None
        self.ax = None
        # 设置中文字体
        self.font = FontProperties(fname=r'C:\Windows\Fonts\SimHei.ttf')
        # 初始化坐标点
        self.point1 = [0, 0]
        self.point2 = None  # 将在加载图片后设置
        self.text1 = None
        self.text2 = None
        
    def _load_image(self):
        """加载图片,处理异常"""
        img = cv2.imdecode(np.fromfile(str(self.image_path), dtype=np.uint8), cv2.IMREAD_COLOR)
        if img is None:
            raise FileNotFoundError(f"无法读取图片: {self.image_path}")
        return img
        
    def _convert_to_rgb(self):
        """将BGR转换为RGB格式"""
        return cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
    
    def _on_click(self, event):
        """处理鼠标点击事件"""
        if event.button == 3:  # 右键点击
            # 计算点击位置与两个点的距离
            dist1 = np.sqrt((event.xdata - self.point1[0])**2 + (event.ydata - self.point1[1])**2)
            dist2 = np.sqrt((event.xdata - self.point2[0])**2 + (event.ydata - self.point2[1])**2)
            
            # 更新距离最近的点
            if dist1 < dist2:
                self.point1 = [int(event.xdata), int(event.ydata)]
                self.text1.set_text(f'左上角: ({self.point1[0]}, {self.point1[1]})')
            else:
                self.point2 = [int(event.xdata), int(event.ydata)]
                self.text2.set_text(f'右下角: ({self.point2[0]}, {self.point2[1]})')
            self.fig.canvas.draw()
    
    def _on_close(self, event):
        """处理窗口关闭事件"""
        print("\n图片已关闭")
        print(f"左上角坐标: ({self.point1[0]}, {self.point1[1]})")
        print(f"右下角坐标: ({self.point2[0]}, {self.point2[1]})")
    
    def get_coordinates(self):
        """返回当前选择的坐标"""
        return (self.point1, self.point2)
    
    def show(self):
        """显示图片并返回选择的坐标"""
        # 获取屏幕尺寸
        import tkinter as tk
        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight() - 100  # 减去任务栏和标题栏的高度
        root.destroy()  # 关闭临时窗口
        
        # 获取图像尺寸
        height, width = self.img_rgb.shape[:2]
        
        # 计算图像缩放比例，确保图像完全适应屏幕
        # 考虑到matplotlib图像的边距和其他元素，使用较小的值
        scale_width = (screen_width * 0.85) / width
        scale_height = (screen_height * 0.85) / height
        scale = min(scale_width, scale_height)  # 选择较小的缩放比例，确保完全显示
        
        # 计算适当的figsize (英寸)
        # matplotlib的默认DPI是100，所以需要将像素转换为英寸
        dpi = 100
        fig_width = (width * scale) / dpi
        fig_height = (height * scale) / dpi
        
        print(f"屏幕尺寸: {screen_width}x{screen_height}，图片尺寸: {width}x{height}")
        print(f"使用缩放比例: {scale:.2f}，图形尺寸: {fig_width:.2f}x{fig_height:.2f}英寸")
        
        # 创建图形，使用计算出的尺寸
        self.fig, self.ax = plt.subplots(figsize=(fig_width, fig_height))
        self.ax.imshow(self.img_rgb)
        self.ax.axis('off')
        
        # 设置第二个点的初始坐标为图片尺寸
        self.point2 = [width, height]
        
        # 设置窗口最大化
        try:
            # 获取当前图形的管理器
            mng = plt.get_current_fig_manager()
            # 获取matplotlib使用的后端
            backend = plt.get_backend().lower()
            print(f"当前使用的Matplotlib后端: {backend}")
            
            # 在Windows下使用不同方法最大化窗口
            if 'tk' in backend:  # TkAgg后端
                # 获取Tk的根窗口然后最大化
                root = mng.window.winfo_toplevel()
                # 以下是根据不同系统最大化窗口的通用方法
                # Windows系统
                root.state('zoomed')  # Windows特定
                print("已使用Tk后端的zoomed状态最大化窗口")
            elif 'qt' in backend:  # Qt后端
                mng.window.showMaximized()
                print("已使用Qt后端的showMaximized方法最大化窗口")
            elif hasattr(mng, 'frame'):  # WxAgg后端
                mng.frame.Maximize(True)
                print("已使用WxAgg后端的Maximize方法最大化窗口")
            elif hasattr(mng, 'resize'):  # 通用方法
                # 获取屏幕尺寸并设置窗口大小
                import tkinter as tk
                root = tk.Tk()
                width = root.winfo_screenwidth()
                height = root.winfo_screenheight()
                root.withdraw()  # 不显示这个临时窗口
                mng.resize(width, height)
                print(f"已将窗口大小调整为屏幕尺寸: {width}x{height}")
            elif hasattr(mng, 'full_screen_toggle'):
                mng.full_screen_toggle()
                print("已切换全屏模式")
            else:
                print(f"未知的后端 {backend}，请手动最大化窗口")
        except Exception as e:
            print(f"无法最大化窗口 (使用后端: {backend}): {str(e)}，请手动最大化")
            # 错误不影响主要功能
        
        # 添加文本框
        # 在图像外部添加文本框
        self.text1 = plt.figtext(0.02, 0.95, f'左上角: ({self.point1[0]}, {self.point1[1]})', 
                                color='red', fontproperties=self.font, fontsize=12,
                                bbox=dict(facecolor='white', alpha=0.7))
        self.text2 = plt.figtext(0.02, 0.90, f'右下角: ({self.point2[0]}, {self.point2[1]})', 
                                color='red', fontproperties=self.font, fontsize=12,
                                bbox=dict(facecolor='white', alpha=0.7))
        # 添加提示文本
        plt.figtext(0.02, 0.85, '右键点击更新坐标', color='blue', 
                    fontproperties=self.font, fontsize=10,
                    bbox=dict(facecolor='white', alpha=0.7))
        
        # 添加标题,使用中文字体
        plt.suptitle(f'图片查看器 - {self.image_path.name}', fontsize=12, fontproperties=self.font)
        
        # 绑定鼠标点击事件和窗口关闭事件
        self.fig.canvas.mpl_connect('button_press_event', self._on_click)
        self.fig.canvas.mpl_connect('close_event', self._on_close)
        
        plt.show()
        return self.get_coordinates()

if __name__ == '__main__':
    # 创建图片查看器实例并显示
    viewer = ImageViewer('1.png')
    coordinates = viewer.show()
    print("\n返回的坐标:")
    print(f"左上角坐标: {coordinates[0]}")
    print(f"右下角坐标: {coordinates[1]}")
    