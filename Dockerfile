FROM ros:humble

RUN apt update
RUN apt install ros-humble-cartographer -y
