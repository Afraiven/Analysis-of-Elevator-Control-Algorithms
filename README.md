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
- [Testing Methodology](#testing-methodology)
- [Conclusions](#conclusions)

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
```

## Testing Methodology
To evaluate the effectiveness of the elevator control algorithms, an empirical distribution of total travel times was compared to a normal distribution. The key metrics collected included average travel time, waiting time, and variance. The performance of the algorithms was assessed based on the following criteria:

1. **Empirical Distribution Analysis**:
   - The travel times were collected over a large number of iterations (e.g., 100,000 passengers) to create an empirical distribution.
   - This distribution was then compared to a normal distribution to check for alignment. A close alignment indicates predictable and efficient performance.

2. **Variance and Outliers**:
   - Variance in travel times was used to measure consistency. Lower variance indicates more predictable and reliable performance.
   - The presence of outliers (extremely high travel times) was also monitored. Algorithms with fewer outliers were considered more efficient.

3. **Average Metrics**:
   - **Average Travel Time**: The mean time passengers spent traveling in the elevator.
   - **Average Waiting Time**: The mean time passengers waited for the elevator to arrive.
   - **Average Total Time**: The sum of average travel and waiting times.

These metrics provided a comprehensive view of each algorithm's performance, allowing for a detailed comparison of their efficiency and effectiveness in different simulation environments.

## Conclusions

This study aimed to present and compare various elevator control algorithms, focusing on optimizing average passenger service times in different scenarios. Key findings are summarized below:

1. **Algorithm Performance**:
   - **Consistent Extremes Algorithm (AZE)**: Performed best in both random and residential building environments. It showed minimal variance in travel times and aligned closely with normal distribution, indicating efficient and predictable performance.
   - **Nearest Target Algorithm (ANC)**: Demonstrated larger variance and longer tail in travel times, making it less optimal in high-intensity random environments. However, it showed potential with optimizations.
   - **Order of Requests Priority Algorithm (APKZ)**: Performed poorly in random environments, with high variance and extreme travel times, indicating inefficiency.

2. **Simulation Environments**:
   - **Random Environment**: AZE showed better overall performance with lower average travel and waiting times compared to ANC.
   - **Residential Building Environment**: Introducing a parking floor improved AZE performance by 5.51% and ANC by 3.735%. AZE remained superior due to its stability and lower variance.

3. **Machine Learning Potential**:
   - Preliminary experiments with **Deep Q-Network (DQN)** showed promise but required more training and tuning. AZE outperformed DQN in a simplified 4-floor environment.

4. **Optimization Strategies**:
   - Adding parking floors for elevators in buildings with predictable travel patterns significantly improved efficiency.
   - Incorporating passenger count in request prioritization could enhance ANC performance.
   - Utilizing machine learning algorithms like AI to determine optimal service sequences and dynamic parking floors could further optimize elevator operations.

5. **Energy Efficiency**:
   - While the study focused on travel time optimization, results indicated that time efficiency does not necessarily compromise energy efficiency, with potential cost-to-performance improvements around 1/5.

In conclusion, the AZE algorithm emerged as the most effective across different environments, particularly with the addition of parking floors. Future research could explore further optimizations using AI and machine learning techniques to develop an ideal elevator control system.

