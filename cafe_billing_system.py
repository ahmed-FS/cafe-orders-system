import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import subprocess
import sys
import platform
import os

class CafeBillingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("☕ Café Billing System ☕")
        self.root.geometry("800x600")
        self.root.configure(bg='#f5f5dc')
        
        # Menu items and prices
        self.menu_items = {
            "Coffee": 10,
            "Tea": 8,
            "Juice": 12,
            "Pastry": 15,
            "Sandwich": 25,
            "Cake": 20,
            "Water": 5,
            "Soda": 7
        }
        
        self.order_items = []
        self.total_amount = 0
        
        self.setup_ui()
    
    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg='#f5f5dc')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left panel - Menu
        menu_frame = tk.Frame(main_frame, bg='#8b7355', relief=tk.GROOVE, bd=3)
        menu_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        tk.Label(menu_frame, text="☕ MENU ☕", font=("Times New Roman", 18, "bold"), 
                bg='#8b7355', fg='#fff8dc').pack(pady=15)
        
        # Menu buttons
        for item, price in self.menu_items.items():
            btn = tk.Button(menu_frame, text=f"{item}\n{price} DH", 
                          font=("Times New Roman", 12, "bold"), width=15, height=2,
                          bg='#d2b48c', fg='#5d4e37',
                          relief=tk.RAISED, bd=2,
                          command=lambda i=item, p=price: self.add_item(i, p))
            btn.pack(pady=8, padx=15)
        
        # Right panel - Order
        order_frame = tk.Frame(main_frame, bg='#8b7355', relief=tk.GROOVE, bd=3)
        order_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        tk.Label(order_frame, text="📋 ORDER 📋", font=("Times New Roman", 18, "bold"),
                bg='#8b7355', fg='#fff8dc').pack(pady=15)
        
        # Order list
        self.order_listbox = tk.Listbox(order_frame, font=("Times New Roman", 11),
                                       bg='#fff8dc', selectmode=tk.SINGLE,
                                       relief=tk.SUNKEN, bd=2)
        self.order_listbox.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Total display
        self.total_label = tk.Label(order_frame, text="Total: 0 DH", 
                                   font=("Times New Roman", 16, "bold"),
                                   bg='#8b7355', fg='#ffd700')
        self.total_label.pack(pady=15)
        
        # Action buttons
        button_frame = tk.Frame(order_frame, bg='#8b7355')
        button_frame.pack(pady=15)
        
        tk.Button(button_frame, text="🗑️ Clear", font=("Times New Roman", 12, "bold"),
                 bg='#cd5c5c', fg='white', width=10,
                 relief=tk.RAISED, bd=2,
                 command=self.clear_order).pack(side=tk.LEFT, padx=8)
        
        tk.Button(button_frame, text="🧾 Print", font=("Times New Roman", 12, "bold"),
                 bg='#228b22', fg='white', width=10,
                 relief=tk.RAISED, bd=2,
                 command=self.print_receipt).pack(side=tk.LEFT, padx=8)
        
        tk.Button(button_frame, text="🚪 Exit", font=("Times New Roman", 12, "bold"),
                 bg='#696969', fg='white', width=8,
                 relief=tk.RAISED, bd=2,
                 command=self.root.quit).pack(side=tk.LEFT, padx=8)
    
    def add_item(self, item_name, price):
        """Add item to order and update total"""
        self.order_items.append({"name": item_name, "price": price})
        self.order_listbox.insert(tk.END, f"{item_name} - {price} DH")
        self.update_total()
    
    def update_total(self):
        """Calculate and display total amount"""
        self.total_amount = sum(item["price"] for item in self.order_items)
        self.total_label.config(text=f"Total: {self.total_amount} DH")
    
    def clear_order(self):
        """Clear all items from order"""
        self.order_items.clear()
        self.order_listbox.delete(0, tk.END)
        self.update_total()
    
    def print_receipt(self):
        """Print receipt using thermal printer or save to file"""
        if not self.order_items:
            messagebox.showwarning("Warning", "No items to print!")
            return
        
        receipt_text = self.generate_receipt_text()
        
        try:
            # Try to print with thermal printer
            self.thermal_print(receipt_text)
        except:
            # Fallback: save to file
            self.save_receipt_to_file(receipt_text)
            messagebox.showinfo("Info", "Receipt saved to receipt.txt")
    
    def generate_receipt_text(self):
        """Generate formatted receipt text"""
        receipt = "=" * 30 + "\n"
        receipt += "     CAFÉ RECEIPT\n"
        receipt += "=" * 30 + "\n"
        receipt += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        receipt += "-" * 30 + "\n"
        
        for item in self.order_items:
            receipt += f"{item['name']:<15} {item['price']:>8} DH\n"
        
        receipt += "-" * 30 + "\n"
        receipt += f"{'TOTAL':<15} {self.total_amount:>8} DH\n"
        receipt += "=" * 30 + "\n"
        receipt += "     Thank you!\n"
        
        return receipt
    
    def thermal_print(self, text):
        """Print to thermal printer with POS device support"""
        try:
            system = platform.system().lower()
            
            if system == "android":
                # Android POS device printing
                self.android_pos_print(text)
            elif system == "windows":
                # Windows - try POS printer first, then USB
                if not self.windows_pos_print(text):
                    self.windows_usb_print(text)
            else:
                # Fallback to USB printing
                self.windows_usb_print(text)
                
        except Exception as e:
            raise Exception(f"Printer error: {str(e)}")
    
    def android_pos_print(self, text):
        """Print on Android POS devices"""
        try:
            # Try Android POS printing methods
            # Method 1: Direct POS printer command
            if self.try_android_raw_print(text):
                return
            
            # Method 2: Android Bluetooth printing
            if self.try_android_bluetooth_print(text):
                return
            
            # Method 3: Android USB printing
            if self.try_android_usb_print(text):
                return
            
            raise Exception("Android POS printer not found")
            
        except Exception as e:
            raise Exception(f"Android POS error: {str(e)}")
    
    def try_android_raw_print(self, text):
        """Try raw print command on Android POS"""
        try:
            # Common Android POS printer paths
            pos_paths = [
                "/dev/usb/lp0",
                "/dev/usb/lp1", 
                "/dev/ttyUSB0",
                "/dev/ttyS0",
                "/sys/class/thermal_printer/thermal_printer0/device"
            ]
            
            for path in pos_paths:
                try:
                    with open(path, 'w', encoding='utf-8') as f:
                        # Add printer initialization commands
                        init_cmd = b'\x1B\x40'  # Initialize printer
                        f.write(init_cmd.decode('latin-1'))
                        f.write(text)
                        # Cut paper command
                        cut_cmd = b'\x1B\x64\x02'  # Cut paper
                        f.write(cut_cmd.decode('latin-1'))
                        return True
                except:
                    continue
            return False
        except:
            return False
    
    def try_android_bluetooth_print(self, text):
        """Try Bluetooth printing on Android"""
        try:
            # Use PyBluez for Android if available
            import bluetooth
            nearby_devices = bluetooth.discover_devices()
            
            for addr in nearby_devices:
                try:
                    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
                    sock.connect((addr, 1))
                    sock.send(text.encode('utf-8'))
                    sock.close()
                    return True
                except:
                    continue
            return False
        except:
            return False
    
    def try_android_usb_print(self, text):
        """Try USB printing on Android"""
        try:
            # Use android-usb-printer if available
            from usbprinter import UsbPrinter
            printer = UsbPrinter()
            printer.print_text(text)
            return True
        except:
            return False
    
    def windows_pos_print(self, text):
        """Print on Windows POS devices"""
        try:
            # Method 1: Windows POS printer (POS for .NET)
            if self.try_windows_pos_dotnet(text):
                return True
            
            # Method 2: Raw Windows printer
            if self.try_windows_raw_print(text):
                return True
            
            # Method 3: Windows default printer
            if self.try_windows_default_print(text):
                return True
            
            return False
        except:
            return False
    
    def try_windows_pos_dotnet(self, text):
        """Try Windows POS for .NET printer"""
        try:
            import clr
            # Add POS for .NET reference if available
            clr.AddReference("Microsoft.PointOfService")
            from Microsoft.PointOfService import PosExplorer
            
            explorer = PosExplorer()
            devices = explorer.GetDevices("PosPrinter")
            
            for device in devices:
                try:
                    printer = explorer.CreateInstance(device)
                    printer.Open()
                    printer.Claim(1000)
                    printer.DeviceEnabled = True
                    
                    # Print receipt
                    printer.PrintNormal(PrinterStation.Receipt, text)
                    printer.CutPaper(100)
                    
                    printer.Release()
                    printer.Close()
                    return True
                except:
                    continue
            return False
        except:
            return False
    
    def try_windows_raw_print(self, text):
        """Try raw Windows printing"""
        try:
            import win32print
            import win32api
            
            # Get available printers
            printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL)
            
            for printer in printers:
                try:
                    printer_name = printer[2]  # Printer name
                    
                    # Check if it's a thermal printer
                    if any(keyword in printer_name.lower() 
                          for keyword in ['thermal', 'pos', 'receipt', 'ticket']):
                        
                        hPrinter = win32print.OpenPrinter(printer_name)
                        try:
                            # Raw print
                            pDoc = {"pDataType": "RAW"}
                            win32print.StartDocPrinter(hPrinter, 1, pDoc)
                            win32print.WritePrinter(hPrinter, text.encode('utf-8'))
                            win32print.EndDocPrinter(hPrinter)
                            return True
                        finally:
                            win32print.ClosePrinter(hPrinter)
                except:
                    continue
            return False
        except:
            return False
    
    def try_windows_default_print(self, text):
        """Try Windows default printer"""
        try:
            import win32print
            import win32api
            
            # Get default printer
            printer_name = win32print.GetDefaultPrinter()
            hPrinter = win32print.OpenPrinter(printer_name)
            
            try:
                pDoc = {"pDataType": "RAW"}
                win32print.StartDocPrinter(hPrinter, 1, pDoc)
                
                # Add ESC/POS commands for thermal printer
                esc_commands = b'\x1B\x40'  # Initialize
                win32print.WritePrinter(hPrinter, esc_commands)
                win32print.WritePrinter(hPrinter, text.encode('utf-8'))
                
                # Cut paper
                cut_command = b'\x1B\x64\x02'
                win32print.WritePrinter(hPrinter, cut_command)
                
                win32print.EndDocPrinter(hPrinter)
                return True
            finally:
                win32print.ClosePrinter(hPrinter)
        except:
            return False
    
    def windows_usb_print(self, text):
        """Original USB thermal printer method"""
        try:
            from escpos.printer import Usb
            
            # Common thermal printer vendor/product IDs:
            printers_to_try = [
                (0x04b8, 0x0202),  # Epson TM-T88
                (0x04b8, 0x0e15),  # Epson TM-T20
                (0x0519, 0x0001),  # Star TSP650
                (0x1cb1, 0x0001),  # Generic Chinese
                (0x154b, 0x0001),  # Generic POS
                (0x0fe6, 0x0011),  # POS printer
            ]
            
            for vendor_id, product_id in printers_to_try:
                try:
                    printer = Usb(vendor_id, product_id)
                    printer.text(text)
                    printer.cut()
                    return True
                except:
                    continue
            
            raise Exception("No USB printer found")
            
        except ImportError:
            raise Exception("python-escpos not installed")
        except Exception as e:
            raise Exception(f"USB printer error: {str(e)}")
    
    def save_receipt_to_file(self, text):
        """Save receipt to text file as fallback"""
        with open("receipt.txt", "w", encoding="utf-8") as f:
            f.write(text)

def main():
    root = tk.Tk()
    app = CafeBillingSystem(root)
    root.mainloop()

if __name__ == "__main__":
    main()
