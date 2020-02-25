import sys
from flask import Flask

sys.path.append('..')
endpoint_app = Flask(__name__)

# Import here to avoid circular imports
from endpoint import endpoint_routes  # noqa isort:skip


if __name__ == '__main__':
    endpoint_app.run(host='localhost', port=5001, threaded=True, debug=True)
