#!/usr/bin/env python3
"""
Debug script to test the executable and capture any errors
"""

import subprocess
import sys
import os
import time

def debug_executable():
    """Debug the executable by capturing its output"""
    print("Debugging PhotoWatermark executable...")
    
    # Get the executable path
    exe_path = os.path.join("dist", "PhotoWatermark_v1.1.0_20251001.exe")
    
    if not os.path.exists(exe_path):
        print(f"ERROR: Executable not found at {exe_path}")
        return False
    
    print(f"✓ Executable found: {exe_path}")
    print(f"  Size: {os.path.getsize(exe_path) / (1024*1024):.1f} MB")
    
    # Test the executable with captured output
    print("\nRunning executable with output capture...")
    try:
        # Start the executable and capture output
        process = subprocess.Popen(
            [exe_path], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        
        # Wait for a few seconds to see if it crashes
        time.sleep(5)
        
        # Check if process is still running
        if process.poll() is None:
            print("✓ Executable started successfully and is running")
            # Give it a bit more time
            time.sleep(2)
            # Terminate the process
            process.terminate()
            try:
                stdout, stderr = process.communicate(timeout=5)
                if stdout:
                    print(f"STDOUT:\n{stdout}")
                if stderr:
                    print(f"STDERR:\n{stderr}")
            except subprocess.TimeoutExpired:
                process.kill()
                stdout, stderr = process.communicate()
                if stdout:
                    print(f"STDOUT:\n{stdout}")
                if stderr:
                    print(f"STDERR:\n{stderr}")
        else:
            # Process has terminated, check exit code
            stdout, stderr = process.communicate()
            print(f"Process terminated with exit code: {process.returncode}")
            if stdout:
                print(f"STDOUT:\n{stdout}")
            if stderr:
                print(f"STDERR:\n{stderr}")
                
    except Exception as e:
        print(f"✗ Failed to start executable: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    debug_executable()