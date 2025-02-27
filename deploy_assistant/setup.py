from setuptools import setup, find_packages

setup(
    name='aiodeploy',
    packages=find_packages(exclude=('demo')),
    version='1.0.0',
    install_requires=[  # 添加了依赖的 package
        'requests', 
        'flask',
        'yaml',
    ],
    extras_require={ # 添加了可选安装的依赖 package，使用: pip install -e .[interactive]
        # 'interactive': ['matplotlib>=2.2.0,<3.0.0', 'jupyter']
    },
    entry_points={  # 设置了在命令行中如何使用 greeting_module  中的 main 函数
        # 'console_scripts': [
        #     'greeting=greeting_pkg.greeting_module:main'
        # ]
    },
    py_modules=[     # 在 package 之外添加两个独立的 module
        # 'isolated_greeting_module_1',
        # 'isolated_greeting_module_2'
    ],
    author="Peter",
    author_email="wangyuqiang@aikosolar.com",
    description="This is an deploy assistant Package for AI2",
    keywords="deploy assistant AI2",
    url="http://172.16.97.177:3000/YQ_Wang/deploy_assistant",   # project home page, if any
    project_urls={
        "Documentation": "http://172.16.97.177:3000/YQ_Wang/deploy_assistant",
        "Source Code": "http://172.16.97.177:3000/YQ_Wang/deploy_assistant",
    },
    classifiers=[
        'License :: OSI Approved :: Python Software Foundation License',
        'Programming Language :: Python :: 3.8',
    ]
)