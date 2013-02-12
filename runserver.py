# -*- coding: utf-8 -*-
"""

    Script to run the application

    :copyright: (c) 2012 by Concert Talent
    :license: see LICENSE for more details.

"""

from concert1 import app

extra_dirs = ['concert1/templates',]
extra_files = extra_dirs[:]
for extra_dir in extra_dirs:
    for dirname, dirs, files in os.walk(extra_dir):
        for filename in files:
            filename = path.join(dirname, filename)
            if path.isfile(filename):
                extra_files.append(filename)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80, extra_files=extra_files)
