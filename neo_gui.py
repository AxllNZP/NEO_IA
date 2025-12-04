# neo_gui.py - Interfaz Gráfica para NEO
"""
NEO GUI v1.0
Interfaz visual overlay para controlar NEO desde una aplicación independiente.
Compatible con Windows.
"""

import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QTextEdit, QFrame, QSystemTrayIcon,
    QMenu, QAction
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QThread, QSize
from PyQt5.QtGui import QIcon, QFont, QPalette, QColor, QPixmap, QPainter, QBrush, QPen
import time
import threading
from datetime import datetime

# ==========================================
# CONFIGURACIÓN GLOBAL
# ==========================================

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600
CAPTURE_INTERVAL = 3000  # 3 segundos entre capturas
VERSION = "1.0"

# ==========================================
# WORKER THREAD - NEO
# ==========================================

class NEOWorker(QThread):
    """Thread separado para ejecutar NEO sin bloquear la GUI"""
    
    # Señales para comunicación con GUI
    status_changed = pyqtSignal(str)  # Estado de NEO
    command_received = pyqtSignal(str)  # Comando recibido
    command_executed = pyqtSignal(str, bool)  # Comando ejecutado (comando, éxito)
    transcription_update = pyqtSignal(str)  # Transcripción en tiempo real
    
    def __init__(self):
        super().__init__()
        self.running = False
        self.neo_modules_loaded = False
        
    def load_neo_modules(self):
        """Carga los módulos de NEO"""
        try:
            # Importar módulos de NEO
            import neo_cerebro
            import neo_control
            import neo_voz
            
            self.neo_cerebro = neo_cerebro
            self.neo_control = neo_control
            self.neo_voz = neo_voz
            
            self.neo_modules_loaded = True
            self.status_changed.emit("Módulos cargados")
            return True
            
        except ImportError as e:
            self.status_changed.emit(f"Error: {str(e)}")
            return False
    
    def run(self):
        """Loop principal de NEO"""
        if not self.neo_modules_loaded:
            if not self.load_neo_modules():
                return
        
        self.running = True
        self.status_changed.emit("Escuchando...")
        
        while self.running:
            try:
                # Aquí iría la lógica de escucha y procesamiento
                # Por ahora es un placeholder
                self.status_changed.emit("Esperando comando...")
                time.sleep(1)
                
            except Exception as e:
                self.status_changed.emit(f"Error: {str(e)}")
                time.sleep(2)
    
    def stop(self):
        """Detiene el worker"""
        self.running = False
        self.status_changed.emit("Detenido")

# ==========================================
# SCREEN CAPTURE WORKER
# ==========================================

class ScreenCaptureWorker(QThread):
    """Thread para captura continua de pantalla"""
    
    screenshot_ready = pyqtSignal(QPixmap)
    
    def __init__(self):
        super().__init__()
        self.running = False
        self.capture_enabled = False
    
    def run(self):
        """Captura pantalla periódicamente"""
        self.running = True
        
        while self.running:
            if self.capture_enabled:
                try:
                    screen = QApplication.primaryScreen()
                    screenshot = screen.grabWindow(0)
                    
                    # Emitir señal con screenshot
                    self.screenshot_ready.emit(screenshot)
                    
                except Exception as e:
                    print(f"Error capturando pantalla: {e}")
            
            # Esperar intervalo
            time.sleep(CAPTURE_INTERVAL / 1000)
    
    def enable_capture(self):
        """Activa captura continua"""
        self.capture_enabled = True
    
    def disable_capture(self):
        """Desactiva captura continua"""
        self.capture_enabled = False
    
    def stop(self):
        """Detiene el worker"""
        self.running = False

# ==========================================
# VENTANA PRINCIPAL - NEO GUI
# ==========================================

