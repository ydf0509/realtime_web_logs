# coding=utf-8
from pathlib import Path
from setuptools import setup, find_packages

# with open("README.md", "r",encoding='utf8') as fh:
#     long_description = fh.read()

# filepath = ((Path(__file__).parent / Path('README.md')).absolute()).as_posix()
filepath = 'README.md'
print(filepath)

setup(
    name='realtime_web_logs',  #
    version="1.5",
    description=(
        'flask files manage,realtime flush logs'),
    keywords=("realtime_web_logs", 'flask',),
    # long_description=open('README.md', 'r',encoding='utf8').read(),
    long_description_content_type="text/markdown",
    long_description=open(filepath, 'r', encoding='utf8').read(),
    # data_files=[filepath],
    author='bfzs',
    author_email='xxxxx@sohu.com',
    maintainer='ydf',
    maintainer_email='xxx@sohu.com',
    license='BSD License',
    # packages=find_packages(),
    packages=['realtime_web_logs',],
    include_package_data=True,
    platforms=["all"],
    url='',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[
        'function_scheduling_distributed_framework',
        'flask_httpauth',
        'flask_bootstrap',
    ],
    entry_points={
        'console_scripts': ['rwl=realtime_web_logs.log_to_web:main']
    }
)

print('恭喜安装完成啦。')
"""
打包上传
python setup.py sdist upload -r pypi


python setup.py sdist & twine upload dist/realtime_web_logs-1.5.tar.gz
twine upload dist/*


python -m pip install realtime_web_logs --upgrade -i https://pypi.org/simple   # 及时的方式，不用等待 阿里云 豆瓣 同步
"""
