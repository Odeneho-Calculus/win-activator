#!/usr/bin/env python3
"""
Windows Activator GUI Application
A modern PyQt5 interface for Windows activation with dark theme
"""

import sys
import os
import subprocess
import platform
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
                             QWidget, QPushButton, QLabel, QComboBox, QTextEdit,
                             QProgressBar, QMessageBox, QFrame, QGroupBox, QGridLayout,
                             QSplashScreen, QSystemTrayIcon, QMenu, QAction, QSizePolicy,
                             QScrollArea, QSpacerItem, QTabWidget, QListWidget, QListWidgetItem,
                             QSplitter, QTextBrowser)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer, QPropertyAnimation, QRect
from PyQt5.QtGui import QFont, QPixmap, QPalette, QColor, QIcon
import json
import time
import ctypes

class ActivationWorker(QThread):
    """Worker thread for Windows activation process"""
    progress_updated = pyqtSignal(int)
    status_updated = pyqtSignal(str)
    activation_completed = pyqtSignal(bool, str)

    def __init__(self, windows_version):
        super().__init__()
        self.windows_version = windows_version
        self.is_running = True

        # Windows version to product key mapping
        self.product_keys = {
            "Windows 11 Home": [
                "TX9XD-98N7V-6WMQ6-BX7FG-H8Q99",
                "3KHY7-WNT83-DGQKR-F7HPR-844BM",
                "7HNRX-D7KGG-3K4RQ-4WPJ4-YTDFH",
                "PVMJN-6DFY6-9CCP6-7BKTT-D3WVR"
            ],
            "Windows 11 Pro": [
                "W269N-WFGWX-YVC9B-4J6C9-T83GX",
                "MH37W-N47XK-V7XM9-C7227-GCQG9",
                "NRG8B-VKK3Q-CXVCJ-9G2XF-6Q84J",
                "9FNHH-K3HBT-3W4TD-6383H-6XYWF",
                "6TP4R-GNPTD-KYYHQ-7B7DP-J447Y",
                "YVWGF-BXNMC-HTQYQ-CPQ99-66QFC"
            ],
            "Windows 11 Enterprise": [
                "NPPR9-FWDCX-D2C8J-H872K-2YT43",
                "DPH2V-TTNVB-4X9Q3-TJR4H-KHJW4",
                "YYVX9-NTFWV-6MDM3-9PT4T-4M68B",
                "44RPN-FTY23-9VTTB-MP9BX-T84FV",
                "WNMTR-4C88C-JK8YV-HQ7T2-76DF9",
                "2F77B-TNFGY-69QQF-B8YKP-D69TJ",
                "DCPHK-NFMTC-H88MJ-PFHPY-QJ4BJ",
                "QFFDN-GRT3P-VKWWX-X7T3R-8B639",
                "M7XTQ-FN8P6-TTKYV-9D4CC-J462D",
                "92NFX-8DJQP-P6BBQ-THF9C-7CG2H"
            ],
            "Windows 11 Education": [
                "NW6C2-QMPVW-D7KKK-3GKT6-VCFB2",
                "2WH4N-8QGBV-H22JP-CT43Q-MDWWJ"
            ],
            "Windows 10 Home": [
                "TX9XD-98N7V-6WMQ6-BX7FG-H8Q99",
                "3KHY7-WNT83-DGQKR-F7HPR-844BM",
                "7HNRX-D7KGG-3K4RQ-4WPJ4-YTDFH",
                "PVMJN-6DFY6-9CCP6-7BKTT-D3WVR"
            ],
            "Windows 10 Pro": [
                "W269N-WFGWX-YVC9B-4J6C9-T83GX",
                "MH37W-N47XK-V7XM9-C7227-GCQG9",
                "NRG8B-VKK3Q-CXVCJ-9G2XF-6Q84J",
                "9FNHH-K3HBT-3W4TD-6383H-6XYWF"
            ],
            "Windows 10 Enterprise": [
                "NPPR9-FWDCX-D2C8J-H872K-2YT43",
                "DPH2V-TTNVB-4X9Q3-TJR4H-KHJW4",
                "YYVX9-NTFWV-6MDM3-9PT4T-4M68B",
                "44RPN-FTY23-9VTTB-MP9BX-T84FV"
            ],
            "Windows 10 Education": [
                "NW6C2-QMPVW-D7KKK-3GKT6-VCFB2",
                "2WH4N-8QGBV-H22JP-CT43Q-MDWWJ"
            ]
        }

        self.kms_servers = [
            "kms7.MSGuides.com",
            "kms8.MSGuides.com",
            "kms9.MSGuides.com"
        ]

    def run(self):
        """Main activation process"""
        try:
            self.status_updated.emit("Starting activation process...")
            self.progress_updated.emit(10)

            # Check if running as administrator
            if not self.is_admin():
                self.status_updated.emit("⚠️ WARNING: Not running as Administrator!")
                self.status_updated.emit("For best results, restart this application as Administrator")
                time.sleep(2)  # Give user time to read the warning

            # Clear existing keys
            self.status_updated.emit("Clearing existing product keys...")
            self.run_command("cscript //nologo C:\\Windows\\System32\\slmgr.vbs /ckms")
            self.run_command("cscript //nologo C:\\Windows\\System32\\slmgr.vbs /upk")
            self.run_command("cscript //nologo C:\\Windows\\System32\\slmgr.vbs /cpky")
            self.progress_updated.emit(30)

            # Install product key
            self.status_updated.emit(f"Installing product key for {self.windows_version}...")
            success = self.install_product_key()
            if not success:
                self.activation_completed.emit(False, "Failed to install product key")
                return

            self.progress_updated.emit(60)

            # Set KMS server and activate
            self.status_updated.emit("Connecting to KMS server...")
            success = self.activate_windows()

            if success:
                self.progress_updated.emit(100)
                self.status_updated.emit("Windows activated successfully!")
                self.activation_completed.emit(True, "Windows has been activated successfully!")
            else:
                self.activation_completed.emit(False, "Activation failed. Please try again.")

        except Exception as e:
            self.activation_completed.emit(False, f"Error during activation: {str(e)}")

    def install_product_key(self):
        """Install product key for selected Windows version"""
        if self.windows_version not in self.product_keys:
            self.status_updated.emit("❌ Windows version not supported")
            return False

        keys = self.product_keys[self.windows_version]
        for i, key in enumerate(keys):
            if not self.is_running:
                return False
            try:
                self.status_updated.emit(f"🔑 Trying product key {i+1}/{len(keys)} for {self.windows_version}...")
                result = self.run_command(f"cscript //nologo C:\\Windows\\System32\\slmgr.vbs /ipk {key}")

                if result:
                    # Check for success indicators
                    if "successfully" in result.lower() or "installed" in result.lower():
                        self.status_updated.emit(f"✅ Product key installed successfully")
                        return True
                    elif "access denied" in result.lower():
                        self.status_updated.emit("❌ Access denied - Please run as Administrator")
                        self.status_updated.emit("💡 Tip: Right-click the application and select 'Run as administrator'")
                        return False
                    elif "invalid" in result.lower():
                        self.status_updated.emit(f"⚠️ Key {i+1} invalid, trying next...")
                        continue
                    else:
                        self.status_updated.emit(f"⚠️ Key {i+1} failed: {result[:100]}...")
                        continue
                else:
                    self.status_updated.emit(f"⚠️ No response for key {i+1}")
                    continue

            except Exception as e:
                self.status_updated.emit(f"⚠️ Error with key {i+1}: {str(e)}")
                continue

        self.status_updated.emit("❌ All product keys failed")
        return False

    def activate_windows(self):
        """Activate Windows using KMS servers"""
        for i, server in enumerate(self.kms_servers):
            if not self.is_running:
                return False

            try:
                self.status_updated.emit(f"Trying KMS server {i+1}/{len(self.kms_servers)}...")

                # Set KMS server
                self.run_command(f"cscript //nologo C:\\Windows\\System32\\slmgr.vbs /skms {server}:1688")

                # Attempt activation
                result = self.run_command("cscript //nologo C:\\Windows\\System32\\slmgr.vbs /ato")

                if result and "successfully" in result.lower():
                    return True

            except Exception as e:
                self.status_updated.emit(f"Server {i+1} failed: {str(e)}")
                continue

        return False

    def run_command(self, command):
        """Execute Windows command and return output"""
        try:
            # For Windows commands, we might need to run with elevated privileges
            result = subprocess.run(command, shell=True, capture_output=True,
                                  text=True, timeout=30, creationflags=subprocess.CREATE_NO_WINDOW)

            output = result.stdout + result.stderr

            # Log the command and its return code for debugging
            if result.returncode != 0:
                self.status_updated.emit(f"Command returned code {result.returncode}")

            return output

        except subprocess.TimeoutExpired:
            return "Command timed out - operation took too long"
        except Exception as e:
            return f"Command execution failed: {str(e)}"

    def is_admin(self):
        """Check if the application is running with administrator privileges"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def stop(self):
        """Stop the activation process"""
        self.is_running = False


class ModernCard(QFrame):
    """Modern card-style container with dark theme"""
    def __init__(self, title="", content_widget=None):
        super().__init__()
        self.setObjectName("ModernCard")
        self.setup_ui(title, content_widget)

    def setup_ui(self, title, content_widget):
        """Setup card UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        if title:
            title_label = QLabel(title)
            title_label.setObjectName("CardTitle")
            layout.addWidget(title_label)

        if content_widget:
            layout.addWidget(content_widget)


