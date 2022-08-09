import setuptools

setuptools.setup(
    name='weibo-sdk',
    version='0.1.0',
    description='新浪微博sdk',
    url='https://github.com/valueflowever/weibo-sdk',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'absl-py',
        'lxml',
        'requests',
        'tqdm',
    ],
    python_requires='>=3.6',
)
