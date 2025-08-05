#!/usr/bin/env python3
"""
Test runner script for SwellSeeker backend
"""
import subprocess
import sys
import os

def run_tests():
    """Run all tests with pytest"""
    print("🏄‍♂️ Running SwellSeeker Backend Tests...")
    print("=" * 50)
    
    # Run tests with coverage
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/",
        "-v",
        "--tb=short",
        "--disable-warnings"
    ]
    
    try:
        result = subprocess.run(cmd, cwd=os.path.dirname(__file__))
        return result.returncode
    except KeyboardInterrupt:
        print("\n❌ Tests interrupted by user")
        return 1

if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code) 