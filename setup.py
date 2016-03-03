from setuptools import setup


setup(
    name="avocado-templated-mail",
    version='0.0.1',
    description='Email templates in your db and easy sending',
    keywords="django, email, templates",
    author="Albert O'Connor <info@albertoconnor.ca>",
    author_email="info@albertoconnor.ca",
    url="https://github.com/AvocadoCoop/avocado-templated-mail",
    license="BSD License",
    packages=["templated_mail"],
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: BSD License",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Django",
        "Environment :: Web Environment",
    ],
)
