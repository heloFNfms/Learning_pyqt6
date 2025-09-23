"""
动画效果模块
提供各种界面动画效果
"""

from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QRect, QTimer, pyqtSignal, QObject, QSequentialAnimationGroup, QParallelAnimationGroup
from PyQt6.QtWidgets import QGraphicsOpacityEffect, QWidget, QGraphicsDropShadowEffect
from PyQt6.QtGui import QColor
import math

class AnimationManager(QObject):
    """动画管理器"""
    
    def __init__(self):
        super().__init__()
        
    def fade_in(self, widget, duration=300):
        """淡入动画"""
        self.opacity_effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(self.opacity_effect)
        
        self.fade_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_animation.setDuration(duration)
        self.fade_animation.setStartValue(0)
        self.fade_animation.setEndValue(1)
        self.fade_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.fade_animation.start()
        
    def fade_out(self, widget, duration=300):
        """淡出动画"""
        self.opacity_effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(self.opacity_effect)
        
        self.fade_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_animation.setDuration(duration)
        self.fade_animation.setStartValue(1)
        self.fade_animation.setEndValue(0)
        self.fade_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.fade_animation.start()
        
    def slide_in_from_left(self, widget, duration=400):
        """从左侧滑入"""
        start_pos = widget.pos()
        widget.move(start_pos.x() - widget.width(), start_pos.y())
        
        self.slide_animation = QPropertyAnimation(widget, b"pos")
        self.slide_animation.setDuration(duration)
        self.slide_animation.setStartValue(widget.pos())
        self.slide_animation.setEndValue(start_pos)
        self.slide_animation.setEasingCurve(QEasingCurve.Type.OutBack)
        self.slide_animation.start()
        
    def slide_in_from_right(self, widget, duration=400):
        """从右侧滑入"""
        start_pos = widget.pos()
        widget.move(start_pos.x() + widget.width(), start_pos.y())
        
        self.slide_animation = QPropertyAnimation(widget, b"pos")
        self.slide_animation.setDuration(duration)
        self.slide_animation.setStartValue(widget.pos())
        self.slide_animation.setEndValue(start_pos)
        self.slide_animation.setEasingCurve(QEasingCurve.Type.OutBack)
        self.slide_animation.start()
        
    def bounce_in(self, widget, duration=600):
        """弹跳进入动画"""
        original_size = widget.size()
        widget.resize(0, 0)
        
        self.bounce_animation = QPropertyAnimation(widget, b"size")
        self.bounce_animation.setDuration(duration)
        self.bounce_animation.setStartValue(widget.size())
        self.bounce_animation.setEndValue(original_size)
        self.bounce_animation.setEasingCurve(QEasingCurve.Type.OutBounce)
        self.bounce_animation.start()
        
    def pulse_effect(self, widget):
        """脉冲效果"""
        self.pulse_timer = QTimer()
        self.pulse_counter = 0
        
        def pulse():
            self.pulse_counter += 1
            opacity = 0.5 + 0.5 * abs(0.5 - (self.pulse_counter % 100) / 100.0)
            
            effect = QGraphicsOpacityEffect()
            effect.setOpacity(opacity)
            widget.setGraphicsEffect(effect)
            
            if self.pulse_counter >= 200:  # 停止脉冲
                self.pulse_timer.stop()
                widget.setGraphicsEffect(None)
                
        self.pulse_timer.timeout.connect(pulse)
        self.pulse_timer.start(50)
        
    def shake_effect(self, widget, duration=300):
        """简化的抖动效果"""
        # 使用透明度效果模拟抖动
        self.shake_timer = QTimer()
        self.shake_counter = 0
        
        def shake():
            self.shake_counter += 1
            opacity = 0.3 + 0.7 * abs(0.5 - (self.shake_counter % 20) / 20.0)
            
            effect = QGraphicsOpacityEffect()
            effect.setOpacity(opacity)
            widget.setGraphicsEffect(effect)
            
            if self.shake_counter >= 40:  # 停止抖动
                self.shake_timer.stop()
                widget.setGraphicsEffect(None)
                
        self.shake_timer.timeout.connect(shake)
        self.shake_timer.start(15)
        
    def glow_effect(self, widget, color=QColor(255, 255, 255, 100)):
        """发光效果"""
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(20)
        shadow_effect.setColor(color)
        shadow_effect.setOffset(0, 0)
        widget.setGraphicsEffect(shadow_effect)
        
        # 动画改变发光强度
        self.glow_timer = QTimer()
        self.glow_counter = 0
        
        def update_glow():
            self.glow_counter += 1
            intensity = 10 + 15 * (1 + math.sin(self.glow_counter * 0.2))
            shadow_effect.setBlurRadius(intensity)
            
            if self.glow_counter >= 100:  # 停止发光
                self.glow_timer.stop()
                widget.setGraphicsEffect(None)
                
        self.glow_timer.timeout.connect(update_glow)
        self.glow_timer.start(100)
        
    def float_up_down(self, widget, distance=3, duration=2000):
        """简化的上下漂浮效果"""
        # 使用透明度变化模拟浮动
        self.float_timer = QTimer()
        self.float_counter = 0
        
        def float_animate():
            self.float_counter += 1
            # 使用正弦波实现平滑的浮动效果
            opacity = 0.7 + 0.3 * abs(math.sin(self.float_counter * 0.1))
            
            effect = QGraphicsOpacityEffect()
            effect.setOpacity(opacity)
            widget.setGraphicsEffect(effect)
            
            # 继续动画直到被停止
            if self.float_counter >= 1000:
                self.float_counter = 0  # 重置计数器
                
        self.float_timer.timeout.connect(float_animate)
        self.float_timer.start(100)
        
    def scale_pulse(self, widget, scale_factor=1.1, duration=1000):
        """缩放脉冲效果"""
        # 放大动画
        scale_up = QPropertyAnimation(widget, b"size")
        scale_up.setDuration(duration // 2)
        scale_up.setStartValue(widget.size())
        scale_up.setEndValue(widget.size() * scale_factor)
        scale_up.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        # 缩小动画
        scale_down = QPropertyAnimation(widget, b"size")
        scale_down.setDuration(duration // 2)
        scale_down.setStartValue(scale_up.endValue())
        scale_down.setEndValue(widget.size())
        scale_down.setEasingCurve(QEasingCurve.Type.InCubic)
        
        # 组合动画
        self.scale_group = QSequentialAnimationGroup()
        self.scale_group.addAnimation(scale_up)
        self.scale_group.addAnimation(scale_down)
        self.scale_group.setLoopCount(3)  # 重复3次
        self.scale_group.start()

# 全局动画管理器实例
animation_manager = AnimationManager()