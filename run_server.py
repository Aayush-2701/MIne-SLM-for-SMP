"""
Server runner script for Mine SLM Platform.
Launches the Streamlit Web Application on port 8501.
"""
import sys
import subprocess
from pathlib import Path

def main():
    root_dir = Path(__file__).resolve().parent
    app_path = root_dir / "app.py"
    
    print("=" * 70)
    print("  ⛏️  MINE SLM FOR SAFETY MANAGEMENT PLAN")
    print("  AI-Based Platform Built on Hybrid RAG for Grounded, Multilingual")
    print("  Mine-Safety Information Access for Indian Mines")
    print("  Department of Mining Engineering, NITK Surathkal")
    print("=" * 70)
    print(f"\nStarting Streamlit interface at http://localhost:8501 ...\n")
    
    cmd = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(app_path),
        "--server.port=8501",
        "--server.headless=true"
    ]
    subprocess.run(cmd)

if __name__ == "__main__":
    main()