class ModernButton(QPushButton):
    """Modern styled button with dark theme"""
    def __init__(self, text, button_type="secondary"):
        super().__init__(text)
        self.button_type = button_type
        self.setObjectName(f"ModernButton_{button_type}")
        self.setMinimumHeight(45)
        self.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
        self.setCursor(Qt.CursorShape.PointingHandCursor)


class WindowsActivatorGUI(QMainWindow):
    """Main application window with modern dark theme"""

    def __init__(self):
        super().__init__()
        self.worker = None
        self.init_ui()
        self.apply_dark_theme()
        self.setup_system_info()

    def init_ui(self):
        """Initialize the user interface with scrolling and rich content"""
        self.setWindowTitle("Windows Activator Pro - Advanced Edition")
        self.setGeometry(100, 100, 1200, 900)
        self.setMinimumSize(1000, 700)

        # Create main scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setObjectName("MainScrollArea")
        self.setCentralWidget(scroll_area)

        # Create scrollable content widget
        content_widget = QWidget()
        scroll_area.setWidget(content_widget)

        # Main layout with proper spacing
        main_layout = QVBoxLayout(content_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(25, 25, 25, 25)

        # Create all sections with enhanced content
        self.create_header(main_layout)
        self.create_admin_status_panel(main_layout)
        self.create_quick_info_panel(main_layout)
        self.create_tabs_section(main_layout)
        self.create_main_control_panel(main_layout)
        self.create_progress_and_status_panel(main_layout)
        self.create_advanced_features_panel(main_layout)
        self.create_log_and_output_panel(main_layout)
        self.create_footer_with_links(main_layout)

        # Add stretch to push everything up
        main_layout.addStretch()

    def create_header(self, layout):
        """Create modern header section"""
        header_card = ModernCard()
        header_card.setObjectName("HeaderCard")

        header_layout = QVBoxLayout()
        header_layout.setSpacing(10)
        header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Main title
        title = QLabel("Windows Activator Pro")
        title.setObjectName("HeaderTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Subtitle
        subtitle = QLabel("Professional Windows Activation Tool")
        subtitle.setObjectName("HeaderSubtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        header_card.layout().addLayout(header_layout)

        layout.addWidget(header_card)

    def create_admin_status_panel(self, layout):
        """Create admin status warning panel"""
        admin_content = QWidget()
        admin_layout = QHBoxLayout(admin_content)
        admin_layout.setSpacing(15)

        # Check admin status
        is_admin = self.is_admin()

        if is_admin:
            status_icon = QLabel("✅")
            status_text = QLabel("Running as Administrator")
            status_text.setObjectName("AdminStatusGood")
            restart_btn = None
        else:
            status_icon = QLabel("⚠️")
            status_text = QLabel("NOT running as Administrator - Some features may not work")
            status_text.setObjectName("AdminStatusWarning")
            restart_btn = ModernButton("🔄 Restart as Admin", "primary")
            restart_btn.clicked.connect(self.restart_as_admin)

        status_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        status_text.setWordWrap(True)

        admin_layout.addWidget(status_icon)
        admin_layout.addWidget(status_text, 1)

        if restart_btn:
            admin_layout.addWidget(restart_btn)

        admin_card = ModernCard("🛡️ Administrator Status", admin_content)
        if not is_admin:
            admin_card.setObjectName("WarningCard")

        layout.addWidget(admin_card)

    def is_admin(self):
        """Check if running as administrator"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def restart_as_admin(self):
        """Restart application as administrator"""
        try:
            import sys
            if sys.platform == "win32":
                # Get the full path to the current script
                script_path = os.path.abspath(sys.argv[0])
                self.log_message("🔄 Restarting with administrator privileges...")

                result = ctypes.windll.shell32.ShellExecuteW(
                    None, "runas", sys.executable, f'"{script_path}"', None, 1
                )

                if result > 32:  # Success
                    self.log_message("✅ Successfully initiated admin restart")
                    QApplication.quit()
                else:
                    self.log_message(f"❌ Failed to restart as admin (error code: {result})")
                    QMessageBox.warning(self, "Error", "Failed to restart as administrator. Please try manually.")
            else:
                QMessageBox.warning(self, "Error", "Admin restart is only supported on Windows.")
        except Exception as e:
            self.log_message(f"❌ Exception during admin restart: {str(e)}")
            QMessageBox.warning(self, "Error", f"Failed to restart as administrator: {str(e)}")

    def create_quick_info_panel(self, layout):
        """Create quick information panel with system stats"""
        # Create horizontal layout for multiple info cards
        info_row = QHBoxLayout()
        info_row.setSpacing(15)

        # System Information Card
        sys_content = QWidget()
        sys_layout = QVBoxLayout(sys_content)

        self.os_label = QLabel("OS: Detecting...")
        self.version_label = QLabel("Version: Detecting...")
        self.architecture_label = QLabel("Architecture: Detecting...")

        labels = [self.os_label, self.version_label, self.architecture_label]
        for label in labels:
            label.setObjectName("InfoLabel")
            sys_layout.addWidget(label)

        sys_card = ModernCard("🖥️ System Information", sys_content)

        # Activation Status Card
        status_content = QWidget()
        status_layout = QVBoxLayout(status_content)

        self.activation_status_label = QLabel("Checking activation status...")
        self.activation_status_label.setObjectName("ActivationStatus")
        self.activation_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        status_layout.addWidget(self.activation_status_label)

        status_card = ModernCard("🔐 Activation Status", status_content)
        status_card.setObjectName("StatusCard")

        # Performance Info Card
        perf_content = QWidget()
        perf_layout = QVBoxLayout(perf_content)

        self.uptime_label = QLabel("Uptime: Calculating...")
        self.cpu_label = QLabel("CPU: Detecting...")
        self.memory_label = QLabel("Memory: Detecting...")

        perf_labels = [self.uptime_label, self.cpu_label, self.memory_label]
        for label in perf_labels:
            label.setObjectName("InfoLabel")
            perf_layout.addWidget(label)

        perf_card = ModernCard("⚡ System Performance", perf_content)

        # Add cards to row
        info_row.addWidget(sys_card)
        info_row.addWidget(status_card)
        info_row.addWidget(perf_card)

        layout.addLayout(info_row)

    def create_tabs_section(self, layout):
        """Create tabbed interface for different features"""
        tab_widget = QTabWidget()
        tab_widget.setObjectName("ModernTabWidget")
        tab_widget.setMinimumHeight(400)  # Ensure minimum height for proper display

        # Main Activation Tab
        main_tab = QWidget()
        main_layout = QVBoxLayout(main_tab)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(25, 25, 25, 25)

        # Windows Version Selection
        version_content = QWidget()
        version_layout = QVBoxLayout(version_content)
        version_layout.setSpacing(12)

        instruction_label = QLabel("Select your Windows version:")
        instruction_label.setObjectName("InstructionLabel")
        instruction_label.setWordWrap(True)
        version_layout.addWidget(instruction_label)

        self.version_combo = QComboBox()
        self.version_combo.setObjectName("VersionCombo")
        self.version_combo.setMinimumHeight(40)
        self.version_combo.addItems([
            "Windows 11 Home",
            "Windows 11 Pro",
            "Windows 11 Enterprise",
            "Windows 11 Education",
            "Windows 10 Home",
            "Windows 10 Pro",
            "Windows 10 Enterprise",
            "Windows 10 Education"
        ])
        version_layout.addWidget(self.version_combo)

        auto_detect_btn = ModernButton("🔍 Auto-Detect Current Version", "secondary")
        auto_detect_btn.setMinimumHeight(45)
        auto_detect_btn.clicked.connect(self.auto_detect_version)
        version_layout.addWidget(auto_detect_btn)

        version_card = ModernCard("Windows Version Selection", version_content)
        main_layout.addWidget(version_card)

        # Product Keys Information
        keys_info = self.create_keys_info_panel()
        main_layout.addWidget(keys_info)

        # Add stretch to fill remaining space
        main_layout.addStretch()

        tab_widget.addTab(main_tab, "🚀 Activation")

        # Tools Tab
        tools_tab = QWidget()
        tools_layout = QVBoxLayout(tools_tab)
        tools_layout.setSpacing(20)
        tools_layout.setContentsMargins(25, 25, 25, 25)

        # Add various tools
        self.create_tools_content(tools_layout)

        # Add stretch to fill remaining space
        tools_layout.addStretch()

        tab_widget.addTab(tools_tab, "🛠️ System Tools")

        # Information Tab
        info_tab = QWidget()
        info_layout = QVBoxLayout(info_tab)
        info_layout.setSpacing(20)
        info_layout.setContentsMargins(25, 25, 25, 25)

        self.create_info_content(info_layout)

        # Add stretch to fill remaining space
        info_layout.addStretch()

        tab_widget.addTab(info_tab, "📖 Documentation")

        layout.addWidget(tab_widget)

    def create_keys_info_panel(self):
        """Create panel showing available product keys"""
        content = QWidget()
        layout = QVBoxLayout(content)

        # Keys list
        self.keys_list = QListWidget()
        self.keys_list.setObjectName("KeysList")
        self.keys_list.setMaximumHeight(150)

        # Add some sample keys for display
        sample_keys = [
            "Generic Key 1: TX9XD-98N7V-6WMQ6-BX7FG-H8Q99",
            "Generic Key 2: W269N-WFGWX-YVC9B-4J6C9-T83GX",
            "Generic Key 3: NPPR9-FWDCX-D2C8J-H872K-2YT43"
        ]

        for key in sample_keys:
            item = QListWidgetItem(key)
            self.keys_list.addItem(item)

        layout.addWidget(QLabel("Available Generic Product Keys:"))
        layout.addWidget(self.keys_list)

        return ModernCard("🔑 Product Keys", content)

    def create_tools_content(self, layout):
        """Create tools tab content"""
        # System Tools
        tools_grid = QGridLayout()
        tools_grid.setSpacing(12)
        tools_grid.setContentsMargins(10, 10, 10, 10)

        # Create tool buttons
        tools = [
            ("🔧 System File Checker", self.run_sfc_scan),
            ("🧹 Disk Cleanup", self.run_disk_cleanup),
            ("📊 System Information", self.show_system_info),
            ("🔄 Windows Update", self.check_windows_updates),
            ("🖥️ Display Settings", self.open_display_settings),
            ("🔊 Sound Settings", self.open_sound_settings),
            ("🌐 Network Settings", self.open_network_settings),
            ("🛡️ Windows Defender", self.open_defender)
        ]

        for i, (text, func) in enumerate(tools):
            btn = ModernButton(text, "secondary")
            btn.setMinimumHeight(50)
            btn.setMinimumWidth(200)
            btn.clicked.connect(func)
            tools_grid.addWidget(btn, i // 2, i % 2)

        tools_widget = QWidget()
        tools_widget.setLayout(tools_grid)

        tools_card = ModernCard("🔧 System Management Tools", tools_widget)
        layout.addWidget(tools_card)

    def create_info_content(self, layout):
        """Create information tab content"""
        info_browser = QTextBrowser()
        info_browser.setObjectName("InfoBrowser")

        info_text = """
        <h2 style="color: #89b4fa;">🎯 Windows Activator Pro - Information</h2>

        <h3 style="color: #a6e3a1;">What is Windows Activation?</h3>
        <p>Windows activation is a process that verifies your copy of Windows is genuine and hasn't been used on more devices than the Microsoft Software License Terms allow.</p>

        <h3 style="color: #a6e3a1;">How This Tool Works</h3>
        <ul>
        <li><b>Generic Keys:</b> Uses Microsoft's Generic Volume License Keys (GVLK)</li>
        <li><b>KMS Activation:</b> Connects to Key Management Service servers</li>
        <li><b>Safe Process:</b> Only uses official Microsoft activation methods</li>
        </ul>

        <h3 style="color: #a6e3a1;">Features</h3>
        <ul>
        <li>✅ Auto-detection of Windows version</li>
        <li>✅ Multiple KMS server fallbacks</li>
        <li>✅ Real-time progress tracking</li>
        <li>✅ Comprehensive logging</li>
        <li>✅ System information display</li>
        <li>✅ Built-in system tools</li>
        </ul>

        <h3 style="color: #fab387;">⚠️ Important Notes</h3>
        <ul>
        <li>This tool is for educational purposes only</li>
        <li>Always ensure you have proper licensing</li>
        <li>Run as administrator for full functionality</li>
        <li>Some antivirus software may flag activation tools</li>
        </ul>

        <h3 style="color: #89b4fa;">🔧 Troubleshooting</h3>
        <ul>
        <li><b>Activation Failed:</b> Try running as administrator</li>
        <li><b>Network Error:</b> Check internet connection</li>
        <li><b>Key Not Accepted:</b> Verify Windows version selection</li>
        </ul>
        """

        info_browser.setHtml(info_text)

        info_card = ModernCard("📋 Documentation", info_browser)
        layout.addWidget(info_card)

    def create_main_control_panel(self, layout):
        """Create main control buttons panel"""
        control_content = QWidget()
        control_layout = QHBoxLayout(control_content)
        control_layout.setSpacing(20)

        # Main activation button (larger and more prominent)
        self.activate_btn = ModernButton("🚀 ACTIVATE WINDOWS", "primary")
        self.activate_btn.setMinimumHeight(60)
        self.activate_btn.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        self.activate_btn.clicked.connect(self.start_activation)

        # Secondary buttons
        self.check_status_btn = ModernButton("📊 Check Status", "secondary")
        self.check_status_btn.clicked.connect(self.check_activation_status)

        self.test_btn = ModernButton("🧪 Test Commands", "secondary")
        self.test_btn.clicked.connect(self.test_activation_commands)

        self.stop_btn = ModernButton("⏹️ Stop Process", "danger")
        self.stop_btn.clicked.connect(self.stop_activation)
        self.stop_btn.setEnabled(False)

        # Quick actions
        quick_check_btn = ModernButton("⚡ Quick Check", "secondary")
        quick_check_btn.clicked.connect(self.quick_activation_check)

        control_layout.addWidget(self.activate_btn, 2)  # Takes more space
        control_layout.addWidget(self.check_status_btn, 1)
        control_layout.addWidget(self.test_btn, 1)
        control_layout.addWidget(quick_check_btn, 1)
        control_layout.addWidget(self.stop_btn, 1)

        control_card = ModernCard("🎮 Main Controls", control_content)
        layout.addWidget(control_card)

    def create_progress_and_status_panel(self, layout):
        """Create enhanced progress and status panel"""
        progress_content = QWidget()
        progress_layout = QVBoxLayout(progress_content)
        progress_layout.setSpacing(15)

        # Current status with icon
        status_row = QHBoxLayout()
        self.status_icon = QLabel("🟢")
        self.status_icon.setFont(QFont("Segoe UI", 16))
        self.status_label = QLabel("Ready to activate")
        self.status_label.setObjectName("StatusLabel")

        status_row.addWidget(self.status_icon)
        status_row.addWidget(self.status_label)
        status_row.addStretch()

        progress_layout.addLayout(status_row)

        # Enhanced progress bar with percentage
        progress_row = QHBoxLayout()
        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("ModernProgressBar")
        self.progress_bar.setMinimumHeight(35)

        self.progress_percentage = QLabel("0%")
        self.progress_percentage.setObjectName("ProgressPercentage")
        self.progress_percentage.setMinimumWidth(40)

        progress_row.addWidget(self.progress_bar)
        progress_row.addWidget(self.progress_percentage)

        progress_layout.addLayout(progress_row)

        # Current operation details
        self.operation_detail = QLabel("No operation in progress")
        self.operation_detail.setObjectName("OperationDetail")
        progress_layout.addWidget(self.operation_detail)

        progress_card = ModernCard("📈 Progress & Status", progress_content)
        layout.addWidget(progress_card)

    def create_advanced_features_panel(self, layout):
        """Create advanced features panel"""
        features_content = QWidget()
        features_layout = QHBoxLayout(features_content)
        features_layout.setSpacing(15)

        # Server selection
        server_widget = QWidget()
        server_layout = QVBoxLayout(server_widget)

        server_layout.addWidget(QLabel("KMS Server Selection:"))
        self.server_combo = QComboBox()
        self.server_combo.setObjectName("ServerCombo")
        self.server_combo.addItems([
            "Auto-Select Best Server",
            "kms7.MSGuides.com",
            "kms8.MSGuides.com",
            "kms9.MSGuides.com"
        ])
        server_layout.addWidget(self.server_combo)

        server_card = ModernCard("🌐 Server Settings", server_widget)

        # Options panel
        options_widget = QWidget()
        options_layout = QVBoxLayout(options_widget)

        self.auto_retry_check = QPushButton("🔄 Auto-Retry on Failure")
        self.auto_retry_check.setCheckable(True)
        self.auto_retry_check.setChecked(True)
        self.auto_retry_check.setObjectName("ModernButton_secondary")

        self.verbose_logging = QPushButton("📝 Verbose Logging")
        self.verbose_logging.setCheckable(True)
        self.verbose_logging.setObjectName("ModernButton_secondary")

        options_layout.addWidget(self.auto_retry_check)
        options_layout.addWidget(self.verbose_logging)

        options_card = ModernCard("⚙️ Options", options_widget)

        features_layout.addWidget(server_card)
        features_layout.addWidget(options_card)

        layout.addWidget(features_content)

    def create_log_and_output_panel(self, layout):
        """Create enhanced logging panel"""
        log_content = QWidget()
        log_layout = QVBoxLayout(log_content)
        log_layout.setSpacing(15)

        # Log controls
        log_controls = QHBoxLayout()

        clear_log_btn = ModernButton("🧹 Clear Log", "secondary")
        clear_log_btn.clicked.connect(self.clear_log)

        save_log_btn = ModernButton("💾 Save Log", "secondary")
        save_log_btn.clicked.connect(self.save_log)

        copy_log_btn = ModernButton("📋 Copy Log", "secondary")
        copy_log_btn.clicked.connect(self.copy_log)

        export_log_btn = ModernButton("📤 Export Log", "secondary")
        export_log_btn.clicked.connect(self.export_log)

        log_controls.addWidget(clear_log_btn)
        log_controls.addWidget(save_log_btn)
        log_controls.addWidget(copy_log_btn)
        log_controls.addWidget(export_log_btn)
        log_controls.addStretch()

        log_layout.addLayout(log_controls)

        # Enhanced log text area
        self.log_text = QTextEdit()
        self.log_text.setObjectName("LogTerminal")
        self.log_text.setMinimumHeight(250)
        self.log_text.setReadOnly(True)
        log_layout.addWidget(self.log_text)

        # Log statistics
        log_stats = QHBoxLayout()
        self.log_lines_count = QLabel("Lines: 0")
        self.log_lines_count.setObjectName("LogStats")
        self.last_update_time = QLabel("Last update: Never")
        self.last_update_time.setObjectName("LogStats")

        log_stats.addWidget(self.log_lines_count)
        log_stats.addStretch()
        log_stats.addWidget(self.last_update_time)

        log_layout.addLayout(log_stats)

        log_card = ModernCard("📋 Process Log & Output", log_content)
        layout.addWidget(log_card)

    def create_footer_with_links(self, layout):
        """Create enhanced footer with links and version info"""
        footer_content = QWidget()
        footer_layout = QVBoxLayout(footer_content)
        footer_layout.setSpacing(10)

        # Version and build info
        version_info = QHBoxLayout()

        version_label = QLabel("Windows Activator Pro v2.0.0")
        version_label.setObjectName("VersionLabel")

        build_label = QLabel("Build: 2024.12.17")
        build_label.setObjectName("BuildLabel")

        version_info.addWidget(version_label)
        version_info.addStretch()
        version_info.addWidget(build_label)

        footer_layout.addLayout(version_info)

        # Links and info
        links_layout = QHBoxLayout()

        disclaimer_btn = ModernButton("⚖️ Legal Disclaimer", "secondary")
        disclaimer_btn.clicked.connect(self.show_disclaimer)

        help_btn = ModernButton("❓ Help & Support", "secondary")
        help_btn.clicked.connect(self.show_help)

        about_btn = ModernButton("ℹ️ About", "secondary")
        about_btn.clicked.connect(self.show_about)

        links_layout.addWidget(disclaimer_btn)
        links_layout.addWidget(help_btn)
        links_layout.addWidget(about_btn)
        links_layout.addStretch()

        footer_layout.addLayout(links_layout)

        # Copyright
        copyright_label = QLabel("© 2024 Windows Activator Pro - Educational Purpose Only")
        copyright_label.setObjectName("FooterLabel")
        copyright_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer_layout.addWidget(copyright_label)

        layout.addWidget(footer_content)

    def create_system_info_card(self, layout):
        """Create system information card"""
        content_widget = QWidget()
        content_layout = QGridLayout(content_widget)
        content_layout.setSpacing(15)

        # System info labels
        self.os_label = QLabel("OS: Detecting...")
        self.version_label = QLabel("Version: Detecting...")
        self.architecture_label = QLabel("Architecture: Detecting...")

        labels = [self.os_label, self.version_label, self.architecture_label]
        for i, label in enumerate(labels):
            label.setObjectName("InfoLabel")
            content_layout.addWidget(label, i // 2, i % 2)

        system_card = ModernCard("System Information", content_widget)
        layout.addWidget(system_card)

    def create_activation_status_card(self, layout):
        """Create activation status card with prominent display"""
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.activation_status_label = QLabel("Activation Status: Checking...")
        self.activation_status_label.setObjectName("ActivationStatus")
        self.activation_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        content_layout.addWidget(self.activation_status_label)

        status_card = ModernCard("Activation Status", content_widget)
        status_card.setObjectName("StatusCard")
        layout.addWidget(status_card)

    def create_version_selection_card(self, layout):
        """Create Windows version selection card"""
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(15)

        # Instruction label
        instruction_label = QLabel("Select your Windows version:")
        instruction_label.setObjectName("InstructionLabel")
        content_layout.addWidget(instruction_label)

        # Version combo box
        self.version_combo = QComboBox()
        self.version_combo.setObjectName("VersionCombo")
        self.version_combo.addItems([
            "Windows 11 Home",
            "Windows 11 Pro",
            "Windows 11 Enterprise",
            "Windows 11 Education",
            "Windows 10 Home",
            "Windows 10 Pro",
            "Windows 10 Enterprise",
            "Windows 10 Education"
        ])
        content_layout.addWidget(self.version_combo)

        # Auto-detect button
        auto_detect_btn = ModernButton("Auto-Detect Current Version", "secondary")
        auto_detect_btn.clicked.connect(self.auto_detect_version)
        content_layout.addWidget(auto_detect_btn)

        version_card = ModernCard("Windows Version Selection", content_widget)
        layout.addWidget(version_card)

    def create_action_buttons(self, layout):
        """Create main action buttons with proper spacing"""
        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)
        button_layout.setSpacing(20)

        # Main activation button
        self.activate_btn = ModernButton("Activate Windows", "primary")
        self.activate_btn.clicked.connect(self.start_activation)

        # Status check button
        self.check_status_btn = ModernButton("Check Status", "secondary")
        self.check_status_btn.clicked.connect(self.check_activation_status)

        # Stop button
        self.stop_btn = ModernButton("Stop Process", "danger")
        self.stop_btn.clicked.connect(self.stop_activation)
        self.stop_btn.setEnabled(False)

        button_layout.addWidget(self.activate_btn)
        button_layout.addWidget(self.check_status_btn)
        button_layout.addWidget(self.stop_btn)

        layout.addWidget(button_widget)

    def create_progress_card(self, layout):
        """Create progress tracking card"""
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(15)

        # Status label
        self.status_label = QLabel("Ready to activate")
        self.status_label.setObjectName("StatusLabel")
        content_layout.addWidget(self.status_label)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("ModernProgressBar")
        self.progress_bar.setMinimumHeight(30)
        content_layout.addWidget(self.progress_bar)

        progress_card = ModernCard("Activation Progress", content_widget)
        layout.addWidget(progress_card)

    def create_log_card(self, layout):
        """Create terminal-style log section"""
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(15)

        # Log text area
        self.log_text = QTextEdit()
        self.log_text.setObjectName("LogTerminal")
        self.log_text.setMinimumHeight(180)
        self.log_text.setReadOnly(True)
        content_layout.addWidget(self.log_text)

        # Clear log button
        clear_log_btn = ModernButton("Clear Log", "secondary")
        clear_log_btn.clicked.connect(self.clear_log)
        content_layout.addWidget(clear_log_btn)

        log_card = ModernCard("Process Log", content_widget)
        layout.addWidget(log_card)

    def create_footer(self, layout):
        """Create application footer"""
        footer_label = QLabel("© 2024 Windows Activator Pro - Educational Purpose Only")
        footer_label.setObjectName("FooterLabel")
        footer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(footer_label)

    def apply_dark_theme(self):
        """Apply modern dark theme styling"""
        dark_stylesheet = """
        /* Main Window and Base Widgets */
        QMainWindow {
            background-color: #1e1e2e;
            color: #cdd6f4;
        }

        /* Labels should have transparent backgrounds */
        QLabel {
            background-color: transparent;
            color: #cdd6f4;
        }

        QScrollArea {
            background-color: #1e1e2e;
            border: none;
        }

        QScrollArea > QWidget > QWidget {
            background-color: #1e1e2e;
        }

        /* Modern Cards */
        QFrame#ModernCard {
            background-color: #313244;
            border: 1px solid #585b70;
            border-radius: 12px;
            margin: 5px;
        }

        QFrame#HeaderCard {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #89b4fa, stop:1 #a6e3a1);
            border: none;
            border-radius: 15px;
        }

        QFrame#StatusCard {
            border: 2px solid #585b70;
        }

        /* Typography */
        QLabel#HeaderTitle {
            font-size: 32px;
            font-weight: bold;
            color: #1e1e2e;
            margin: 10px 0;
        }

        QLabel#HeaderSubtitle {
            font-size: 16px;
            color: #181825;
            margin-bottom: 10px;
        }

        QLabel#CardTitle {
            font-size: 16px;
            font-weight: bold;
            color: #89b4fa;
            margin-bottom: 5px;
        }

        QLabel#InfoLabel {
            font-size: 13px;
            color: #bac2de;
            padding: 8px 0;
            margin: 2px 0;
        }

        QLabel#ActivationStatus {
            font-size: 18px;
            font-weight: bold;
            padding: 15px;
            border-radius: 8px;
            background-color: #45475a;
        }

        QLabel#InstructionLabel {
            font-size: 14px;
            color: #bac2de;
            margin-bottom: 5px;
        }

        QLabel#StatusLabel {
            font-size: 14px;
            font-weight: 600;
            color: #a6e3a1;
            margin-bottom: 5px;
        }

        QLabel#FooterLabel {
            font-size: 11px;
            color: #585b70;
            font-style: italic;
            margin-top: 20px;
        }

        /* Buttons */
        QPushButton#ModernButton_primary {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #a6e3a1, stop:1 #94d3a2);
            color: #1e1e2e;
            border: none;
            border-radius: 10px;
            padding: 12px 24px;
            font-weight: bold;
            font-size: 12px;
        }

        QPushButton#ModernButton_primary:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #b6f3b1, stop:1 #a4e3b2);
        }

        QPushButton#ModernButton_primary:pressed {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #96d391, stop:1 #84c392);
        }

        QPushButton#ModernButton_primary:disabled {
            background-color: #585b70;
            color: #6c6f85;
        }

        QPushButton#ModernButton_secondary {
            background-color: #45475a;
            color: #cdd6f4;
            border: 1px solid #585b70;
            border-radius: 10px;
            padding: 12px 24px;
            font-weight: 500;
            font-size: 12px;
        }

        QPushButton#ModernButton_secondary:hover {
            background-color: #585b70;
            border-color: #89b4fa;
        }

        QPushButton#ModernButton_secondary:pressed {
            background-color: #313244;
        }

        QPushButton#ModernButton_danger {
            background-color: #f38ba8;
            color: #1e1e2e;
            border: none;
            border-radius: 10px;
            padding: 12px 24px;
            font-weight: bold;
            font-size: 12px;
        }

        QPushButton#ModernButton_danger:hover {
            background-color: #f5a3c7;
        }

        QPushButton#ModernButton_danger:pressed {
            background-color: #f173a7;
        }

        QPushButton#ModernButton_danger:disabled {
            background-color: #585b70;
            color: #6c6f85;
        }

        /* ComboBox */
        QComboBox#VersionCombo {
            background-color: #45475a;
            color: #cdd6f4;
            border: 2px solid #585b70;
            border-radius: 8px;
            padding: 12px 16px;
            font-size: 13px;
            min-height: 20px;
        }

        QComboBox#VersionCombo:focus {
            border-color: #89b4fa;
        }

        QComboBox#VersionCombo::drop-down {
            border: none;
            width: 30px;
        }

        QComboBox#VersionCombo::down-arrow {
            image: none;
            border-left: 6px solid transparent;
            border-right: 6px solid transparent;
            border-top: 6px solid #cdd6f4;
            margin-right: 8px;
        }

        QComboBox#VersionCombo QAbstractItemView {
            background-color: #313244;
            color: #cdd6f4;
            border: 1px solid #585b70;
            border-radius: 6px;
            selection-background-color: #89b4fa;
            selection-color: #1e1e2e;
        }

        /* Progress Bar */
        QProgressBar#ModernProgressBar {
            background-color: #45475a;
            border: 2px solid #585b70;
            border-radius: 12px;
            text-align: center;
            font-weight: bold;
            color: #cdd6f4;
            font-size: 12px;
        }

        QProgressBar#ModernProgressBar::chunk {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #89b4fa, stop:1 #a6e3a1);
            border-radius: 10px;
            margin: 2px;
        }

        /* Log Terminal */
        QTextEdit#LogTerminal {
            background-color: #181825;
            color: #a6e3a1;
            border: 2px solid #313244;
            border-radius: 8px;
            font-family: 'Consolas', 'Courier New', monospace;
            font-size: 12px;
            padding: 12px;
            selection-background-color: #45475a;
        }

        /* Scrollbars */
        QScrollBar:vertical {
            background-color: #313244;
            width: 12px;
            border-radius: 6px;
        }

        QScrollBar::handle:vertical {
            background-color: #585b70;
            border-radius: 6px;
            margin: 2px;
        }

        QScrollBar::handle:vertical:hover {
            background-color: #89b4fa;
        }

        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            border: none;
            background: none;
        }

        /* Tab Widget */
        QTabWidget#ModernTabWidget {
            background-color: transparent;
        }

        QTabWidget::pane {
            border: 2px solid #585b70;
            border-radius: 8px;
            background-color: #313244;
            margin-top: -2px;
            padding: 5px;
        }

        QTabWidget::tab-bar {
            alignment: center;
        }

        QTabBar::tab {
            background-color: #45475a;
            color: #cdd6f4;
            padding: 15px 25px;
            margin-right: 3px;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            font-weight: 500;
            font-size: 12px;
            min-width: 120px;
            text-align: center;
        }

        QTabBar::tab:selected {
            background-color: #89b4fa;
            color: #1e1e2e;
            font-weight: bold;
        }

        QTabBar::tab:hover:!selected {
            background-color: #585b70;
        }

        /* List Widget */
        QListWidget#KeysList {
            background-color: #181825;
            color: #cdd6f4;
            border: 2px solid #313244;
            border-radius: 8px;
            padding: 8px;
            font-family: 'Consolas', 'Courier New', monospace;
            font-size: 11px;
        }

        QListWidget#KeysList::item {
            padding: 6px;
            border-bottom: 1px solid #313244;
        }

        QListWidget#KeysList::item:selected {
            background-color: #89b4fa;
            color: #1e1e2e;
        }

        QListWidget#KeysList::item:hover {
            background-color: #45475a;
        }

        /* Text Browser */
        QTextBrowser#InfoBrowser {
            background-color: #181825;
            color: #cdd6f4;
            border: 2px solid #313244;
            border-radius: 8px;
            padding: 15px;
            font-size: 13px;
        }

        /* Additional Labels */
        QLabel#ProgressPercentage {
            font-size: 14px;
            font-weight: bold;
            color: #89b4fa;
        }

        QLabel#OperationDetail {
            font-size: 12px;
            color: #bac2de;
            font-style: italic;
        }

        QLabel#LogStats {
            font-size: 11px;
            color: #585b70;
        }

        QLabel#VersionLabel {
            font-size: 12px;
            font-weight: bold;
            color: #89b4fa;
        }

        /* Admin Status */
        QLabel#AdminStatusGood {
            color: #a6e3a1;
            font-weight: bold;
        }

        QLabel#AdminStatusWarning {
            color: #fab387;
            font-weight: bold;
        }

        QFrame#WarningCard {
            border: 2px solid #fab387;
        }

        QLabel#BuildLabel {
            font-size: 11px;
            color: #585b70;
        }

        /* Server Combo */
        QComboBox#ServerCombo {
            background-color: #45475a;
            color: #cdd6f4;
            border: 2px solid #585b70;
            border-radius: 8px;
            padding: 8px 12px;
            font-size: 12px;
            min-height: 16px;
        }

        QComboBox#ServerCombo:focus {
            border-color: #89b4fa;
        }

        QComboBox#ServerCombo QAbstractItemView {
            background-color: #313244;
            color: #cdd6f4;
            border: 1px solid #585b70;
            border-radius: 6px;
            selection-background-color: #89b4fa;
            selection-color: #1e1e2e;
        }
        """

        self.setStyleSheet(dark_stylesheet)

    # Add new method implementations
    def run_sfc_scan(self):
        """Run System File Checker"""
        try:
            subprocess.Popen("sfc /scannow", shell=True)
            self.log_message("🔧 System File Checker started")
        except Exception as e:
            self.log_message(f"❌ Failed to start SFC: {str(e)}")

    def run_disk_cleanup(self):
        """Run Disk Cleanup"""
        try:
            subprocess.Popen("cleanmgr", shell=True)
            self.log_message("🧹 Disk Cleanup started")
        except Exception as e:
            self.log_message(f"❌ Failed to start Disk Cleanup: {str(e)}")

    def show_system_info(self):
        """Show system information"""
        try:
            subprocess.Popen("msinfo32", shell=True)
            self.log_message("📊 System Information opened")
        except Exception as e:
            self.log_message(f"❌ Failed to open System Information: {str(e)}")

    def check_windows_updates(self):
        """Check for Windows updates"""
        try:
            subprocess.Popen("ms-settings:windowsupdate", shell=True)
            self.log_message("🔄 Windows Update settings opened")
        except Exception as e:
            self.log_message(f"❌ Failed to open Windows Update: {str(e)}")

    def open_display_settings(self):
        """Open display settings"""
        try:
            subprocess.Popen("ms-settings:display", shell=True)
            self.log_message("🖥️ Display settings opened")
        except Exception as e:
            self.log_message(f"❌ Failed to open Display settings: {str(e)}")

    def open_sound_settings(self):
        """Open sound settings"""
        try:
            subprocess.Popen("ms-settings:sound", shell=True)
            self.log_message("🔊 Sound settings opened")
        except Exception as e:
            self.log_message(f"❌ Failed to open Sound settings: {str(e)}")

    def open_network_settings(self):
        """Open network settings"""
        try:
            subprocess.Popen("ms-settings:network", shell=True)
            self.log_message("🌐 Network settings opened")
        except Exception as e:
            self.log_message(f"❌ Failed to open Network settings: {str(e)}")

    def open_defender(self):
        """Open Windows Defender"""
        try:
            subprocess.Popen("windowsdefender:", shell=True)
            self.log_message("🛡️ Windows Defender opened")
        except Exception as e:
            self.log_message(f"❌ Failed to open Windows Defender: {str(e)}")

    def quick_activation_check(self):
        """Quick activation status check"""
        self.log_message("⚡ Performing quick activation check...")
        self.check_activation_status_silent()

    def save_log(self):
        """Save log to file"""
        try:
            import datetime
            filename = f"activation_log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(self.log_text.toPlainText())
            self.log_message(f"💾 Log saved to {filename}")
            QMessageBox.information(self, "Log Saved", f"Log saved to {filename}")
        except Exception as e:
            self.log_message(f"❌ Failed to save log: {str(e)}")

    def copy_log(self):
        """Copy log to clipboard"""
        try:
            clipboard = QApplication.clipboard()
            log_text = self.log_text.toPlainText()
            clipboard.setText(log_text)
            self.log_message("📋 Log copied to clipboard")
            QMessageBox.information(self, "Log Copied", "Log has been copied to clipboard")
        except Exception as e:
            self.log_message(f"❌ Failed to copy log: {str(e)}")

    def export_log(self):
        """Export log with detailed information"""
        try:
            import datetime
            filename = f"activation_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

            report = f"""
