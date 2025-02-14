# SPDX-FileCopyrightText: 2025-present Bogatyrev Aleksandr <bogatirevas.dev@gmail.com>

"""
Stopwatch
"""

import time


stopwatches = {}


class Localization:
    language: str = "en"
    text_map: dict = {
        "en": {
            "h": "hours",
            "m": "minutes",
            "s": "seconds",
        },
        "ru": {
            "h": "час.",
            "m": "мин.",
            "s": "сек.",
        }
    }

    @staticmethod
    def get(key: str):
        return Localization.text_map[Localization.language][key]


class StopwatchConfig:
    should_delete_stopwatch: bool = True
    round_number: int | None = 4
    result_format: str | None = None


class Stopwatch:
    def __init__(self, mark: str, start: int = None):
        self._mark = mark
        self._start = None
        self._end = None
        self._total = None
        self.set_start(start)
        self._conf = StopwatchConfig()
        stopwatches[mark] = self

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    @property
    def total(self):
        return self._total

    @property
    def mark(self):
        return self._mark

    def _round_time(self, round_number: int = None):
        round_number = self._conf.round_number if round_number is None else round_number
        result = self.total
        if round_number is not None:
            result = round_(result, round_number)
        return result

    def set_start(self, start: float = None):
        self._start = time.time() if start is None else start
        return self.start

    def _set_end(self):
        self._end = time.time()
        self._total = self.end - self.start
        return self.end

    def get_total_time(self, round_number: int = None, should_delete_stopwatch: bool = None,
                       result_format: str = None):
        """
        Return total time in the specified format, if args is None, then get it from StopwatchConfig

        :param round_number: if not None, then round by int value
        :param should_delete_stopwatch: if True, then delete stopwatch from "stopwatches" for create new instance when
            call get_stopwatch with current mark
        :param result_format: if not None, then uses format_total_time before return result
        """
        should_delete_stopwatch = self._conf.should_delete_stopwatch \
            if should_delete_stopwatch is None else should_delete_stopwatch
        result_format = self._conf.result_format if result_format is None else result_format
        self._set_end()
        if should_delete_stopwatch:
            delete_stopwatch(self.mark)
        if result_format is not None:
            return format_total_time(self.total, result_format)
        return self._round_time(round_number)


def get_stopwatch(mark: str):
    """
    init new or find an existing stopwatch

    :param mark: global mark for the search
    """
    stopwatch = stopwatches.get(mark)
    if stopwatch is None:
        stopwatch = Stopwatch(mark)
    return stopwatch


def delete_stopwatch(mark):
    result = stopwatches.pop(mark, "DontExist")
    if result == "DontExist":
        return False
    return True


def convert_total_time(total: float, hour=True, minute=True):
    """
    :param total: time in seconds
    :param hour: if True, subtract hours and add "h" key to result
    :param minute: if True, subtract minutes and add "m" key to result
    """
    result = {}
    if hour:
        result["h"] = int(total // 3600)
        total = total % 3600
    if minute:
        result["m"] = int(total // 60)
        total = total % 60
    result["s"] = int(total)
    return result


def format_total_time(total: float, result_format: str = "hms|time") -> str:
    """
    :param total: time in seconds
    :param result_format: format examples:
        "hms|time" = 00:00:00,
        "ms|char" = 0m0s,
        "s|text" = 0 seconds
    """
    hour = False
    minute = False
    if result_format[0] == "h":
        hour = True
    if (result_format[0] == "m") or (result_format[1] == "m"):
        minute = True
    converted = convert_total_time(total, hour, minute)
    sep_format = result_format.split("|")[1]

    result_list = []
    for key, val in converted.items():
        if sep_format == "time":
            result_list.append(f"{val:02}")
        elif sep_format == "char":
            result_list.append(f"{val}{Localization.get(key)[0]}")
        elif sep_format == "text":
            result_list.append(f"{val} {Localization.get(key)}")
    sep_map = {
        "time": ":",
        "char": "",
        "text": " ",
    }
    return sep_map[sep_format].join(result_list)


def round_(number, ndigits=None):
    if ndigits in [None, 0]:
        ndigits = None
    return round(number, ndigits)


if __name__ == "__main__":
    StopwatchConfig.round_number = 5
    StopwatchConfig.should_delete_stopwatch = False
    Localization.text_map["fictive_lang"] = {
        "h": "[*-*]",
        "m": "(-_-)",
        "s": ")-_-(",
    }
    Localization.language = "fictive_lang"
    test_stopwatch = get_stopwatch("test")
    time.sleep(1)
    print(test_stopwatch.get_total_time())
    print(get_stopwatch("test").get_total_time(result_format="hms|time"))
    print(get_stopwatch("test").get_total_time(result_format="hms|char"))
    print(get_stopwatch("test").get_total_time(result_format="hms|text"))
    print(get_stopwatch("test").get_total_time(round_number=0))
