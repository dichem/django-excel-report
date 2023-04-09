from setuptools import find_packages, setup

__version__ = "0.0.1"

setup(
    name="django_excel_report",
    version=__version__,
    author="Boris Alekseev",
    author_email="i.borisalekseev@gmail.com",
    packages=find_packages('src', exclude=["tests*"]),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.7",
    install_requires=[
        "Django>=3.2",
    ],
)
