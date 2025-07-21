from setuptools import setup, find_packages

setup(
    name='qgp',
    version='0.1.0',
    description='QGP (Quantum Good Privacy): Hybrid Post-Quantum & ECC Secure Messaging',
    author='Your Name',
    author_email='you@example.com',
    url='https://github.com/yourusername/qgp',
    packages=find_packages(),
    install_requires=[
        'pynacl>=1.5.0',
        'kyber-py>=1.0.1',
        'zstd>=1.4.9',
        'ipfshttpclient>=0.7.0,<0.9.0',
    ],
    entry_points={
        'console_scripts': [
            'qgp = qgp.cli:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
