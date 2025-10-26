#!/usr/bin/env python3
"""
Google Cloud App Engine Entry Point
"""

import os
from schedule_creator_app import app

if __name__ == '__main__':
    # For Google Cloud App Engine
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
