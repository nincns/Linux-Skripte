#!/bin/bash

# Set the locale
sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

# Enable the Ubuntu Universe Repository
sudo apt install software-properties-common
sudo add-apt-repository universe

# Add the ROS 2 GPG key
sudo apt update && sudo apt install curl -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

# Add the repository to your sources list
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

# Update your apt repository caches after setting up the repositories
sudo apt update

# Ensure your system is up to date
sudo apt upgrade

# Install ROS 2 Humble (Desktop version)
sudo apt install ros-humble-desktop

# Set up your environment by sourcing the following file
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc

# Check the installation
ros2 --version
