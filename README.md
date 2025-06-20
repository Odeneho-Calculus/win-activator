# Windows Activator Pro - Modern GUI

A modern, user-friendly PyQt5 application for Windows activation with an intuitive interface and advanced features.

## 🌟 Features

- **Modern UI Design**: Clean, professional interface with gradient backgrounds and smooth animations
- **Multi-Version Support**: Supports Windows 10 and Windows 11 (Home, Pro, Enterprise, Education)
- **Auto-Detection**: Automatically detects your current Windows version
- **Real-time Progress**: Live progress tracking with detailed status updates
- **System Information**: Displays comprehensive system details and activation status
- **Process Logging**: Detailed log output for troubleshooting
- **Admin Detection**: Automatically checks for administrator privileges
- **Threaded Operations**: Non-blocking UI with background processing
- **Error Handling**: Robust error handling with user-friendly messages

## 📋 Requirements

- **Operating System**: Windows 10/11
- **Python**: 3.7 or higher
- **Administrator Privileges**: Required for Windows activation
- **Dependencies**: PyQt5, PyInstaller (automatically installed)

## 🚀 Quick Start

### Method 1: Automated Setup (Recommended)

1. **Download/Clone** the project files
2. **Run the setup script**:
   ```bash
   python setup.py
   ```
3. **Choose option 4** for full setup (installs dependencies and builds executable)
4. **Run the application**:
   - For testing: `python main.py`
   - For production: Use `RunAsAdmin.bat` or `dist/WindowsActivatorPro.exe`

### Method 2: Manual Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application**:
   ```bash
   python main.py
   ```

3. **Build executable** (optional):
   ```bash
   pyinstaller --onefile --windowed --name=WindowsActivatorPro main.py
   ```

## 🖥️ Usage Instructions

### Running the Application

1. **Administrator Rights**: The application must be run as administrator
2. **Launch Options**:
   - **Development**: `python main.py`
   - **Executable**: Double-click `WindowsActivatorPro.exe`
   - **Admin Launcher**: Use `RunAsAdmin.bat` for automatic elevation

### Using the Interface

1. **System Information**: View your current Windows details and activation status
2. **Version Selection**:
   - Use the dropdown to select your Windows version
   - Click "Auto-Detect" to automatically identify your version
3. **Activation Process**:
   - Click "Activate Windows" to start the process
   - Monitor progress in real-time
   - View detailed logs in the Process Log section
4. **Status Checking**: Use "Check Activation Status" for detailed activation information

### Interface Sections

- **Header**: Application title and branding
- **System Information**: OS details, version, architecture, activation status
- **Version Selection**: Windows version dropdown with auto-detection
- **Action Buttons**: Main controls (Activate, Check Status, Stop)
- **Progress Section**: Real-time progress bar and status updates
- **Process Log**: Detailed operation logs with timestamps
- **Footer**: Application information

## 🔧 Technical Details

### Architecture

- **Main Thread**: UI operations and user interactions
- **Worker Thread**: Background activation process to prevent UI freezing
- **Signal/Slot System**: PyQt5 communication between threads

### Activation Process

1. **Preparation**: Clear existing product keys and KMS settings
2. **Key Installation**: Install appropriate product key for selected Windows version
3. **KMS Connection**: Connect to KMS servers (multiple fallback servers)
4. **Activation**: Execute activation command and verify success
5. **Verification**: Check final activation status

### KMS Servers

The application uses multiple KMS servers for reliability:
- kms7.MSGuides.com
- kms8.MSGuides.com
- kms9.MSGuides.com

### Product Keys

The application includes Generic Volume License Keys (GVLK) for:
- Windows 11: Home, Pro, Enterprise, Education
- Windows 10: Home, Pro, Enterprise, Education

## 📦 Building Executable

### Simple Build
```bash
python setup.py
# Choose option 2 or 4
```

### Advanced Build with Custom Options
```bash
pyinstaller WindowsActivatorPro.spec
```

### Build Options Explained

- `--onefile`: Creates single executable file
- `--windowed`: Removes console window
- `--name`: Sets executable name
- `--icon`: Adds application icon (if available)
- `--clean`: Cleans build cache
- `--hidden-import`: Includes required PyQt5 modules

## 🛠️ Customization

### Styling

The application uses modern CSS-like styling through PyQt5 stylesheets:
- **Colors**: Professional blue/green gradient theme
- **Fonts**: Segoe UI for Windows consistency
- **Effects**: Hover effects, rounded corners, shadows
- **Responsive**: Adapts to different window sizes

### Adding New Windows Versions

To add support for new Windows versions:

1. **Update product_keys dictionary** in `ActivationWorker` class
2. **Add version to combo box** in `create_version_selection` method
3. **Update auto-detection logic** in `auto_detect_version` method

### Modifying KMS Servers

To change or add KMS servers:
- Edit the `kms_servers` list in `ActivationWorker` class

## 🔒 Security Considerations

- **Administrator Privileges**: Required for system-level operations
- **Network Communication**: Connects to external KMS servers
- **System Modification**: Modifies Windows licensing settings
- **Antivirus**: May be flagged by antivirus software (false positive)

## 🐛 Troubleshooting

### Common Issues

1. **"Access Denied" Error**:
   - Solution: Run as administrator
   - Use `RunAsAdmin.bat` launcher

2. **"Module not found" Error**:
   - Solution: Install dependencies
   - Run: `pip install -r requirements.txt`

3. **Activation Fails**:
   - Check internet connection
   - Verify Windows version selection
   - Try different KMS server (automatic fallback)

4. **UI Not Responding**:
   - Wait for background process to complete
   - Use "Stop Process" button if needed

### Debug Mode

For debugging, run with Python directly:
```bash
python main.py
```

Check the Process Log section for detailed error messages.

## 📄 File Structure

```
win-activator/
├── main.py                    # Main application file
├── requirements.txt           # Python dependencies
├── setup.py                  # Setup and build script
├── README.md                 # This documentation
├── win.txt                   # Original batch script
├── WindowsActivatorPro.spec  # PyInstaller spec file (generated)
├── version_info.txt          # Executable version info (generated)
├── RunAsAdmin.bat           # Admin launcher (generated)
├── build/                   # Build cache (generated)
├── dist/                    # Final executable (generated)
│   └── WindowsActivatorPro.exe
└── __pycache__/            # Python cache (generated)
```

## ⚖️ Legal Notice

**IMPORTANT**: This software is provided for educational purposes only.

- Use only on systems you own or have explicit permission to modify
- Ensure compliance with Microsoft's licensing terms
- The developers are not responsible for any misuse
- This tool uses publicly available Generic Volume License Keys (GVLK)

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For issues and questions:
- Check the troubleshooting section
- Review the Process Log for error details
- Ensure administrator privileges
- Verify internet connectivity

## 🔄 Version History

### v1.0.0 (Current)
- Initial release
- Modern PyQt5 interface
- Multi-version Windows support
- Auto-detection capabilities
- Threaded activation process
- Comprehensive logging
- Executable generation

## 🎯 Future Enhancements

- [ ] Dark/Light theme toggle
- [ ] Custom KMS server configuration
- [ ] Activation scheduling
- [ ] Multiple language support
- [ ] System tray integration
- [ ] Automatic updates
- [ ] Enhanced error recovery

---

**© 2024 Windows Activator Pro - Educational Purpose Only**