class NEOWindow(QWidget):
    """Ventana principal overlay de NEO"""
    
    def __init__(self):
        super().__init__()
        
        # Workers
        self.neo_worker = NEOWorker()
        self.capture_worker = ScreenCaptureWorker()
        
        # Estado
        self.neo_active = False
        self.capture_active = False
        self.last_screenshot = None
        
        # Inicializar UI
        self.init_ui()
        
        # Conectar señales
        self.connect_signals()
        
        # Iniciar captura worker (pero no capturando aún)
        self.capture_worker.start()
    
    def init_ui(self):
        """Inicializa la interfaz"""
        
        # Configuración de ventana
        self.setWindowTitle(f"NEO v{VERSION}")
        self.setGeometry(100, 100, WINDOW_WIDTH, WINDOW_HEIGHT)
        
        # Flags de ventana para overlay
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint |  # Siempre encima
            Qt.FramelessWindowHint |   # Sin marco
            Qt.Tool                     # No aparece en taskbar
        )
        
        # Hacer ventana semi-transparente
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.95)
        
        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # === HEADER ===
        header = self.create_header()
        main_layout.addWidget(header)
        
        # === ESTADO ===
        self.status_frame = self.create_status_section()
        main_layout.addWidget(self.status_frame)
        
        # === TRANSCRIPCIÓN ===
        self.transcription_frame = self.create_transcription_section()
        main_layout.addWidget(self.transcription_frame)
        
        # === CONTROLES ===
        controls = self.create_controls()
        main_layout.addWidget(controls)
        
        # === FOOTER ===
        footer = self.create_footer()
        main_layout.addWidget(footer)
        
        # Establecer layout
        self.setLayout(main_layout)
        
        # Estilo global
        self.apply_styles()
    
    def create_header(self):
        """Crea el header con logo y título"""
        header_frame = QFrame()
        header_frame.setFrameShape(QFrame.StyledPanel)
        header_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(30, 30, 30, 200);
                border-radius: 10px;
                border: 2px solid #00ff88;
            }
        """)
        
        layout = QHBoxLayout()
        
        # Logo/Avatar de NEO (círculo)
        self.neo_avatar = QLabel()
        self.neo_avatar.setFixedSize(60, 60)
        self.neo_avatar.setAlignment(Qt.AlignCenter)
        self.neo_avatar.setStyleSheet("""
            QLabel {
                background-color: #00ff88;
                border-radius: 30px;
                font-size: 24px;
                font-weight: bold;
                color: #000;
            }
        """)
        self.neo_avatar.setText("NEO")
        
        # Título y versión
        title_layout = QVBoxLayout()
        title_label = QLabel("NEO Assistant")
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        title_label.setStyleSheet("color: #00ff88;")
        
        version_label = QLabel(f"Versión {VERSION}")
        version_label.setStyleSheet("color: #888; font-size: 10px;")
        
        title_layout.addWidget(title_label)
        title_layout.addWidget(version_label)
        
        # Botones de ventana
        window_buttons = QHBoxLayout()
        
        minimize_btn = QPushButton("−")
        minimize_btn.setFixedSize(30, 30)
        minimize_btn.clicked.connect(self.showMinimized)
        
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(30, 30)
        close_btn.clicked.connect(self.close)
        
        window_buttons.addWidget(minimize_btn)
        window_buttons.addWidget(close_btn)
        
        # Ensamblar header
        layout.addWidget(self.neo_avatar)
        layout.addLayout(title_layout)
        layout.addStretch()
        layout.addLayout(window_buttons)
        
        header_frame.setLayout(layout)
        return header_frame
    
    def create_status_section(self):
        """Crea sección de estado"""
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setStyleSheet("""
            QFrame {
                background-color: rgba(40, 40, 40, 200);
                border-radius: 10px;
                border: 1px solid #555;
            }
        """)
        
        layout = QVBoxLayout()
        
        # Título
        title = QLabel("Estado de NEO")
        title.setFont(QFont("Arial", 12, QFont.Bold))
        title.setStyleSheet("color: #00ff88;")
        
        # Indicador de estado
        self.status_label = QLabel("⚫ Inactivo")
        self.status_label.setFont(QFont("Arial", 14))
        self.status_label.setStyleSheet("color: #fff; padding: 10px;")
        
        layout.addWidget(title)
        layout.addWidget(self.status_label)
        
        frame.setLayout(layout)
        return frame
    
    def create_transcription_section(self):
        """Crea sección de transcripción"""
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setStyleSheet("""
            QFrame {
                background-color: rgba(40, 40, 40, 200);
                border-radius: 10px;
                border: 1px solid #555;
            }
        """)
        
        layout = QVBoxLayout()
        
        # Título
        title = QLabel("Última Transcripción")
        title.setFont(QFont("Arial", 12, QFont.Bold))
        title.setStyleSheet("color: #00ff88;")
        
        # Área de texto
        self.transcription_text = QTextEdit()
        self.transcription_text.setReadOnly(True)
        self.transcription_text.setMaximumHeight(150)
        self.transcription_text.setStyleSheet("""
            QTextEdit {
                background-color: rgba(20, 20, 20, 200);
                color: #fff;
                border: 1px solid #333;
                border-radius: 5px;
                padding: 10px;
                font-family: 'Courier New';
            }
        """)
        self.transcription_text.setPlaceholderText("Esperando comando de voz...")
        
        layout.addWidget(title)
        layout.addWidget(self.transcription_text)
        
        frame.setLayout(layout)
        return frame
    
    def create_controls(self):
        """Crea botones de control"""
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setStyleSheet("""
            QFrame {
                background-color: rgba(40, 40, 40, 200);
                border-radius: 10px;
                border: 1px solid #555;
            }
        """)
        
        layout = QVBoxLayout()
        
        # Botón principal de activación
        self.toggle_neo_btn = QPushButton("🎤 ACTIVAR NEO")
        self.toggle_neo_btn.setFixedHeight(50)
        self.toggle_neo_btn.setFont(QFont("Arial", 14, QFont.Bold))
        self.toggle_neo_btn.setStyleSheet("""
            QPushButton {
                background-color: #00ff88;
                color: #000;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #00cc70;
            }
            QPushButton:pressed {
                background-color: #009955;
            }
        """)
        self.toggle_neo_btn.clicked.connect(self.toggle_neo)
        
        # Botones secundarios
        secondary_layout = QHBoxLayout()
        
        # Botón de captura
        self.capture_btn = QPushButton("📸 Captura")
        self.capture_btn.clicked.connect(self.toggle_capture)
        
        # Botón de historial
        history_btn = QPushButton("📜 Historial")
        history_btn.clicked.connect(self.show_history)
        
        # Botón de configuración
        config_btn = QPushButton("⚙️ Config")
        config_btn.clicked.connect(self.show_config)
        
        secondary_layout.addWidget(self.capture_btn)
        secondary_layout.addWidget(history_btn)
        secondary_layout.addWidget(config_btn)
        
        # Aplicar estilo a botones secundarios
        for btn in [self.capture_btn, history_btn, config_btn]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(60, 60, 60, 200);
                    color: #fff;
                    border: 1px solid #666;
                    border-radius: 5px;
                    padding: 10px;
                }
                QPushButton:hover {
                    background-color: rgba(80, 80, 80, 200);
                }
            """)
        
        layout.addWidget(self.toggle_neo_btn)
        layout.addLayout(secondary_layout)
        
        frame.setLayout(layout)
        return frame
    
    def create_footer(self):
        """Crea footer con información"""
        footer_frame = QFrame()
        footer_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(30, 30, 30, 200);
                border-radius: 5px;
            }
        """)
        
        layout = QHBoxLayout()
        
        # Información
        info_label = QLabel("💡 Di 'NEO' + tu comando")
        info_label.setStyleSheet("color: #888; font-size: 10px;")
        
        # Timestamp
        self.time_label = QLabel()
        self.time_label.setStyleSheet("color: #888; font-size: 10px;")
        self.update_time()
        
        layout.addWidget(info_label)
        layout.addStretch()
        layout.addWidget(self.time_label)
        
        footer_frame.setLayout(layout)
        
        # Timer para actualizar hora
        timer = QTimer(self)
        timer.timeout.connect(self.update_time)
        timer.start(1000)
        
        return footer_frame
    
    def apply_styles(self):
        """Aplica estilos globales"""
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(20, 20, 20, 230);
                color: #ffffff;
                font-family: Arial;
            }
        """)
    
    def connect_signals(self):
        """Conecta señales de los workers"""
        # NEO Worker
        self.neo_worker.status_changed.connect(self.update_status)
        self.neo_worker.command_received.connect(self.update_transcription)
        
        # Capture Worker
        self.capture_worker.screenshot_ready.connect(self.handle_screenshot)
    
    # ==========================================
    # MÉTODOS DE CONTROL
    # ==========================================
    
    def toggle_neo(self):
        """Activa/desactiva NEO"""
        if not self.neo_active:
            # Activar
            self.neo_active = True
            self.toggle_neo_btn.setText("⏸️ DETENER NEO")
            self.toggle_neo_btn.setStyleSheet("""
                QPushButton {
                    background-color: #ff5555;
                    color: #fff;
                    border: none;
                    border-radius: 10px;
                }
                QPushButton:hover {
                    background-color: #cc4444;
                }
            """)
            
            # Iniciar worker de NEO
            if not self.neo_worker.isRunning():
                self.neo_worker.start()
            
        else:
            # Desactivar
            self.neo_active = False
            self.toggle_neo_btn.setText("🎤 ACTIVAR NEO")
            self.toggle_neo_btn.setStyleSheet("""
                QPushButton {
                    background-color: #00ff88;
                    color: #000;
                    border: none;
                    border-radius: 10px;
                }
                QPushButton:hover {
                    background-color: #00cc70;
                }
            """)
            
            # Detener worker
            self.neo_worker.stop()
    
    def toggle_capture(self):
        """Activa/desactiva captura continua"""
        if not self.capture_active:
            self.capture_active = True
            self.capture_btn.setText("📸 Detener")
            self.capture_worker.enable_capture()
        else:
            self.capture_active = False
            self.capture_btn.setText("📸 Captura")
            self.capture_worker.disable_capture()
    
    def show_history(self):
        """Muestra historial de comandos"""
        # TODO: Implementar ventana de historial
        self.transcription_text.append("\n[INFO] Historial próximamente...")
    
    def show_config(self):
        """Muestra configuración"""
        # TODO: Implementar ventana de configuración
        self.transcription_text.append("\n[INFO] Configuración próximamente...")
    
    # ==========================================
    # MÉTODOS DE ACTUALIZACIÓN
    # ==========================================
    
    def update_status(self, status):
        """Actualiza el estado visual"""
        if "Escuchando" in status:
            self.status_label.setText("🟢 Escuchando...")
            self.neo_avatar.setStyleSheet("""
                QLabel {
                    background-color: #00ff88;
                    border-radius: 30px;
                    font-size: 24px;
                    font-weight: bold;
                    color: #000;
                }
            """)
        elif "Procesando" in status:
            self.status_label.setText("🟡 Procesando...")
            self.neo_avatar.setStyleSheet("""
                QLabel {
                    background-color: #ffff00;
                    border-radius: 30px;
                    font-size: 24px;
                    font-weight: bold;
                    color: #000;
                }
            """)
        elif "Error" in status:
            self.status_label.setText("🔴 Error")
            self.neo_avatar.setStyleSheet("""
                QLabel {
                    background-color: #ff5555;
                    border-radius: 30px;
                    font-size: 24px;
                    font-weight: bold;
                    color: #fff;
                }
            """)
        else:
            self.status_label.setText(f"⚫ {status}")
    
    def update_transcription(self, text):
        """Actualiza la transcripción"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.transcription_text.append(f"[{timestamp}] {text}")
    
    def update_time(self):
        """Actualiza el timestamp"""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.setText(current_time)
    
    def handle_screenshot(self, pixmap):
        """Maneja screenshot capturado"""
        self.last_screenshot = pixmap
        # Aquí podrías procesar la imagen con LLaVA si es necesario
    
    # ==========================================
    # EVENTOS DE VENTANA
    # ==========================================
    
    def mousePressEvent(self, event):
        """Permite mover la ventana"""
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        """Mueve la ventana"""
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
            event.accept()
    
    def closeEvent(self, event):
        """Al cerrar, detener workers"""
        self.neo_worker.stop()
        self.capture_worker.stop()
        event.accept()

# ==========================================
# PROGRAMA PRINCIPAL
# ==========================================

def main():
    """Función principal"""
    app = QApplication(sys.argv)
    
    # Configurar aplicación
    app.setApplicationName("NEO Assistant")
    app.setOrganizationName("NEO")
    
    # Crear y mostrar ventana
    window = NEOWindow()
    window.show()
    
    # Ejecutar
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()