from setuptools import find_packages, setup

__version__ = "0.0.2"


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name="django_excel_report",
    version=__version__,
    author="Boris Alekseev",
    author_email="i.borisalekseev@gmail.com",
    maintainer="",
    maintainer_email="",
    description="Simplify excel reports from django apps",
    long_description=readme(),
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.7",
    install_requires=[
        "XlsxWriter~=3.0.0"
    ],
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    project_urls={
        'Source': 'https://github.com/dichem/django-excel-report'
    },
    keywords='django excel',
)
