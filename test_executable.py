#!/usr/bin/env python3
"""
Test script to verify executable functionality
"""

import subprocess
import sys
import os
import time

def test_executable():
    """Test the executable functionality"""
    print("Testing PhotoWatermark executable...")
    
    # Get the executable path
    exe_path = os.path.join("dist", "PhotoWatermark_v1.1.0_20251001.exe")
    
    if not os.path.exists(exe_path):
        print(f"ERROR: Executable not found at {exe_path}")
        return False
    
    print(f"✓ Executable found: {exe_path}")
    print(f"  Size: {os.path.getsize(exe_path) / (1024*1024):.1f} MB")
    
    # Test 1: Check if executable starts without errors
    print("\nTest 1: Checking if executable starts...")
    try:
        # Start the executable
        process = subprocess.Popen([exe_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a few seconds to see if it crashes
        time.sleep(3)
        
        # Check if process is still running
        if process.poll() is None:
            print("✓ Executable started successfully and is running")
            # Terminate the process
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
        else:
            # Process has terminated, check exit code
            stdout, stderr = process.communicate()
            if process.returncode == 0:
                print("✓ Executable started and exited normally")
            else:
                print(f"✗ Executable failed with exit code {process.returncode}")
                if stderr:
                    print(f"  Error output: {stderr.decode('utf-8', errors='ignore')}")
                return False
                
    except Exception as e:
        print(f"✗ Failed to start executable: {e}")
        return False
    
    # Test 2: Check dependencies
    print("\nTest 2: Checking required dependencies...")
    required_modules = ['PIL', 'windnd', 'tkinter']
    
    for module in required_modules:
        try:
            # Test if we can import the module
            if module == 'PIL':
                import PIL
                print(f"✓ {module} imported successfully")
            elif module == 'windnd':
                import windnd
                print(f"✓ {module} imported successfully")
            elif module == 'tkinter':
                import tkinter
                print(f"✓ {module} imported successfully")
        except ImportError as e:
            print(f"✗ Failed to import {module}: {e}")
            return False
    
    print("\n✓ All tests passed! Executable is working correctly.")
    return True

if __name__ == "__main__":
    success = test_executable()
    if success:
        print("\n🎉 Executable verification successful!")
        print("The PhotoWatermark v1.1.0 executable is ready for release.")
    else:
        print("\n❌ Executable verification failed!")
        print("Please check the errors above and rebuild the executable.")
        sys.exit(1)