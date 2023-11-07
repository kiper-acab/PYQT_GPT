# Для начала скачаем нужные нам библиотеки
# pip install os-sys
# pip install PyQt5
# pip install openai

# импортируем библиотеки 
import sys
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QDialog, QVBoxLayout, QTextEdit, QPushButton
from PyQt6 import QtGui, uic
import openai

# Создаём класс
class ChatgptBot(QMainWindow):
    def __init__(self):
        super().__init__()
        # инициальзируем нашу разметку
        uic.loadUi('my.ui', self)
        # устанавливаем заголовок для нашего приложения
        self.setWindowTitle('ChatGpt-bot version 3')
        # добавляем api openai
        self.key = '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'
        openai.api_key = self.key
        # инициализируем UI
        self.initUI()
    
    
    def initUI(self):
        # делаем иконку для приложения
        self.setWindowIcon(QtGui.QIcon('chatgpt.jpg'))
        # запрещаем пользователю изменять размер окна
        self.setFixedSize(802, 640)
        # делаем событие нажатия на кнопку
        self.pushButton.clicked.connect(self.req)
        # загружаем фото и передвигаем его на нужное место
        self.pixmap = QPixmap('logo.png')
        self.image = QLabel(self)
        self.image.move(270, 0)
        self.image.resize(64, 60)
        self.image.setPixmap(self.pixmap)
        # Чтобы было удобнее, мы делаем перенос строк в qlistwidget если они выходят за границы
        self.listWidget.setWordWrap(True)
        # делаем диалоговое окно и настраиваем для того чтобы узнать как обращаться к пользователю
        self.dialog = QDialog(self)
        self.dialog.setWindowTitle("Как к вам обращаться?")
        self.dialog.setFixedSize(300, 100)
        self.layout = QVBoxLayout(self.dialog)
        self.label = QLabel("Введите ваше имя или как к вам обращаться:")
        # настраиваем стили
        self.label.setStyleSheet('''background-color: rgba(255, 255, 255, 60);
                                        border: 1px solid rgba(255, 255, 255, 40);
                                        border-radius: 10%;''')
        self.line_edit = QTextEdit()
        self.line_edit.setStyleSheet('''background-color: rgba(255, 255, 255, 60);
                                        border: 1px solid rgba(255, 255, 255, 40);
                                        border-radius: 7p;''')
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.line_edit)
        self.ok_button = QPushButton("OK")
        self.ok_button.setStyleSheet('''background-color: rgba(255, 255, 255, 60);
                                        border-radius: 100px;
                                        border-color: 1px rgb(255, 255, 255);''')
        self.ok_button.clicked.connect(self.dialog.accept)
        self.layout.addWidget(self.ok_button)
        self.pushButton.setStyleSheet('''border-color: 1px rgb(255, 255, 255);''')
        self.dialog.exec()
        # делаем штуку чтобы можно было копировать
        self.listWidget.itemClicked.connect(self.copy_selected_item)

        # устанавливаем имя пользователя 
        if self.line_edit.toPlainText().replace(' ', '') ==  '':
            self.user_name = "Пользователь"
        else:
            self.user_name = self.line_edit.toPlainText().replace('\n', ' ')
    # делаем функцию для получения ответа от chatgpt
    def chatgpt_conversation(self, conversation_log):
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=conversation_log
        )
        conversation_log.append({
            'role': response.choices[0].message.role, 
            'content': response.choices[0].message.content.strip()
        })
        return conversation_log

    # Делаем функию для того чтобы добавить ответ от Chatgpt в qlistwidget
    def req(self):
        self.request = self.textEdit.toPlainText()
        
        # Проверяем написал ли что то пользователь, если нет, то не отправляем запрос в chatgpt
        if self.request != '':
            # добавляем ответ пользователя в qlistwidget
            self.listWidget.addItem(f'{self.user_name}: {self.request}')

            self.conversations = []
            self.question = self.textEdit.toPlainText()
            self.conversations.append({'role': 'user', 'content': self.question})
            self.conversations = self.chatgpt_conversation(self.conversations)
            self.final = self.conversations[-1]['content'].strip()
            self.listWidget.addItem(f'ChatGpt: {self.final}')
            # сбрасываем то что было написано в textedit
            self.textEdit.setText('')
            
    # добавляем функцию для копирования текста
    def copy_selected_item(self):
        # Получаем выбранный элемент из QListWidget
        selected_item = self.listWidget.currentItem()
        if selected_item:
            # Получаем текст выбранного элемента
            text_to_copy = selected_item.text()
            # Копируем текст в буфер обмена
            clipboard = QApplication.clipboard()
            clipboard.setText(text_to_copy)

# запускаем код
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ChatgptBot()
    ex.show()
    sys.exit(app.exec())