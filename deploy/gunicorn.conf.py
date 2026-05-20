bind = 'unix:/run/ecommerceee/gunicorn.sock'
workers = 3
worker_class = 'sync'
timeout = 60
accesslog = '-'
errorlog = '-'
