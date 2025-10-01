"""
Setup script for Invisibility Cloak Project
Checks dependencies and provides installation guidance
"""

import subprocess
import sys
import importlib.util

def check_python_version():
    """Check if Python version is compatible"""
    print("Checking Python version...")
    version = sys.version_info
    
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print(f"❌ Python {version.major}.{version.minor} detected")
        print("❌ This project requires Python 3.7 or higher")
        return False
    else:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
        return True

def check_package(package_name, import_name=None):
    """Check if a package is installed"""
    if import_name is None:
        import_name = package_name
    
    try:
        spec = importlib.util.find_spec(import_name)
        if spec is not None:
            print(f"✅ {package_name} is installed")
            return True
        else:
            print(f"❌ {package_name} is not installed")
            return False
    except ImportError:
        print(f"❌ {package_name} is not installed")
        return False

def install_package(package_name):
    """Install a package using pip"""
    print(f"Installing {package_name}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        print(f"✅ {package_name} installed successfully")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Failed to install {package_name}")
        return False

def check_camera():
    """Check if camera is accessible"""
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            ret, frame = cap.read()
            cap.release()
            if ret:
                print("✅ Camera is accessible")
                return True
            else:
                print("❌ Camera found but cannot capture frames")
                return False
        else:
            print("❌ Cannot access camera")
            return False
    except Exception as e:
        print(f"❌ Camera check failed: {e}")
        return False

def main():
    """Main setup function"""
    print("=== Invisibility Cloak Setup ===")
    print()
    
    # Check Python version
    if not check_python_version():
        print("\nPlease upgrade your Python installation and try again.")
        return False
    
    print("\nChecking dependencies...")
    
    # Required packages
    packages = [
        ("opencv-python", "cv2"),
        ("numpy", "numpy")
    ]
    
    missing_packages = []
    
    for package_name, import_name in packages:
        if not check_package(package_name, import_name):
            missing_packages.append(package_name)
    
    # Install missing packages
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        response = input("Would you like to install them now? (y/n): ").lower().strip()
        
        if response == 'y' or response == 'yes':
            print("\nInstalling missing packages...")
            for package in missing_packages:
                if not install_package(package):
                    print(f"\nFailed to install {package}. Please install manually:")
                    print(f"pip install {package}")
                    return False
        else:
            print("\nPlease install the missing packages manually:")
            for package in missing_packages:
                print(f"pip install {package}")
            return False
    
    print("\n" + "="*50)
    print("Checking camera access...")
    
    if check_camera():
        print("\n🎉 Setup completed successfully!")
        print("\nYou can now run the invisibility cloak:")
        print("  Basic version: python invisibility_cloak.py")
        print("  Advanced version: python advanced_invisibility_cloak.py")
        print("\nTips for best results:")
        print("  - Use bright, solid red colored fabric")
        print("  - Ensure good lighting conditions")
        print("  - Keep the background stationary")
        return True
    else:
        print("\n⚠️  Setup completed but camera access failed")
        print("Please check:")
        print("  - Camera is connected and working")
        print("  - No other applications are using the camera")
        print("  - Camera drivers are up to date")
        return False

if __name__ == "__main__":
    success = main()
    
    if not success:
        print("\n❌ Setup encountered issues. Please resolve them and try again.")
        sys.exit(1)
    else:
        print("\n✅ Setup completed successfully!")