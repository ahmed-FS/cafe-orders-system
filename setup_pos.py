"""
POS Device Setup Script for Café Billing System
Installs required dependencies and configures printer access
"""

import subprocess
import sys
import platform
import os

def install_windows_dependencies():
    """Install Windows-specific dependencies"""
    print("Installing Windows POS dependencies...")
    
    packages = [
        "pywin32==306",
        "python-escpos==3.1",
        "pyusb"
    ]
    
    for package in packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✓ Installed {package}")
        except subprocess.CalledProcessError:
            print(f"✗ Failed to install {package}")

def install_android_dependencies():
    """Install Android-specific dependencies"""
    print("Installing Android POS dependencies...")
    
    packages = [
        "pybluez",
        "android-usb-printer",
        "python-escpos==3.1"
    ]
    
    for package in packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✓ Installed {package}")
        except subprocess.CalledProcessError:
            print(f"✗ Failed to install {package}")

def test_printer_access():
    """Test printer access on current platform"""
    print("\nTesting printer access...")
    
    system = platform.system().lower()
    
    if system == "windows":
        try:
            import win32print
            printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL)
            print(f"Found {len(printers)} printers:")
            for i, printer in enumerate(printers):
                print(f"  {i+1}. {printer[2]}")
        except ImportError:
            print("✗ win32print not available")
    
    elif system == "linux":
        try:
            usb_devices = os.listdir("/dev/usb")
            print(f"Found USB devices: {usb_devices}")
        except:
            print("No USB devices found")
    
    elif system == "android":
        pos_paths = [
            "/dev/usb/lp0",
            "/dev/usb/lp1", 
            "/dev/ttyUSB0",
            "/dev/ttyS0"
        ]
        
        for path in pos_paths:
            if os.path.exists(path):
                print(f"✓ Found POS device: {path}")
                return
        
        print("No POS devices found")

def main():
    print("=== Café Billing System POS Setup ===")
    print(f"Platform: {platform.system()}")
    
    system = platform.system().lower()
    
    if system == "windows":
        install_windows_dependencies()
    elif system == "linux":
        install_windows_dependencies()  
    elif system == "android":
        install_android_dependencies()
    else:
        print("Unsupported platform")
        return
    
    test_printer_access()
    
    print("\n=== Setup Complete ===")
    print("Run the café billing system with: python cafe_billing_system.py")

if __name__ == "__main__":
    main()
