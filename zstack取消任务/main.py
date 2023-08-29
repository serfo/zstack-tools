import sys
import requests
import json
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QVBoxLayout


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Zstack结束任务小工具')
        self.setGeometry(300, 300, 400, 400)
        layout = QVBoxLayout()

        ip_label = QLabel('IP地址:                                无需填写端口，默认5000')
        self.ip_input = QLineEdit()

        uuid_label = QLabel('任务UUID:')
        self.uuid_input = QLineEdit()

        self.result_text = QTextEdit()
        self.confirm_button = QPushButton('确定')
        self.confirm_button.clicked.connect(self.on_confirm_button_clicked)

        layout.addWidget(ip_label)
        layout.addWidget(self.ip_input)
        layout.addWidget(uuid_label)
        layout.addWidget(self.uuid_input)
        layout.addWidget(self.result_text)
        layout.addWidget(self.confirm_button)

        self.setLayout(layout)

    def request_api(self, ip, uuid):
        url = f'http://{ip}:5000/api/operation/action/cancel?actionId={uuid}'
        res = requests.get(url)
        data = json.loads(res.text)
        return data

    def on_confirm_button_clicked(self):
        ip = self.ip_input.text()
        uuid = self.uuid_input.text()

        if ip == '' or uuid == '':
            err = 'IP地址或UUID不能为空'
            return self.result_text.setText(err)
        else:
            try:
                data = self.request_api(ip, uuid)
                if data['success'] == True:
                    name = '请求任务名称: ' + data['action']['name']
                    userName = '请求用户名称: ' + data['action']["userName"]
                    loginIp = '任务用户 IP: ' + data['action']["loginIp"]
                    status = '取消任务结果: ' + data['action']["status"]
                    result = f'IP地址: {ip}\n' \
                             f'UUID: {uuid}\n' \
                             f'-----------------------------------------------------------------\n'
                    self.result_text.setText(result + name + '\n' + userName + '\n' + loginIp + '\n' + status)
                elif data['success'] == False:
                    status = '请求状态：' + str(data['success'])
                    err = '\n错误信息：' + data["error"]
                    return self.result_text.setText(status + err)
            except Exception as e:
                err = '捕获到异常，请检查IP地址或UUID是否正确\n' + '错误信息：' + str(e)
                return self.result_text.setText(err)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()

    # 设置QSS样式
    qss = '''
        QWidget {
            background-color: #f0f0f0;
        }

        QLabel {
            font-size: 14px;
            color: #333;
        }

        QLineEdit {
            padding: 6px;
            border: 1px solid #aaa;
            border-radius: 3px;
        }

        QPushButton {
            padding: 8px 16px;
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 3px;
        }

        QTextEdit {
            padding: 6px;
            border: 1px solid #aaa;
            border-radius: 3px;
        }
    '''
    app.setStyleSheet(qss)

    window.show()
    sys.exit(app.exec_())
