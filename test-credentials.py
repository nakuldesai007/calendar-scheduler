#!/usr/bin/env python3
"""Test script to verify credentials work"""
import os
import base64
import pickle
import io

def test_credentials():
    # Check environment variables
    creds_json_env = os.environ.get('GOOGLE_CREDENTIALS')
    token_env = os.environ.get('GOOGLE_TOKEN')
    
    print(f"GOOGLE_CREDENTIALS set: {creds_json_env is not None}")
    print(f"GOOGLE_TOKEN set: {token_env is not None}")
    
    if token_env:
        try:
            token_data = base64.b64decode(token_env)
            token_file = io.BytesIO(token_data)
            creds = pickle.load(token_file)
            print(f"✅ Token loaded successfully!")
            print(f"Token valid: {creds.valid}")
            print(f"Token expired: {creds.expired if creds else None}")
            if creds:
                print(f"Refresh token exists: {hasattr(creds, 'refresh_token') and creds.refresh_token is not None}")
        except Exception as e:
            print(f"❌ Error loading token: {e}")
    else:
        print("No GOOGLE_TOKEN environment variable found")

if __name__ == "__main__":
    test_credentials()

