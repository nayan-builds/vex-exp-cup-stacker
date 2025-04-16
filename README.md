# VEX EXP Cup Stacker

<p align="center">
  <img src="https://github.com/nayan-builds/vex-exp-cup-stacker/blob/main/robot.jpg?raw=true" alt="Cup Stacker Robot" width="300"/>
</p>

## What it does

The robot takes 6 cups and build a stack with 3 layers (3 on the bottom, 2 middle, 1 on top).

## Features of the Robot

- 4 omni-directional wheels for straight movements in orthogonal directions.
- Arm with claw attached.
- Distance sensor on the claw.
- Distance sensor on the base.
- Elastic band for extra tension force to help lift the arm.
- Brain positioned at the back to help balance out the weight of the arm.

## Setup Instructions

### Code Setup
The code is entirely run on the VEX EXP brain and **should already be downloaded**. To run this, you should navigate to `Programs` on the VEX EXP brain and select `Cup Stacker` then simply select `Run`.
If the code is not already downloaded to the brain, go to [VEXCode EXP](https://codeexp.vex.com/) and open `Cup Stacker.exppython` found in this repository. Connect the robot to your computer with the USB cable, then select `BRAIN` at the top right of the page and click connect, following the prompts provided. Once connected to the brain, click `DOWNLOAD` in the top right to download the code to the brain.

### Physical Setup
The cups should be setup to the right of the robot, and forwards enough such that the robot moving to the right should not hit any of them (the robot does reverse a little bit at the start though to avoid any cups slightly too close). The cups should not be too close together so that multiple cups do not get caught in the claw at the same time. The cups can be placed in columns of two but any more usually leads to collisions. If the cups are more than ~30cm from the claw sensor, they will not be detected without increasing the value of `MAX_VISION_RANGE` in the code.

<p align="center">
  <img src="https://github.com/nayan-builds/vex-exp-cup-stacker/blob/main/example-setup.jpg?raw=true" alt="Example Cup Setup" width="300"
</p>
