# CLI Help

## `python -m api_test_hub --help`

```text
usage: api-test-hub [-h] {generate,run,init} ...

positional arguments:
  {generate,run,init}
    generate           Generate pytest file from config
    run                Run cases from config file
    init               Generate template project

optional arguments:
  -h, --help           show this help message and exit
```

## `python -m api_test_hub generate --help`

```text
usage: api-test-hub generate [-h] -c CONFIG -o OUTPUT

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Config file path
  -o OUTPUT, --output OUTPUT
                        Output pytest file path
```

## `python -m api_test_hub run --help`

```text
usage: api-test-hub run [-h] (-c CONFIG | -p PROJECT) [--log-dir LOG_DIR]
                        [--timeout TIMEOUT] [--no-allure]
                        [--allure-results ALLURE_RESULTS]
                        [--allure-report ALLURE_REPORT]

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Config file path
  -p PROJECT, --project PROJECT
                        Project directory
  --log-dir LOG_DIR     Log directory path
  --timeout TIMEOUT     Request timeout
  --no-allure           Run directly without generating Allure results/report
  --allure-results ALLURE_RESULTS
                        Allure results directory
  --allure-report ALLURE_REPORT
                        Allure HTML report directory
```

## `python -m api_test_hub init --help`

```text
usage: api-test-hub init [-h] -o OUTPUT

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Target directory
```
