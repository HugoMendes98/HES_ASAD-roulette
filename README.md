# Roulette

> Jeu de roulette

## Run with docker

To build the image:
```bash
docker build . -t asad_roulette
```

To run the image:
```bash
docker run -it -p 5000:5000 asad_roulette
```

### Environment variables

| Variable | description |
| ------------ | ------------ |
| CONFIG_IDLE_TIME | Time the game stays in the `IDLE` state |
| CONFIG_BIDABLE_TIME | Time the game stays in the `BIDABLE` state |
| CONFIG_WAITING_TIME | Time the game stays in the `WAITING` state |
| CONFIG_RESULTS_TIME | Time the game stays in the `RESULTS` state |

Example:
```bash
docker run -it -p 5000:5000 \
  -e CONFIG_IDLE_TIME=20 \
  -e CONFIG_BIDABLE_TIME=20 \
  -e CONFIG_WAITING_TIME=20 \
  -e CONFIG_RESULTS_TIME=20 \
  asad_roulette
```
