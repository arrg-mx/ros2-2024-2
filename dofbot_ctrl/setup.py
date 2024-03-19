from setuptools import find_packages, setup
from glob import glob

package_name = 'dofbot_ctrl'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='rivascf',
    maintainer_email='rivascf@gmail.com',
    description='Dofbot Ctrl ROS2 package',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'dofbot_node = dofbot_ctrl.dofbot_node:main'
        ],
    },
)
