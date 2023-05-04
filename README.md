# H-Scenario-Generator
[Hyundai Research] Automated Generation of Driving Scenario

## Installation

Follow [INSTALL.md](./INSTALL.md)


## Execution

```shell
cd src
./init.sh
```
Make directory for scenario results

```shell
python ./run_random_scenario.py --town 2
```
You can switch town parameter. (1-5)

```shell
python ./run_random_scenario.py -x roundabout.xodr
```
You can load your own HD-Map(.xodr format) using `-x option` after add OpenDRIVE file in `src/ScenaVRo/HDMap2RoadGraph/HD-Map/`

## Simulation Results

After running the scenario, we can check the results in the artifact directory, `src/out-artifact/`.