Windows Activator Pro - Detailed Report
Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
========================================

System Information:
{self.os_label.text()}
{self.version_label.text()}
{self.architecture_label.text()}

Activation Status:
{self.activation_status_label.text()}

Process Log:
{self.log_text.toPlainText()}

========================================
End of Report
"""

            with open(filename, 'w', encoding='utf-8') as f:
                f.write(report)
            self.log_message(f"📤 Report exported to {filename}")
            QMessageBox.information(self, "Report Exported", f"Detailed report exported to {filename}")
        except Exception as e:
            self.log_message(f"❌ Failed to export report: {str(e)}")

    def show_disclaimer(self):
        """Show legal disclaimer"""
        disclaimer_text = """
        LEGAL DISCLAIMER

        This software is provided for educational purposes only.

        • This tool uses publicly available Microsoft Generic Volume License Keys (GVLK)
        • Users are responsible for ensuring they have proper Windows licensing
        • The developers assume no responsibility for misuse of this software
        • This tool should only be used on systems you own or have explicit permission to modify
        • Always comply with Microsoft's Software License Terms

        By using this software, you acknowledge that you understand and accept these terms.
        """
        QMessageBox.information(self, "Legal Disclaimer", disclaimer_text)

    def show_help(self):
        """Show help information"""
        help_text = """
        HELP & SUPPORT

        How to use Windows Activator Pro:

        1. 🔍 Auto-detect your Windows version or select manually
        2. 🚀 Click "ACTIVATE WINDOWS" to start the process
        3. 📊 Monitor progress in the status panel
        4. 📋 Check the log for detailed information

        Troubleshooting:
        • Make sure you're running as Administrator
        • Check your internet connection
        • Try different KMS servers if activation fails
        • Verify your Windows version selection is correct

        Additional Tools:
        • Use the Tools tab for system maintenance
        • Check the Information tab for detailed documentation
        • Export logs for technical support
        """
        QMessageBox.information(self, "Help & Support", help_text)

    def show_about(self):
        """Show about information"""
        about_text = """
        Windows Activator Pro v2.0.0
        Advanced Edition

        A modern, feature-rich Windows activation tool with dark theme UI.

        Features:
        ✅ Modern dark theme interface
        ✅ Tabbed interface with multiple tools
        ✅ Real-time progress tracking
        ✅ Comprehensive system information
        ✅ Built-in system utilities
        ✅ Detailed logging and reporting
        ✅ Multiple KMS server support
        ✅ Auto-detection capabilities

        Built with PyQt5 and modern design principles.

        © 2024 - Educational Purpose Only
        """
        QMessageBox.information(self, "About Windows Activator Pro", about_text)

    def update_progress(self, value):
        """Update progress bar with percentage display"""
        self.progress_bar.setValue(value)
        self.progress_percentage.setText(f"{value}%")

        # Update status icon based on progress
        if value == 0:
            self.status_icon.setText("🔵")
        elif value < 50:
            self.status_icon.setText("🟡")
        elif value < 100:
            self.status_icon.setText("🟠")
        else:
            self.status_icon.setText("🟢")

    def update_status(self, message):
        """Update status label, operation detail, and log"""
        self.status_label.setText(message)
        self.operation_detail.setText(f"Current: {message}")
        self.log_message(f"ℹ {message}")

    def log_message(self, message):
        """Enhanced log message with statistics update"""
        timestamp = time.strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"
        self.log_text.append(formatted_message)

        # Update log statistics
        line_count = len(self.log_text.toPlainText().split('\n'))
        self.log_lines_count.setText(f"Lines: {line_count}")
        self.last_update_time.setText(f"Last update: {timestamp}")

        # Auto-scroll to bottom
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def setup_system_info(self):
        """Setup comprehensive system information detection"""
        try:
            # Get OS information
            os_info = platform.system() + " " + platform.release()
            self.os_label.setText(f"OS: {os_info}")

            # Get version
            version_info = platform.version()
            self.version_label.setText(f"Version: {version_info}")

            # Get architecture
            arch_info = platform.architecture()[0]
            self.architecture_label.setText(f"Architecture: {arch_info}")

            # Get performance information
            self.update_performance_info()

            # Check activation status
            self.check_activation_status_silent()

            # Initialize log statistics
            self.log_lines_count.setText("Lines: 0")
            self.last_update_time.setText("Last update: Never")

            self.log_message("🚀 Windows Activator Pro initialized successfully")
            self.log_message("ℹ System information loaded")

        except Exception as e:
            self.log_message(f"❌ Error getting system info: {str(e)}")

    def update_performance_info(self):
        """Update performance information with robust parsing"""
        try:
            # Get CPU info with better parsing
            try:
                result = subprocess.run("wmic cpu get name /format:list", shell=True, capture_output=True, text=True, timeout=10)
                if result.stdout:
                    lines = [line.strip() for line in result.stdout.split('\n') if line.strip()]
                    cpu_name = None
                    for line in lines:
                        if line.startswith('Name=') and len(line) > 5:
                            cpu_name = line[5:].strip()
                            break

                    if cpu_name:
                        # Clean up CPU name
                        cpu_name = cpu_name.replace('(R)', '').replace('(TM)', '').replace('  ', ' ').strip()
                        if len(cpu_name) > 45:
                            cpu_name = cpu_name[:42] + "..."
                        self.cpu_label.setText(f"CPU: {cpu_name}")
                    else:
                        # Fallback method
                        result2 = subprocess.run("wmic cpu get name", shell=True, capture_output=True, text=True, timeout=10)
                        lines2 = [line.strip() for line in result2.stdout.split('\n') if line.strip() and line.strip() != 'Name']
                        if lines2:
                            cpu_name = lines2[0].replace('(R)', '').replace('(TM)', '').replace('  ', ' ').strip()
                            if len(cpu_name) > 45:
                                cpu_name = cpu_name[:42] + "..."
                            self.cpu_label.setText(f"CPU: {cpu_name}")
                        else:
                            self.cpu_label.setText("CPU: Detection failed")
                else:
                    self.cpu_label.setText("CPU: No output")
            except Exception as e:
                self.cpu_label.setText("CPU: Not available")
                self.log_message(f"CPU detection error: {str(e)}")

            # Get memory info with better parsing
            try:
                result = subprocess.run('wmic computersystem get TotalPhysicalMemory /format:list', shell=True, capture_output=True, text=True, timeout=10)
                if result.stdout:
                    lines = [line.strip() for line in result.stdout.split('\n') if line.strip()]
                    memory_bytes = None
                    for line in lines:
                        if line.startswith('TotalPhysicalMemory=') and len(line) > 20:
                            memory_str = line[20:].strip()
                            if memory_str.isdigit():
                                memory_bytes = int(memory_str)
                                break

                    if memory_bytes:
                        memory_gb = round(memory_bytes / (1024**3), 1)
                        self.memory_label.setText(f"Memory: {memory_gb} GB")
                    else:
                        # Fallback method
                        result2 = subprocess.run('wmic computersystem get TotalPhysicalMemory', shell=True, capture_output=True, text=True, timeout=10)
                        lines2 = [line.strip() for line in result2.stdout.split('\n') if line.strip() and line.strip() != 'TotalPhysicalMemory']
                        if lines2 and lines2[0].isdigit():
                            memory_gb = round(int(lines2[0]) / (1024**3), 1)
                            self.memory_label.setText(f"Memory: {memory_gb} GB")
                        else:
                            self.memory_label.setText("Memory: Detection failed")
                else:
                    self.memory_label.setText("Memory: No output")
            except Exception as e:
                self.memory_label.setText("Memory: Not available")
                self.log_message(f"Memory detection error: {str(e)}")

            # Get uptime with multiple methods
            try:
                import psutil
                boot_time = psutil.boot_time()
                from datetime import datetime
                uptime = datetime.now() - datetime.fromtimestamp(boot_time)
                days = uptime.days
                hours, remainder = divmod(uptime.seconds, 3600)
                minutes, _ = divmod(remainder, 60)
                self.uptime_label.setText(f"Uptime: {days}d {hours}h {minutes}m")
            except ImportError:
                # Fallback to WMIC if psutil is not available
                try:
                    result = subprocess.run("wmic os get lastbootuptime /format:list", shell=True, capture_output=True, text=True, timeout=10)
                    if result.stdout:
                        lines = [line.strip() for line in result.stdout.split('\n') if line.strip()]
                        boot_time_str = None
                        for line in lines:
                            if line.startswith('LastBootUpTime=') and len(line) > 15:
                                boot_time_str = line[15:].strip()
                                break

                        if boot_time_str and len(boot_time_str) >= 14:
                            # Parse the WMI datetime format
                            boot_time = boot_time_str[:14]
                            from datetime import datetime
                            boot_datetime = datetime.strptime(boot_time, "%Y%m%d%H%M%S")
                            uptime = datetime.now() - boot_datetime
                            days = uptime.days
                            hours, remainder = divmod(uptime.seconds, 3600)
                            minutes, _ = divmod(remainder, 60)
                            self.uptime_label.setText(f"Uptime: {days}d {hours}h {minutes}m")
                        else:
                            self.uptime_label.setText("Uptime: Parse failed")
                    else:
                        self.uptime_label.setText("Uptime: No output")
                except Exception as e:
                    self.uptime_label.setText("Uptime: Not available")
                    self.log_message(f"Uptime detection error: {str(e)}")
            except Exception as e:
                self.uptime_label.setText("Uptime: Error")
                self.log_message(f"Uptime detection error: {str(e)}")

        except Exception as e:
            self.log_message(f"⚠ Error updating performance info: {str(e)}")

    def auto_detect_version(self):
        """Auto-detect current Windows version"""
        try:
            # Get Windows edition
            result = subprocess.run("wmic os get Caption", shell=True,
                                  capture_output=True, text=True)

            if result.stdout:
                output = result.stdout.lower()
                if "windows 11" in output:
                    if "home" in output:
                        self.version_combo.setCurrentText("Windows 11 Home")
                    elif "pro" in output:
                        self.version_combo.setCurrentText("Windows 11 Pro")
                    elif "enterprise" in output:
                        self.version_combo.setCurrentText("Windows 11 Enterprise")
                    elif "education" in output:
                        self.version_combo.setCurrentText("Windows 11 Education")
                elif "windows 10" in output:
                    if "home" in output:
                        self.version_combo.setCurrentText("Windows 10 Home")
                    elif "pro" in output:
                        self.version_combo.setCurrentText("Windows 10 Pro")
                    elif "enterprise" in output:
                        self.version_combo.setCurrentText("Windows 10 Enterprise")
                    elif "education" in output:
                        self.version_combo.setCurrentText("Windows 10 Education")

                self.log_message("✓ Windows version auto-detected successfully")
            else:
                self.log_message("⚠ Could not auto-detect Windows version")

        except Exception as e:
            self.log_message(f"✗ Error auto-detecting version: {str(e)}")

    def check_activation_status_silent(self):
        """Check activation status without user interaction"""
        try:
            result = subprocess.run("cscript //nologo C:\\Windows\\System32\\slmgr.vbs /xpr",
                                  shell=True, capture_output=True, text=True, timeout=10)

            if "permanently activated" in result.stdout.lower():
                self.activation_status_label.setText("✅ Windows is Activated")
                self.activation_status_label.setStyleSheet("""
                    QLabel#ActivationStatus {
                        color: #a6e3a1;
                        background-color: rgba(166, 227, 161, 0.1);
                        border: 2px solid #a6e3a1;
                    }
                """)
            else:
                self.activation_status_label.setText("❌ Windows Not Activated")
                self.activation_status_label.setStyleSheet("""
                    QLabel#ActivationStatus {
                        color: #f38ba8;
                        background-color: rgba(243, 139, 168, 0.1);
                        border: 2px solid #f38ba8;
                    }
                """)

        except Exception:
            self.activation_status_label.setText("❓ Status Unknown")
            self.activation_status_label.setStyleSheet("""
                QLabel#ActivationStatus {
                    color: #fab387;
                    background-color: rgba(250, 179, 135, 0.1);
                    border: 2px solid #fab387;
                }
            """)

    def check_activation_status(self):
        """Check and display activation status"""
        try:
            self.log_message("🔍 Checking activation status...")
            result = subprocess.run("cscript //nologo C:\\Windows\\System32\\slmgr.vbs /dlv",
                                  shell=True, capture_output=True, text=True, timeout=15)

            if result.stdout:
                # Show detailed activation info
                QMessageBox.information(self, "Activation Status", result.stdout)
                self.log_message("✓ Activation status checked successfully")
            else:
                QMessageBox.warning(self, "Error", "Could not retrieve activation status")

        except subprocess.TimeoutExpired:
            QMessageBox.warning(self, "Timeout", "Activation status check timed out")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error checking activation status: {str(e)}")

    def test_activation_commands(self):
        """Test if activation commands work properly"""
        self.log_message("🧪 Testing activation commands...")

        try:
            # Test basic slmgr command
            result = subprocess.run("cscript //nologo C:\\Windows\\System32\\slmgr.vbs /?",
                                  shell=True, capture_output=True, text=True, timeout=10)

            if result.returncode == 0:
                self.log_message("✅ slmgr.vbs is available and working")

                # Test getting current license info
                result2 = subprocess.run("cscript //nologo C:\\Windows\\System32\\slmgr.vbs /dli",
                                       shell=True, capture_output=True, text=True, timeout=15)

                if result2.stdout:
                    self.log_message("✅ License information retrieved successfully")
                    self.log_message(f"Current license info: {result2.stdout[:200]}...")
                else:
                    self.log_message("⚠️ Could not retrieve license information")

                # Check admin privileges
                if self.is_admin():
                    self.log_message("✅ Running with administrator privileges")
                else:
                    self.log_message("❌ NOT running with administrator privileges - this will cause issues")

            else:
                self.log_message(f"❌ slmgr.vbs test failed with return code: {result.returncode}")
                self.log_message(f"Error output: {result.stderr}")

        except subprocess.TimeoutExpired:
            self.log_message("⚠️ Command test timed out")
        except Exception as e:
            self.log_message(f"❌ Error testing commands: {str(e)}")

    def start_activation(self):
        """Start the Windows activation process"""
        if self.worker and self.worker.isRunning():
            QMessageBox.warning(self, "Process Running", "Activation is already in progress!")
            return

        # Confirm activation
        reply = QMessageBox.question(self, "Confirm Activation",
                                   f"Are you sure you want to activate {self.version_combo.currentText()}?",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply != QMessageBox.StandardButton.Yes:
            return

        # Check admin privileges upfront
        if not self.is_admin():
            admin_reply = QMessageBox.question(self, "Admin Rights Required",
                                             "Administrator privileges are required for Windows activation.\n\n"
                                             "Would you like to restart the application with admin rights now?",
                                             QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if admin_reply == QMessageBox.StandardButton.Yes:
                self.restart_as_admin()
                return
            else:
                proceed_reply = QMessageBox.question(self, "Continue Anyway?",
                                                   "Activation will likely fail without admin rights.\n\n"
                                                   "Continue anyway?",
                                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                if proceed_reply != QMessageBox.StandardButton.Yes:
                    return

        # Disable buttons and reset progress
        self.activate_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.progress_bar.setValue(0)

        # Clear log and start process
        self.log_message("═" * 60)
        self.log_message(f"🚀 Starting activation for {self.version_combo.currentText()}")
        self.log_message("═" * 60)

        # Create and start worker thread
        self.worker = ActivationWorker(self.version_combo.currentText())
        self.worker.progress_updated.connect(self.update_progress)
        self.worker.status_updated.connect(self.update_status)
        self.worker.activation_completed.connect(self.activation_finished)
        self.worker.start()

    def stop_activation(self):
        """Stop the activation process"""
        if self.worker and self.worker.isRunning():
            self.worker.stop()
            self.worker.wait(3000)  # Wait up to 3 seconds

            self.log_message("🛑 Activation process stopped by user")
            self.activation_finished(False, "Process stopped by user")

    def update_progress(self, value):
        """Update progress bar"""
        self.progress_bar.setValue(value)

    def update_status(self, message):
        """Update status label and log"""
        self.status_label.setText(message)
        self.log_message(f"ℹ {message}")

    def activation_finished(self, success, message):
        """Handle activation completion"""
        # Re-enable buttons
        self.activate_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)

        # Update UI
        if success:
            self.status_label.setText("✅ Activation Successful!")
            self.status_label.setStyleSheet("QLabel#StatusLabel { color: #a6e3a1; }")
            self.progress_bar.setValue(100)
            QMessageBox.information(self, "Success", message)

            # Update activation status
            self.check_activation_status_silent()
        else:
            self.status_label.setText("❌ Activation Failed")
            self.status_label.setStyleSheet("QLabel#StatusLabel { color: #f38ba8; }")

            # Auto-handle admin privileges
            if "access denied" in message.lower() or not self.is_admin():
                reply = QMessageBox.question(self, "Admin Rights Required",
                                           "Administrator privileges are required for Windows activation.\n\n"
                                           "Would you like to restart the application with admin rights?",
                                           QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                if reply == QMessageBox.StandardButton.Yes:
                    self.restart_as_admin()
                else:
                    QMessageBox.information(self, "Note", "You can manually restart as administrator later for full functionality.")
            else:
                QMessageBox.warning(self, "Activation Failed", message)

        self.log_message("═" * 60)
        self.log_message(f"🏁 Activation completed: {message}")
        self.log_message("═" * 60)

    def log_message(self, message):
        """Add message to log with timestamp"""
        timestamp = time.strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"
        self.log_text.append(formatted_message)

        # Auto-scroll to bottom
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def clear_log(self):
        """Clear the log text"""
        self.log_text.clear()
        self.log_message("🧹 Log cleared")

    def closeEvent(self, event):
        """Handle application close event"""
        if self.worker and self.worker.isRunning():
            reply = QMessageBox.question(self, "Confirm Exit",
                                       "Activation is in progress. Are you sure you want to exit?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

            if reply == QMessageBox.StandardButton.Yes:
                self.worker.stop()
                self.worker.wait(3000)
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)

    # Set application properties
    app.setApplicationName("Windows Activator Pro")
    app.setApplicationVersion("2.0.0")
    app.setOrganizationName("Windows Activator Pro")

    # Set application-wide dark theme
    app.setStyle('Fusion')  # Use Fusion style for better dark theme support

    # Create dark palette
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.ColorRole.Window, QColor(30, 30, 46))
    dark_palette.setColor(QPalette.ColorRole.WindowText, QColor(205, 214, 244))
    dark_palette.setColor(QPalette.ColorRole.Base, QColor(24, 24, 37))
    dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(49, 50, 68))
    dark_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(205, 214, 244))
    dark_palette.setColor(QPalette.ColorRole.ToolTipText, QColor(205, 214, 244))
    dark_palette.setColor(QPalette.ColorRole.Text, QColor(205, 214, 244))
    dark_palette.setColor(QPalette.ColorRole.Button, QColor(69, 71, 90))
    dark_palette.setColor(QPalette.ColorRole.ButtonText, QColor(205, 214, 244))
    dark_palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ColorRole.Link, QColor(137, 180, 250))
    dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(137, 180, 250))
    dark_palette.setColor(QPalette.ColorRole.HighlightedText, QColor(30, 30, 46))

    app.setPalette(dark_palette)

    # Check if running as administrator
    try:
        import ctypes
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        if not is_admin:
            QMessageBox.warning(None, "Administrator Required",
                              "This application requires administrator privileges to function properly.\n"
                              "Please run as administrator.")
    except:
        pass

    # Create and show main window
    window = WindowsActivatorGUI()
    window.show()

    # Start event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()