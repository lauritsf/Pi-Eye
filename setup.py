from setuptools import setup, find_packages

setup(
    name="pieye",
    python_requires=">=3.9",
    version="0.0.1",
    description="Pi Eye Camera Service",
    author="Laurits Fredsgaard Larsen, Roberta Eleanor Hunt",
    license="MIT",
    author_email="",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "": [
            "fake_camera_files/full.dng",
            "fake_camera_files/preview.jpg",
            "fake_camera_files/image.jpg",
            "fake_camera_files",
        ]
    },
    install_requires=[
        "bottle",
        "numpy",
        "Pillow",
    ],
    entry_points={
        "console_scripts": [
            "pieye = pieye.__main__:run_server",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha"
        "Intended Audience :: Developers"
        "Natural Language :: English"
        "License :: OSI Approved :: MIT License",
        'Operating System :: POSIX :: Linux'
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Topic :: Multimedia :: Graphics :: Capture :: Digital Camera"

    ]
)
