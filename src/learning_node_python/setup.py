from setuptools import setup

package_name = 'learning_node_python'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='lucas',
    maintainer_email='lucas@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        'node_helloworld = learning_node_python.node_helloworld:main',
        'node_helloworld_class = learning_node_python.node_helloworld_class:main',
        'node_object = learning_node_python.node_object:main',
        'node_object_webcam = learning_node_python.node_object_webcam:main'
        ],
    },
)
