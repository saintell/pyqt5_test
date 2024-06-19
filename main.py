import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QListWidget, QListWidgetItem,
    QMessageBox, QLabel, QInputDialog
)

class TaskManager(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Configura la ventana principal
        self.setWindowTitle('Gestor de Tareas')
        
        # Establece el tamaño inicial de la ventana
        self.resize(350, 250)

        # Crea el layout principal
        self.layout = QVBoxLayout()

        # Crea el layout para la entrada de nuevas tareas
        self.task_input_layout = QHBoxLayout()
        self.task_input = QLineEdit(self)
        self.task_input.setPlaceholderText('Ingrese una nueva tarea')
        self.add_task_button = QPushButton('Agregar Tarea', self)
        self.add_task_button.clicked.connect(self.add_task)

        self.task_input_layout.addWidget(self.task_input)
        self.task_input_layout.addWidget(self.add_task_button)

        # Crea el widget para la lista de tareas
        self.task_list = QListWidget(self)

        # Agrega los layouts y widgets al layout principal
        self.layout.addLayout(self.task_input_layout)
        self.layout.addWidget(self.task_list)

        self.setLayout(self.layout)

    def add_task(self):
        # Obtiene el texto de la tarea desde el campo de entrada
        task_text = self.task_input.text()
        if task_text.strip():
            # Crea un nuevo elemento de lista y su widget asociado
            task_item = QListWidgetItem()
            task_widget = self.create_task_widget(task_text, task_item)
            task_item.setSizeHint(task_widget.sizeHint())
            self.task_list.addItem(task_item)
            self.task_list.setItemWidget(task_item, task_widget)
            self.task_input.clear()
        else:
            # Muestra un mensaje de advertencia si la tarea está vacía
            QMessageBox.warning(self, 'Error', 'La tarea no puede estar vacía')

    def create_task_widget(self, task_text, task_item):
        # Crea el widget para una tarea
        item_widget = QWidget()
        item_layout = QHBoxLayout()

        # Crea una etiqueta para mostrar el texto de la tarea
        task_label = QLabel(task_text)
        item_layout.addWidget(task_label)

        # Botón para ver la tarea
        view_button = QPushButton('Ver')
        view_button.clicked.connect(lambda: self.view_task(task_label.text()))
        item_layout.addWidget(view_button)

        # Botón para editar la tarea
        edit_button = QPushButton('Editar')
        edit_button.clicked.connect(lambda: self.edit_task(task_label, task_item, item_widget))
        item_layout.addWidget(edit_button)

        # Botón para eliminar la tarea
        delete_button = QPushButton('Eliminar')
        delete_button.clicked.connect(lambda: self.remove_task(task_item))
        item_layout.addWidget(delete_button)

        item_widget.setLayout(item_layout)
        return item_widget

    def view_task(self, task_text):
        # Muestra un mensaje con los detalles de la tarea
        QMessageBox.information(self, 'Detalles de la Tarea', task_text)

    def edit_task(self, task_label, task_item, item_widget):
        # Abre un diálogo para editar el texto de la tarea
        task_text = task_label.text()
        new_task_text, ok = QInputDialog.getText(
            self, 'Editar Tarea', 'Modificar tarea:', QLineEdit.Normal, task_text
        )
        if ok and new_task_text.strip():
            # Actualiza el texto de la tarea si se ha modificado
            task_label.setText(new_task_text)
            self.update_task_widget(task_item, new_task_text, item_widget)
        elif ok and not new_task_text.strip():
            # Muestra un mensaje de advertencia si la tarea está vacía
            QMessageBox.warning(self, 'Error', 'La tarea no puede estar vacía')

    def update_task_widget(self, task_item, new_task_text, item_widget):
        # Elimina el widget anterior y crea uno nuevo con el texto actualizado
        row = self.task_list.row(task_item)
        new_task_item = QListWidgetItem()
        new_task_widget = self.create_task_widget(new_task_text, new_task_item)
        new_task_item.setSizeHint(new_task_widget.sizeHint())
        self.task_list.takeItem(row)
        self.task_list.insertItem(row, new_task_item)
        self.task_list.setItemWidget(new_task_item, new_task_widget)

    def remove_task(self, task_item):
        # Elimina la tarea de la lista
        row = self.task_list.row(task_item)
        self.task_list.takeItem(row)

if __name__ == '__main__':
    # Crea y ejecuta la aplicación
    app = QApplication(sys.argv)
    task_manager = TaskManager()
    task_manager.show()
    sys.exit(app.exec_())
