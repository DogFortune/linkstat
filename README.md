# linkstat
<div align="center">
[![test-lint-format](https://github.com/DogFortune/linkstat/actions/workflows/lint-test-format.yml/badge.svg?branch=main)](https://github.com/DogFortune/linkstat/actions) [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
</div>

<table>
	<thead>
    	<tr>
      		<th style="text-align:center">English</th>
      		<th style="text-align:center"><a href="README_JP.md">日本語</a></th>
    	</tr>
  	</thead>
</table>

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

If no path is specified, the current directory will be scanned.

## Output

You can output reports in JSON format by using the option.

```sh
linkstat --report-json {path} {source_file_or_directory}
```

## Contribute
[Guideline](CONTRIBUTING.md)