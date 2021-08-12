# Installation
Once the repository has been downloaded, you might want to create a Python virtual environment in order to encapsulate the required libraries installation. In order to do that, type the following commands in the commandline:

Unix-based
```
python3 -m venv .venv
```

Activate the newly created virtual environment:
```
source .venv/bin/activate
```

Update pip’s version to ensure latest libraries versions:
```
pip install -U pip
```

One of the required libraries, `dlib`, requires CMake to be installed. After installing CMake, the following command will install the required libraries
```
pip install -r requirements
```

Now you should be able to run the `imageshuffle` script file.

## (Optional) Add to path

In Unix-based system, you can add the program to PATH using the following command:
```bash
export PATH="<path_to_repo_directory>:$PATH"
```

As long as the virtual environment is activated, you should now be able to run the program from any directory inside the commandline.
