#!/bin/bash
python -m hypercorn -c hypercorn_config.toml app:create_app() 