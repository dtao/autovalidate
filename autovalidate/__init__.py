import os

from autovalidate.reporters import get_reporter
from autovalidate.validators import get_validator


def find_and_validate(directory, **options):
    for root, dirs, files in os.walk(directory):
        for filename in files:
            basename, ext = os.path.splitext(filename)
            validator = get_validator(ext)
            if validator is None:
                continue
            yield validator.validate(os.path.join(root, filename))


def autovalidate(directory, reporter, **options):
    reporter = get_reporter(reporter)
    for result in find_and_validate(directory, **options):
        reporter.record(result)

    reporter.summarize()

    return reporter.invalid_count == 0
