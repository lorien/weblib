from setuptools import setup, find_packages

setup(
    name="weblib",
    version="0.1.30",
    description="Set of tools for web scraping projects",
    long_description=open("README.md", encoding="utf-8").read(),
    author="Gregory Petukhov",
    author_email="lorien@lorien.name",
    url="https://github.com/lorien/weblib",
    long_description_content_type="text/markdown",
    install_requires=[
        "pytils",
        "six",
        "user_agent",
    ],
    extras_require={
        "full": [
            "feedparser",
            "selenium",
            "lxml",
        ],
    },
    keywords="web html encoding text",
    packages=find_packages(exclude=["tests"]),
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
