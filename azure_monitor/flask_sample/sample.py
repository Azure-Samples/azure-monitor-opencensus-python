# ensure that the parent/top level package is part of the path
import sys
from pathlib import Path

file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))

# initialize the flask app
from flask_sample.app.app import app

if __name__ == "__main__":
    app.run(debug=True)
