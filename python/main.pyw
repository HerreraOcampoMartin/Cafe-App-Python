from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import myPalette
import os
import sqlite3

#--------------START APP------------

class Main():

    def __init__(self):
        self.startApp()

    #----METHODS----

    def startApp(self):

        #App
        self.app = QApplication([])
        self.app.setStyle("Fusion")
        self.app.setPalette(myPalette.getPalette())
        self.app.setWindowIcon(QIcon(os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "../img/coffee.png"))
        self.app.setApplicationName("Cafe")

        #Window
        self.window = QWidget()
        self.window.resize(800, 600)
        self.window.showMaximized()

        #------------------------TOP-----------------------------

        self.menu = QWidget()

        self.newProduct = QPushButton(QIcon(os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "../img/addProduct.png"), "Nuevo Producto")
        self.newProduct.clicked.connect(self.addProdEvent)

        self.deleteProduct = QPushButton(QIcon(os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "../img/removeProduct.png"), "Eliminar producto")
        self.deleteProduct.clicked.connect(self.removeProdEvent)

        self.resetApp = QPushButton(QIcon(os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "../img/reset.png"), "Reset")
        self.resetApp.clicked.connect(self.resetEvent)

        self.menuLayout = QHBoxLayout(self.menu)
        self.menuLayout.addWidget(self.newProduct)
        self.menuLayout.addWidget(self.deleteProduct)
        self.menuLayout.addWidget(self.resetApp)

        #------------------------TABLE-----------------------------
 
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers) 
        self.header = self.table.horizontalHeader()
        self.table.setHorizontalHeaderLabels(("ID:;CLIENTE:;PEDIDO:;PRECIO:").split(";"))
        self.header.setSectionResizeMode(1, QHeaderView.Stretch)
        self.header.setSectionResizeMode(2, QHeaderView.Stretch)
        self.header.setSectionResizeMode(3, QHeaderView.Stretch)

        self.fillTable()

        #---------------------------BUTTONS---------------------

        self.buttonsWindow = QWidget(self.window)

        self.add = QPushButton(QIcon(os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "../img/add.png"), "Añadir")

        self.remove = QPushButton(QIcon(os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "../img/delete.png"), "Cancelar pedido")

        self.edit = QPushButton(QIcon(os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "../img/edit.png"), "Editar")

        #self.buy = QPushButton(QIcon(os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "../img/buy.png"), "Entregar")

        self.buttonsLayout = QHBoxLayout(self.buttonsWindow)
        self.buttonsLayout.addWidget(self.add)
        self.buttonsLayout.addWidget(self.remove)
        self.buttonsLayout.addWidget(self.edit)
        #self.buttonsLayout.addWidget(self.buy)

        self.add.clicked.connect(self.eventAdd)
        self.remove.clicked.connect(self.removeEvent)
        self.edit.clicked.connect(self.editEvent)
        #self.buy.clicked.connect(self.editEvent)

        #--------------------------LAYOUT---------------------

        self.layout = QGridLayout(self.window)
        self.layout.addWidget(self.menu, 0, 0)
        self.layout.addWidget(self.table, 1, 0)
        self.layout.addWidget(self.buttonsWindow, 2, 0)

        self.newProduct.setStyleSheet("background-color: white; color: black;")
        self.deleteProduct.setStyleSheet("background-color: white; color: black;")
        self.resetApp.setStyleSheet("background-color: white; color: black;")

        #Exec
        self.window.show()
        self.app.exec_()

    def eventAdd(self):
        dialog = QDialog()
        dialog.setWindowTitle("Añadir")
        dialog.setStyleSheet("QLabel{ text-decoration: underline; }")

        def cancel():
            dialog.close()

        def accept():
            clientName = client.text()
            clientOrder = order.currentText()

            if (clientName != None  and clientName != "" and clientOrder != None and clientOrder != ""):
                conn = sqlite3.connect("DB/db")
                cursor = conn.cursor()

                cursor.execute("SELECT Price FROM products WHERE Product='" + clientOrder + "'")
                values = cursor.fetchall()

                cursor = conn.cursor()

                array = (clientName, clientOrder, int(values[0][0]))

                cursor.execute("INSERT INTO orders VALUES (null, ?, ?, ?)", array)

                cursor = conn.cursor()
                cursor.execute("SELECT * FROM orders")

                _id = cursor.lastrowid

                cursor.close()

                conn.commit()
                conn.close()

                self.table.setRowCount(self.i+1)
                self.table.setItem(self.i, 0, QTableWidgetItem(str(_id)))
                self.table.setItem(self.i, 1, QTableWidgetItem(array[0]))
                self.table.setItem(self.i, 2, QTableWidgetItem(array[1]))
                self.table.setItem(self.i, 3, QTableWidgetItem(str(array[2])))
                
                self.i += 1

                QMessageBox.information(None, "Pedido insertado", "Pedido almacenado con éxito.")

            else:
                QMessageBox.information(None, "Error", "Rellene todos los campos de texto.")

            cancel()

        title = QLabel("Añadir pedido")
        title.setFont(QFont("Verdana", 16))
        title.setAlignment(Qt.AlignCenter)

        lblClient = QLabel("Nombre del cliente:")
        client = QLineEdit()
        lblOrder = QLabel("Pedido:")
        order = QComboBox()
        
        conn = sqlite3.connect("DB/db")
        cursor = conn.cursor()
        products = cursor.execute("SELECT * FROM products")

        for p in products:
            order.addItem(p[0])

        conn.commit()
        conn.close()
        
        submitButton = QPushButton("Aceptar")
        submitButton.clicked.connect(accept)

        cancelButton = QPushButton("Cancelar")
        cancelButton.clicked.connect(cancel)

        buttonsLayout = QHBoxLayout()
        buttonsLayout.addWidget(submitButton)
        buttonsLayout.addWidget(cancelButton)

        layout = QVBoxLayout(dialog)
        layout.addWidget(title)
        layout.addWidget(lblClient)
        layout.addWidget(client)
        layout.addWidget(lblOrder)
        layout.addWidget(order)
        layout.addLayout(buttonsLayout)

        dialog.setMinimumSize(225, 180)
        dialog.setMaximumSize(225, 180)
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.exec_()

    def fillTable(self):
        conn = sqlite3.connect("DB/db")
        cursor = conn.cursor()

        orders = cursor.execute("SELECT * FROM orders")

        self.i = 0

        for order in orders:
            self.table.setRowCount(self.i+1)
            self.table.setItem(self.i, 0, QTableWidgetItem(str(order[0])))
            self.table.setItem(self.i, 1, QTableWidgetItem(order[1]))
            self.table.setItem(self.i, 2, QTableWidgetItem(order[2]))
            self.table.setItem(self.i, 3, QTableWidgetItem(str(order[3])))
            self.i += 1

        conn.close()

    def removeEvent(self):
        try:
            conn = sqlite3.connect("DB/db")
            cursor = conn.cursor()

            array = self.table.selectedItems()

            if len(array):
                for e in array:
                    sql = "DELETE FROM orders WHERE ID=" + e.text()
                    cursor.execute(sql)
                    self.table.removeRow(int(e.row()))
                    self.i -= 1
                    conn.commit()

                conn.close()

                QMessageBox.information(None, "Eliminado", "Pedido eliminado con éxito.")
            else:
                QMessageBox.information(None, "Error", "Seleccione el ID del campo a eliminar.")

        except:
            QMessageBox.information(None, "Error", "Seleccione el ID del campo a eliminar.")

    def editEvent(self):
        try:
            
            row = self.table.selectedItems()[0].row()
            
            storage1 = self.table.item(row, 1)
            storage2 = self.table.item(row, 2)
            storage3 = self.table.item(row, 3)

            _id = self.table.item(row, 0).text()
            cell1 = storage1.text()
            cell2 = storage2.text()
            cell3 = storage3.text()

            dialog = QDialog()
            dialog.setWindowTitle("Editar")
            dialog.setStyleSheet("QLabel{ text-decoration: underline; }")

            def cancel():
                dialog.close()

            lblClient = QLabel("Nombre del cliente:")
            client = QLineEdit(cell1)

            lblOrder = QLabel("Pedido:")
            order = QComboBox()
            order.addItem(cell2)
            
            conn = sqlite3.connect("DB/db")
            cursor = conn.cursor()
            products = cursor.execute("SELECT * FROM products")

            for p in products:
                order.addItem(p[0])

            conn.commit()
            conn.close()
            
            lblPrice = QLabel("Precio:")
            orderPrice = QLineEdit(cell3)

            def accept():

                clientVal = client.text()
                orderVal = order.currentText()
                priceVal = orderPrice.text()

                if(clientVal != "" and clientVal != None and orderVal != "" and orderVal != None and priceVal != "" and priceVal != None):
                    array = [
                        clientVal,
                        orderVal,
                        priceVal,
                        _id
                    ]

                    conn = sqlite3.connect("DB/db")
                    cursor = conn.cursor()

                    cursor.execute("UPDATE orders SET Client=?, Product=?, Price=? WHERE ID=?", array)

                    conn.commit()
                    conn.close()

                    storage1.setText(array[0])
                    storage2.setText(array[1])
                    storage3.setText(array[2])

                    QMessageBox.information(None, "Editado", "Registro editado con éxito.")

                else:
                    QMessageBox.information(None, "Error", "Rellene todos los campos.")

                cancel()

            title = QLabel("Editar pedido")
            title.setFont(QFont("Verdana", 16))
            title.setAlignment(Qt.AlignCenter)

            submitButton = QPushButton("Aceptar")
            submitButton.clicked.connect(accept)

            cancelButton = QPushButton("Cancelar")
            cancelButton.clicked.connect(cancel)

            buttonsLayout = QHBoxLayout()
            buttonsLayout.addWidget(submitButton)
            buttonsLayout.addWidget(cancelButton)

            layout = QVBoxLayout(dialog)
            layout.addWidget(title)

            layout.addWidget(lblClient)
            layout.addWidget(client)

            layout.addWidget(lblOrder)
            layout.addWidget(order)

            layout.addWidget(lblPrice)
            layout.addWidget(orderPrice)

            layout.addLayout(buttonsLayout)

            dialog.setMinimumSize(225, 240)
            dialog.setMaximumSize(225, 240)
            dialog.setWindowModality(Qt.ApplicationModal)
            dialog.exec_()

        except:
            QMessageBox.information(None, "Error", "Seleccione el campo a editar.")



    def addProdEvent(self):
        dialog = QDialog()
        dialog.setWindowTitle("Añadir producto")
        dialog.setStyleSheet("QLabel{ text-decoration: underline; }")

        def cancel():
            dialog.close()

        def accept():
            prod = product.text()
            pri = int(price.text())
            
            if(prod != None and prod != "" and pri != None and pri != ""):
                params = [
                    prod,
                    pri
                ]

                try:

                    conn = sqlite3.connect("DB/db")
                    cursor = conn.cursor()

                    cursor.execute("INSERT INTO products (Product, Price) VALUES (?, ?)", params)

                    conn.commit()
                    conn.close()

                    QMessageBox.information(None, "Nuevo producto", "Producto insertado con éxito.")

                except:
                    QMessageBox.information(None, "Error", "Error al almacenar el producto")

            else:
                QMessageBox.information(None, "Error", "Rellene todos los campos.")

            cancel()

        title = QLabel("Añadir producto")
        title.setFont(QFont("Verdana", 16))
        title.setAlignment(Qt.AlignCenter)

        lblProduct = QLabel("Nuevo producto:")
        product = QLineEdit()
        
        lblPrice = QLabel("Precio:")
        price = QLineEdit()
        
        submitButton = QPushButton("Aceptar")
        submitButton.clicked.connect(accept)

        cancelButton = QPushButton("Cancelar")
        cancelButton.clicked.connect(cancel)

        buttonsLayout = QHBoxLayout()
        buttonsLayout.addWidget(submitButton)
        buttonsLayout.addWidget(cancelButton)

        layout = QVBoxLayout(dialog)
        layout.addWidget(title)

        layout.addWidget(lblProduct)
        layout.addWidget(product)

        layout.addWidget(lblPrice)
        layout.addWidget(price)

        layout.addLayout(buttonsLayout)

        dialog.setMinimumSize(225, 180)
        dialog.setMaximumSize(225, 180)
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.exec_()

    def removeProdEvent(self):
        dialog = QDialog()
        dialog.setWindowTitle("Eliminar producto")
        dialog.setStyleSheet("QLabel{ text-decoration: underline; }")

        def cancel():
            dialog.close()

        def accept():
            prod = product.currentText()

            if prod != "---Eligir producto---":
                conn = sqlite3.connect("DB/db")
                cursor = conn.cursor()

                cursor.execute("DELETE FROM PRODUCTS WHERE Product='" + prod + "'")

                conn.commit()
                conn.close()

                QMessageBox.information(None, "Producto eliminado", "Producto eliminado con éxito.")
            
            else:
                QMessageBox.information(None, "Error", "Elija un producto para eliminar.")

            cancel()

        title = QLabel("Eliminar producto")
        title.setFont(QFont("Verdana", 16))
        title.setAlignment(Qt.AlignCenter)

        lblProduct = QLabel("Producto a eliminar:")
        product = QComboBox()
        product.addItem("---Eligir producto---")

        conn = sqlite3.connect("DB/db")
        cursor = conn.cursor()
        products = cursor.execute("SELECT * FROM products")

        for p in products:
            product.addItem(p[0])

        conn.commit()
        conn.close()
        
        submitButton = QPushButton("Aceptar")
        submitButton.clicked.connect(accept)

        cancelButton = QPushButton("Cancelar")
        cancelButton.clicked.connect(cancel)

        buttonsLayout = QHBoxLayout()
        buttonsLayout.addWidget(submitButton)
        buttonsLayout.addWidget(cancelButton)

        layout = QVBoxLayout(dialog)
        layout.addWidget(title)

        layout.addWidget(lblProduct)
        layout.addWidget(product)

        layout.addLayout(buttonsLayout)

        dialog.setMinimumSize(225, 180)
        dialog.setMaximumSize(225, 180)
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.exec_()

    def resetEvent(self):
        # YES ----> 16384
        # NO ----> 65536
        op = QMessageBox.question(None, "¿Seguro?", "¿Seguro que quiere resetear los pedidos? (Esto va a borrar todo)")
        
        if op == 16384:
            conn = sqlite3.connect("DB/db")
            cursor = conn.cursor()

            cursor.execute("DELETE FROM orders")

            conn.commit()
            conn.close()

            self.startApp()

            QMessageBox.information(None, "Reseteado", "Registros reseteados...")


#----------FIN CLASE------------


def start():
    main = Main()

start()