#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Runs ASGI server """

import uvicorn

from app import create_app

app = create_app()

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=5000)
