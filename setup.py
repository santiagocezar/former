import setuptools

setuptools.setup(
    name="former-svcezar", # Replace with your own username
    version="0.0.1",
    author="Santiago Cézar",
    author_email="santiagocezar2013@gmail.com",
    description="Easy markdown forms",
    long_description="# Former",
    long_description_content_type="text/markdown",
    url="https://encuestas.svcezar.com.ar",
    packages=setuptools.find_packages(),
    classifiers=[],
    include_package_data=True,
    install_requires=[
        'Flask==1.1.1',
        'mistune==2.0.0a4',
        'watchdog==0.10.3',
        'waitress==1.4.4',
        'flask_sqlalchemy==2.4.1'
    ],
    python_requires='>=3.6',
)