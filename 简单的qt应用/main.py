# -*- coding: utf-8 -*-
import sys
import csv
import time
import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
import jieba
from wordcloud import WordCloud
from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox
from PySide6.QtCore import QThread, Signal

# 导入UI类
from mainwindow import Ui_mainWindow
from selecturl import Ui_dialog as Ui_SelectUrlDialog
from progress import Ui_Dialog as Ui_ProgressDialog


# ==================== 1. 选择网址的Dialog ====================
class SelectUrlDialog(QDialog, Ui_SelectUrlDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.selected_url = None
        
        self.buttonBox.accepted.connect(self.on_accept)
        self.buttonBox.rejected.connect(self.on_reject)
    
    def on_accept(self):
        if self.radioButton.isChecked():
            self.selected_url = "www.hupu.com"
        elif self.radioButton_2.isChecked():
            self.selected_url = "待更新"
        else:
            QMessageBox.warning(self, "提示", "请先选择一个目标网站！")
            return
        self.accept()
    
    def on_reject(self):
        self.selected_url = None
        self.reject()
    
    def get_selected_url(self):
        return self.selected_url


# ==================== 2. 爬虫工作线程 ====================
class CrawlWorker(QThread):
    progress_updated = Signal(int, str)
    finished = Signal()
    error_occurred = Signal(str)
    data_saved = Signal()
    
    def __init__(self, max_pages=21):
        super().__init__()
        self.max_pages = max_pages
        self.is_running = True
        self.is_paused = False
        self._is_finished = False  # 防止重复发送完成信号
    
    def pause(self):
        self.is_paused = True
    
    def resume(self):
        self.is_paused = False
    
    def stop(self):
        self.is_running = False
    
    def run(self):
        try:
            self.init_csv()
            self.progress_updated.emit(0, "开始爬取虎扑新闻...")
            
            for pageNo in range(1, self.max_pages + 1):
                if not self.is_running:
                    return
                
                while self.is_paused:
                    time.sleep(0.5)
                    if not self.is_running:
                        return
                
                self.progress_updated.emit(
                    int((pageNo - 1) / self.max_pages * 100),
                    f"正在爬取第 {pageNo}/{self.max_pages} 页..."
                )
                
                all_news = self.get_data(pageNo)
                self.save_csv(all_news)
                
                progress = int((pageNo / self.max_pages) * 100)
                self.progress_updated.emit(progress, f"已完成第 {pageNo}/{self.max_pages} 页")
            
            self.progress_updated.emit(100, "✅ 爬取完成！")
            self.data_saved.emit()
            
            # 防止重复发送finished信号
            if not self._is_finished:
                self._is_finished = True
                self.finished.emit()
            
        except Exception as e:
            self.error_occurred.emit(str(e))
    
    def get_data(self, pageNo):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        params = {'pageNo': pageNo, 'pageSize': '50'}
        url = 'https://www.hupu.com/home/v1/news'
        
        res = requests.get(url=url, headers=headers, params=params, timeout=10)
        res.raise_for_status()
        data = res.json()
        items = data['data']
        
        all_news = []
        for item in items:
            title = item.get('title', '无标题')
            topicName = item.get('topicName', '未知分区')
            content = item.get('content', '无内容')
            tid = item.get('tid', '')
            detail_url = f'https://bbs.hupu.com/{tid}.html' if tid else ''
            all_news.append([title, topicName, content, detail_url])
        
        time.sleep(0.5)
        return all_news
    
    def init_csv(self):
        with open('news.csv', 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['新闻标题', '新闻分区', '新闻内容', '新闻链接'])
    
    def save_csv(self, all_news):
        with open('news.csv', 'a', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(all_news)


# ==================== 3. 进度Dialog ====================
class ProgressDialog(QDialog, Ui_ProgressDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        self.progressBar.setValue(0)
        self.label_tip.setText("准备开始爬取...")
        self.start.setText("开始")
        
        self.worker = None
        self._is_finished = False  # 防止重复弹窗
        
        # 断开UI文件中的默认连接（关键修复）
        try:
            self.start.clicked.disconnect()
        except:
            pass
        
        # 重新连接
        self.start.clicked.connect(self.on_start_clicked)
    
    def on_start_clicked(self):
        if self.start.text() == "开始":
            self.start_crawling()
        elif self.start.text() == "暂停":
            self.pause_crawling()
        elif self.start.text() == "继续":
            self.resume_crawling()
    
    def start_crawling(self):
        # 重置完成标志
        self._is_finished = False
        
        self.start.setText("暂停")
        self.start.setEnabled(True)
        self.label_tip.setText("正在初始化...")
        self.progressBar.setValue(0)
        
        self.worker = CrawlWorker(max_pages=21)
        self.worker.progress_updated.connect(self.update_progress)
        self.worker.finished.connect(self.crawl_finished)
        self.worker.error_occurred.connect(self.crawl_error)
        self.worker.data_saved.connect(lambda: self.label_tip.setText("✅ 数据已保存至 news.csv"))
        self.worker.start()
    
    def pause_crawling(self):
        if self.worker:
            self.worker.pause()
            self.start.setText("继续")
            self.label_tip.setText("⏸️ 已暂停")
    
    def resume_crawling(self):
        if self.worker:
            self.worker.resume()
            self.start.setText("暂停")
            self.label_tip.setText("🔄 继续爬取...")
    
    def update_progress(self, value, message):
        self.progressBar.setValue(value)
        self.label_tip.setText(message)
    
    def crawl_finished(self):
        """爬取完成 - 确保只触发一次"""
        # 防止重复触发
        if self._is_finished:
            return
        self._is_finished = True
        
        self.start.setText("完成")
        self.start.setEnabled(False)
        self.label_tip.setText("✅ 所有数据爬取完成！")
        
        # 只弹一次窗
        QMessageBox.information(self, "成功", "数据爬取完成！\n已保存至 news.csv")
    
    def crawl_error(self, error_msg):
        self.start.setText("开始")
        self.start.setEnabled(True)
        self.label_tip.setText("❌ 爬取出错")
        QMessageBox.critical(self, "错误", error_msg)
    
    def closeEvent(self, event):
        if self.worker and self.worker.isRunning():
            self.worker.stop()
            self.worker.wait()
        event.accept()


# ==================== 4. 主窗口 ====================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 创建UI实例并设置
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)
        
        self.current_url = None
        self.progress_dialog = None
        
        # 初始化状态
        self.ui.sucecess.setText("就绪")
        self.ui.sucecess.setStyleSheet("color: gray;")
        
        # 断开UI文件中的信号连接（避免重复触发）
        try:
            self.ui.target_URL.clicked.disconnect()
        except:
            pass
        try:
            self.ui.data_get.clicked.disconnect()
        except:
            pass
        try:
            self.ui.generate_excel.clicked.disconnect()
        except:
            pass
        try:
            self.ui.generate_wordcloud.clicked.disconnect()
        except:
            pass
        
        # 重新连接信号
        self.ui.target_URL.clicked.connect(self.get_URL)
        self.ui.data_get.clicked.connect(self.data_get)
        self.ui.generate_excel.clicked.connect(self.generate_excel)
        self.ui.generate_wordcloud.clicked.connect(self.generate_wordcloud)
    
    def get_URL(self):
        """选择目标网站"""
        dialog = SelectUrlDialog(self)
        result = dialog.exec()
        
        if result == QDialog.Accepted:
            url = dialog.get_selected_url()
            if url:
                self.current_url = url
                self.ui.sucecess.setText(f"已选: {url}")
                self.ui.sucecess.setStyleSheet("color: green;")
            else:
                self.ui.sucecess.setText("未选择")
                self.ui.sucecess.setStyleSheet("color: orange;")
        else:
            self.ui.sucecess.setText("已取消")
            self.ui.sucecess.setStyleSheet("color: orange;")
    
    def data_get(self):
        """数据获取"""
        if not self.current_url:
            QMessageBox.warning(self, "提示", "请先选择目标网站！")
            return
        
        if self.progress_dialog and self.progress_dialog.isVisible():
            QMessageBox.information(self, "提示", "爬取窗口已打开")
            self.progress_dialog.raise_()
            self.progress_dialog.activateWindow()
            return
        
        self.progress_dialog = ProgressDialog(self)
        self.progress_dialog.finished.connect(
            lambda: setattr(self, 'progress_dialog', None)
        )
        self.progress_dialog.show()
    
    def generate_excel(self):
        """生成新闻分区占比饼状图"""
        try:
            if not os.path.exists('news.csv'):
                QMessageBox.warning(self, "提示", "未找到数据文件 news.csv！\n请先进行数据爬取。")
                return
            
            df = pd.read_csv('news.csv')
            if df.empty:
                QMessageBox.warning(self, "提示", "数据文件为空！\n请先进行数据爬取。")
                return
            
            plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
            plt.rcParams['axes.unicode_minus'] = False
            
            topic_counts = df['新闻分区'].value_counts().head(10)
            
            if len(topic_counts) == 0:
                QMessageBox.warning(self, "提示", "没有有效的数据可以生成图表！")
                return
            
            plt.figure(figsize=(10, 8))
            colors = plt.cm.Set3.colors
            plt.pie(
                topic_counts, 
                labels=topic_counts.index, 
                autopct='%1.1f%%',
                colors=colors,
                textprops={'fontsize': 10}
            )
            plt.title('虎扑新闻分区占比 (TOP 10)', fontsize=16)
            plt.axis('equal')
            
            plt.savefig('新闻分区占比饼图.png', dpi=300, bbox_inches='tight')
            plt.close()
            
            self.ui.sucecess.setText(f"✅ 饼图已生成！分区数: {len(topic_counts)}")
            self.ui.sucecess.setStyleSheet("color: green;")
            
            QMessageBox.information(
                self, 
                "成功", 
                f"饼状图已生成！\n包含 {len(topic_counts)} 个新闻分区\n保存为: 新闻分区占比饼图.png"
            )
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"生成图表失败：{str(e)}")
    
    def generate_wordcloud(self):
        """生成新闻标题高频词云图"""
        try:
            if not os.path.exists('news.csv'):
                QMessageBox.warning(self, "提示", "未找到数据文件 news.csv！\n请先进行数据爬取。")
                return
            
            df = pd.read_csv('news.csv')
            if df.empty:
                QMessageBox.warning(self, "提示", "数据文件为空！\n请先进行数据爬取。")
                return
            
            if not os.path.exists('stopwordscn.txt'):
                QMessageBox.warning(
                    self, 
                    "提示", 
                    "未找到停用词文件 stopwordscn.txt！\n"
                    "请在同目录下放置停用词文件。\n\n"
                    "如果没有，可以创建一个包含常见停用词的文本文件。"
                )
                return
            
            plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
            plt.rcParams['axes.unicode_minus'] = False
            
            with open('stopwordscn.txt', 'r', encoding='utf-8') as f:
                stopwords = [sw.strip() for sw in f.readlines()]
            
            title_str = ''.join(df['新闻标题'].astype(str))
            wordlist = jieba.cut(title_str)
            
            word_freq = {}
            for word in wordlist:
                if word not in stopwords and len(word) > 1:
                    word_freq[word] = word_freq.get(word, 0) + 1
            
            if not word_freq:
                QMessageBox.warning(self, "提示", "没有有效的高频词可以生成词云！")
                return
            
            high_freq_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:150]
            
            # 尝试多个可能的字体路径
            font_paths = [
                'simhei.ttf',
                'C:/Windows/Fonts/simhei.ttf',
                'C:/Windows/Fonts/SimHei.ttf',
                '/System/Library/Fonts/PingFang.ttc',  # macOS
                '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc'  # Linux
            ]
            
            font_path = None
            for path in font_paths:
                if os.path.exists(path):
                    font_path = path
                    break
            
            if not font_path:
                QMessageBox.warning(
                    self, 
                    "提示", 
                    "未找到中文字体文件！\n"
                    "请下载 simhei.ttf 放到程序目录，或安装中文字体。"
                )
                return
            
            wc = WordCloud(
                font_path=font_path,
                background_color='white',
                width=800,
                height=600,
                max_words=200
            )
            
            wc.generate_from_frequencies(dict(high_freq_words))
            
            plt.figure(figsize=(10, 7))
            plt.imshow(wc, interpolation='bilinear')
            plt.axis('off')
            
            plt.savefig('新闻标题高频词云图.png', dpi=300, bbox_inches='tight')
            plt.close()
            
            self.ui.sucecess.setText(f"✅ 词云图已生成！高频词数: {len(high_freq_words)}")
            self.ui.sucecess.setStyleSheet("color: green;")
            
            QMessageBox.information(
                self, 
                "成功", 
                f"词云图已生成！\n包含 {len(high_freq_words)} 个高频词\n保存为: 新闻标题高频词云图.png"
            )
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"生成词云失败：{str(e)}")


# ==================== 启动 ====================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
