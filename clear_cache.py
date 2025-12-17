#!/usr/bin/env python3
"""Clear Python cache files"""
import os
import shutil
import glob

def clear_cache():
    """Remove all .pyc files and __pycache__ directories"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Remove .pyc files
    for pyc_file in glob.glob(os.path.join(current_dir, "**", "*.pyc"), recursive=True):
        try:
            os.remove(pyc_file)
            print(f"Removed: {pyc_file}")
        except Exception as e:
            print(f"Error removing {pyc_file}: {e}")
    
    # Remove __pycache__ directories
    for root, dirs, files in os.walk(current_dir):
        if '__pycache__' in dirs:
            cache_dir = os.path.join(root, '__pycache__')
            try:
                shutil.rmtree(cache_dir)
                print(f"Removed: {cache_dir}")
            except Exception as e:
                print(f"Error removing {cache_dir}: {e}")
    
    print("Cache cleared!")

if __name__ == "__main__":
    clear_cache()
