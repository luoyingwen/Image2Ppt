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
                self.text1.set_text(f'点1: ({self.point1[0]}, {self.point1[1]})')
            else:
                self.point2 = [int(event.xdata), int(event.ydata)]
                self.text2.set_text(f'点2: ({self.point2[0]}, {self.point2[1]})')
            
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
        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        self.ax.imshow(self.img_rgb)
        self.ax.axis('off')
        
        # 设置第二个点的初始坐标为图片尺寸
        height, width = self.img_rgb.shape[:2]
        self.point2 = [width, height]
        
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
