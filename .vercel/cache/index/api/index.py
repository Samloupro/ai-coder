from flask import Flask, request, jsonify
import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

# Vercel requires the app to be named 'app'
app = app