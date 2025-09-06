#!/usr/bin/env python
"""
Build and serve documentation with automatic API reference generation.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def check_dependencies():
    """Check if required packages are installed."""
    try:
        import mkdocs
        import mkdocstrings
        print("✓ Documentation dependencies installed")
    except ImportError:
        print("✗ Missing dependencies. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "docs/requirements.txt"])
        print("✓ Dependencies installed")


def build_docs(clean=False):
    """Build the documentation."""
    print("\n📚 Building documentation...")
    
    if clean:
        print("  Cleaning previous build...")
        subprocess.run(["mkdocs", "build", "--clean"])
    else:
        subprocess.run(["mkdocs", "build"])
    
    print("✓ Documentation built successfully")
    print("  Output directory: ./site/")


def serve_docs(port=8000):
    """Serve documentation locally."""
    print(f"\n🌐 Serving documentation on http://127.0.0.1:{port}")
    print("  Press Ctrl+C to stop")
    
    try:
        subprocess.run(["mkdocs", "serve", "--dev-addr", f"127.0.0.1:{port}"])
    except KeyboardInterrupt:
        print("\n✓ Server stopped")


def deploy_docs():
    """Deploy documentation to GitHub Pages."""
    print("\n🚀 Deploying to GitHub Pages...")
    subprocess.run(["mkdocs", "gh-deploy"])
    print("✓ Documentation deployed")


def main():
    parser = argparse.ArgumentParser(description="Documentation builder for SIA-CE")
    parser.add_argument(
        "command",
        choices=["build", "serve", "deploy", "check"],
        help="Command to execute"
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Clean build directory before building"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port for serving documentation (default: 8000)"
    )
    
    args = parser.parse_args()
    
    # Change to project root
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # Check dependencies
    check_dependencies()
    
    # Execute command
    if args.command == "check":
        print("✓ Ready to build documentation")
    elif args.command == "build":
        build_docs(clean=args.clean)
    elif args.command == "serve":
        serve_docs(port=args.port)
    elif args.command == "deploy":
        deploy_docs()


if __name__ == "__main__":
    main()