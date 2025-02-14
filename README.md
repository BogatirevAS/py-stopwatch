# Stopwatch

-----

## Table of Contents

- [Installation](#installation)
- [Examples](#examples)

## Installation

- console
```console
pip install git+https://github.com/BogatirevAS/py-stopwatch.git@master
```
```console
pip install git+https://github.com/BogatirevAS/py-stopwatch.git@0.5.0
```

- requirements.txt
```requirements
stopwatch @ git+https://github.com/BogatirevAS/py-stopwatch.git@master
```
```requirements
stopwatch @ git+https://github.com/BogatirevAS/py-stopwatch.git@0.5.0
```

## Examples

```python
from stopwatch import get_stopwatch, Stopwatch
import time


# init stopwatch
test_stopwatch = get_stopwatch("test")
# alternative
# test_stopwatch = Stopwatch("test")

# wait and get result
time.sleep(1)
print(test_stopwatch.get_total_time())
# alternative
# print(get_stopwatch("test").get_total_time())
# 1.0002
```

```python
# change global config and print different result formats from stopwatch by mark
from stopwatch import get_stopwatch, StopwatchConfig
import time


StopwatchConfig.round_number = 5
StopwatchConfig.should_delete_stopwatch = False
print(get_stopwatch("test").get_total_time())
# 0.0
time.sleep(1)
print(get_stopwatch("test").get_total_time())
# 1.00018
print(get_stopwatch("test").get_total_time(result_format="hms|time"))
# 00:00:01
print(get_stopwatch("test").get_total_time(result_format="hms|char"))
# 0h0m1s
print(get_stopwatch("test").get_total_time(result_format="hms|text"))
# 0 hours 0 minutes 1 seconds
print(get_stopwatch("test").get_total_time(round_number=0))
# 1

# time.sleep(60)
# print(get_stopwatch("test").get_total_time(result_format="s|text"))
# 61 seconds
```

```python
# set your localization or edit default by "en" key
from stopwatch import Localization, get_stopwatch


Localization.text_map["fictive_lang"] = {
    "h": "[*-*]",
    "m": "(-_-)",
    "s": ")-_-(",
}
Localization.language = "fictive_lang"
# alternative
# Localization.text_map["en"] = {
#     "h": "[*-*]",
#     "m": "(-_-)",
#     "s": ")-_-(",
# }
test_stopwatch = get_stopwatch("test")
time.sleep(1)
print(get_stopwatch("test").get_total_time(result_format="hms|char"))
# 0[0(1)
# by default the stopwatch is deleted after receiving the result
get_stopwatch("test")
time.sleep(1)
print(get_stopwatch("test").get_total_time(should_delete_stopwatch=False, result_format="hms|text"))
# 0 [*-*] 0 (-_-) 1 )-_-(
time.sleep(1)
print(get_stopwatch("test").get_total_time(result_format="ms|char"))
# 0(2)
# first stopwatch has been removed from global visibility but can be used locally by keeping the reference
print(test_stopwatch.get_total_time())
# 3.0008
```