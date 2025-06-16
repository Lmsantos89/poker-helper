import multiprocessing

# Gunicorn configuration for Render deployment
bind = "0.0.0.0:10000"  # Render will override this with PORT env variable
workers = multiprocessing.cpu_count() * 2 + 1
threads = 2
timeout = 60
worker_class = "sync"
loglevel = "info"
