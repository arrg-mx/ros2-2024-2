from setuptools import find_packages, setup

package_name = 'mypkg_py'

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
    maintainer='arrusr',
    maintainer_email='rivascf@gmail.com',
    description='Paquete de prueba ROS2',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'test_nodo = mypkg_py.nodo_demo:main'
        ],
    },
)
