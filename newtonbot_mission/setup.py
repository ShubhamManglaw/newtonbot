from setuptools import find_packages, setup

package_name = 'newtonbot_mission'

setup(
    name=package_name,
    version='1.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        (
            'share/ament_index/resource_index/packages',
            ['resource/' + package_name],
        ),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/mission.launch.py']),
        ('share/' + package_name + '/config', ['config/mission_params.yaml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Shubham Manglaw',
    maintainer_email='Shubhammanglaw@gmail.com',
    description='Mission management package for NewtonBot.',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'mission_manager = newtonbot_mission.mission_manager:main',
        ],
    },
)
