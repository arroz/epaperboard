from distutils.core import setup

setup(
    name="epaperboard",
    packages=['epaperboard', 'epaperboard.src', 'epaperboard.fonts', 'epaperboard.images'],
    version="1.0.0",
    url="https://github.com/arroz/epaperboard",
    description="Dashboard for Raspberry Pi with e-paper display.",
    install_requires=[
        "pillow",
        "bottle"
    ],
    extras_require={
        "epd": ["IT8951"]
    },
    entry_points={
        'console_scripts': [
            'epaperboard = epaperboard.main:run'
        ],
    },
    include_package_data=True
)