import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='weibo-sdk',
    version='0.3.0',
    description='新浪微博sdk',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/dataabc/weiboSpider',
    packages=setuptools.find_packages(),
    package_data={'weibo_sdk': ['config_sample.json', 'logging.conf']},
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
