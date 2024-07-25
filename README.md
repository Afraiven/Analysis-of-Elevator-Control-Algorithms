# Analysis of Elevator Control Algorithms

This repository contains various algorithms and a simulation environment implemented in Python using the pygame library, designed to analyze and optimize elevator control systems. The goal of this project is to minimize the average passenger service times in various real-world scenarios. These files can be easily modified, for instance by changing timestep, the animations can be changed freely also metrics.py allows to change the way results are shown.

## Table of Contents
- [Introduction](#introduction)
- [Algorithms](#algorithms)
  - [AZE (Extreme Agreement Algorithm)](#aze-extreme-agreement-algorithm)
  - [ANC (Nearest Target Algorithm)](#anc-nearest-target-algorithm)
  - [APKZ (Request Order Priority Algorithm)](#apkz-request-order-priority-algorithm)
- [Simulation Environments](#simulation-environments)
  - [Random Environment with High Intensity](#random-environment-with-high-intensity)
  - [Residential Building Scenario](#residential-building-scenario)
- [Performance Analysis](#performance-analysis)
- [Installation](#installation)
- [Usage](#usage)
- [Contribution](#contribution)
- [License](#license)
- [Authors and Acknowledgments](#authors-and-acknowledgments)

## Introduction
This project aims to present and compare different approaches to elevator control algorithms, evaluating their advantages and identifying potential improvements. The study focuses on minimizing the time required to complete elevator requests, ignoring energy consumption costs. The project includes several algorithms, implemented and verified based on observations.

## Algorithms
### AZE (Extreme Agreement Algorithm)
- The elevator moves in a specified direction, picking up passengers whose destination aligns with the current direction of travel until all requests are serviced, then changes direction.

### ANC (Nearest Target Algorithm)
- This algorithm prioritizes the nearest target relative to the elevator's position, adjusting the direction based on the closest target within the elevator and the nearest request, if sensible.

### APKZ (Request Order Priority Algorithm)
- The elevator operates based on the chronological order of requests, ignoring extremes. The direction is set based on the earliest passenger inside the elevator, then the earliest requests.

## Simulation Environments
### Random Environment with High Intensity
- Passengers are generated randomly with random destinations. The elevator has an unlimited capacity, and the environment is simulated to handle 100,000 passengers.

### Residential Building Scenario
- The elevator has a maximum capacity of 6 passengers, and the movement simulates real-world patterns in a residential building with varying passenger counts per request.

## Performance Analysis
- The performance of each algorithm is analyzed in different environments, highlighting their efficiency and areas for potential optimization. The AZE algorithm generally shows better performance, especially when enhanced with strategic stop points.

## Installation
To run the simulations, you need to have Python installed along with the required libraries. Use the following commands to install the dependencies:

```bash
pip install -r requirements.txt
