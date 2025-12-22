# linkstat
[![test-lint-format](https://github.com/DogFortune/linkstat/actions/workflows/lint-test-format.yml/badge.svg?branch=main)](https://github.com/DogFortune/linkstat/actions) [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

_linkstat_ is a script that verifies the connectivity of links documented in the documentation. By detecting broken links early, it maintains the integrity of the documentation.  
Currently, only Markdown files (*.md) are supported.

## Caution
This library accesses services during runtime, so executing it in large quantities will cause load on the target service. When performing functional verification or integrating into CI/CD, please ensure the load on the linked service is minimized as much as possible.

## Install

```sh
pip install linkstat
```

## Usage

```sh
linkstat {source_file_or_directory}
```

## Output

You can output reports in JSON format by using the option.

```sh
linkstat --report-json {path} {source_file_or_directory}
```

## Contribute
[Guideline](CONTRIBUTING.md)