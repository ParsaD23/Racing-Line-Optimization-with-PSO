<h1 align="center">Racing Line Optimization with PSO</h1>

This repository contains a racing line optimization algorithm in python that uses **Particle Swarm Optimization**.

## Requirements

This version was developed and tested with ```python==3.8.12```. The following modules are required:
* ```matplotlib```
* ```numpy```
* ```scipy```
* ```shapely```

## How does it work?

### 1. Input Parameters

The **input** parameters are:
- `track_layout`: array of $(x,y)$ coordinates that represent the layout of the track.
- `width`: width of the track. We assume it is constant along the track.
They are stored in the `./data/tracks.json` file.

### 2. Define the search space

The **track borders** are obtained by adding an offset (i.e. half of the `width`) to the `track_layout` in both directions (left and right).

Now, we define the **search space** of the algorithm, namely the sectors. Sectors are equally distanced segments that go from the outer border to inner border of the track. The points through which the racing line passes, will move along these segments:

![](imgs/Sectors.png)

### 3. Compute racing line

To find the racing line, the algorithm will fit a cubic spline to the sector points. The vehicles's speed at each point $i$ of the racing line is computed as:

$$ v_i = \sqrt{\mu * r_i * 9.81} $$

where $\mu$ is the coeffcient of friction (set to $0.13$) and $r$ is the radius of curvature which is computed as:

$$ r = \frac{1}{k} \quad \text{with} \quad k = \frac{|x'y''-y'x''|}{(x'^2+y'^2)^{3/2}} $$

where $x$ and $y$ are the coordinates of each point of the spline.

The algorithm's **objective** is to compute the fastest racing line around the track based on the laptime. Having the speed and the distance between each pair of points computed by the spline, we can compute the laptime.

## Run the algorithm

Run the `main.py` script to see the optimizer work. Inside the main function you will have the possibility to change the hyper-parameters of the PSO algorithm.

![](imgs/RacingLineEvolution.gif)

![](imgs/LapTimeEvolution.png)

## License

This project is under the MIT license. See [LICENSE](https://github.com/ParsaD23/Racing-Line-Optimization-with-PSO/blob/master/LICENSE) for more information.
