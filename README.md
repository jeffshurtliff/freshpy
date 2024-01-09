<a href='https://pypi.org/project/freshpy/'>
    <img src="https://github.com/jeffshurtliff/freshpy/blob/main/docs/_static/freshpy-logo.png" width="100" />
</a>

# FreshPy
A Python toolset for utilizing the Freshservice API

<table>
    <tr>
        <td>Latest Stable Release</td>
        <td>
            <a href='https://pypi.org/project/freshpy/'>
                <img alt="PyPI" src="https://img.shields.io/pypi/v/freshpy">
            </a>
        </td>
    </tr>
    <tr>
        <td>Latest Dev/Beta/RC Release</td>
        <td>
            <a href='https://pypi.org/project/freshpy/#history'>
                <img alt="PyPI" src="https://img.shields.io/badge/pypi-1.1.0b1-blue">
            </a>
        </td>
    </tr>
    <tr>
        <td>Build Status</td>
        <td>
            N/A
            <!--
            <a href="https://github.com/jeffshurtliff/freshpy/blob/master/.github/workflows/pythonpackage.yml">
                <img alt="GitHub Workflow Status" 
                src="https://img.shields.io/github/workflow/status/jeffshurtliff/freshpy/Python package">
            </a>
            -->
        </td>
    </tr>
    <tr>
        <td>Supported Versions</td>
        <td>
            <a href='https://pypi.org/project/freshpy/'>
                <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/freshpy">
            </a>
        </td>
    </tr>
    <!--
    <tr>
        <td>Code Coverage</td>
        <td>
            <a href="https://codecov.io/gh/jeffshurtliff/freshpy">
                <img src="https://codecov.io/gh/jeffshurtliff/freshpy/branch/master/graph/badge.svg" />
            </a>
        </td>
    </tr>
    <tr>
        <td>Code Quality (LGTM)</td>
        <td>
            <a href="https://lgtm.com/projects/g/jeffshurtliff/freshpy">
            <img alt="LGTM Grade" src="https://img.shields.io/lgtm/grade/python/github/jeffshurtliff/freshpy">
            </a>
        </td>
    </tr>
    <tr>
        <td>CodeFactor Grade</td>
        <td>
            <a href="https://lgtm.com/projects/g/jeffshurtliff/freshpy">
            <img alt="CodeFactor Grade" src="https://img.shields.io/codefactor/grade/github/jeffshurtliff/freshpy">
            </a>
        </td>
    </tr>
    -->
    <tr>
        <td>Documentation</td>
        <td>
            <a href='https://freshpy.readthedocs.io/en/latest/?badge=latest'>
                <img src='https://readthedocs.org/projects/freshpy/badge/?version=latest' alt='Documentation Status' /><br />
            </a>
        </td>
    </tr>
    <!--
    <tr>
        <td>Security Audits</td>
        <td>
            <a href="https://github.com/marketplace/actions/python-security-check-using-bandit">
                <img alt="Bandit" src="https://img.shields.io/badge/security-bandit-yellow.svg">
            </a><br />
            <a href="https://github.com/marketplace/actions/pycharm-python-security-scanner">
                <img alt="PyCharm Security Scanner" src="https://img.shields.io/badge/security-pycharm%20security%20scanner-green">
            </a>
        </td>
    </tr>
    -->
    <tr>
        <td>License</td>
        <td>
            <a href="https://github.com/jeffshurtliff/freshpy/blob/master/LICENSE">
                <img alt="License (GitHub)" src="https://img.shields.io/github/license/jeffshurtliff/freshpy">
            </a>
        </td>
    </tr>
    <tr>
        <td style="vertical-align: top;">Issues</td>
        <td>
            <a href="https://github.com/jeffshurtliff/freshpy/issues">
                <img style="margin-bottom:5px;" alt="GitHub open issues" src="https://img.shields.io/github/issues-raw/jeffshurtliff/freshpy"><br />
            </a>
            <a href="https://github.com/jeffshurtliff/freshpy/issues">
                <img alt="GitHub closed issues" src="https://img.shields.io/github/issues-closed-raw/jeffshurtliff/freshpy">
            </a>
        </td>
    </tr>
    <tr>
        <td style="vertical-align: top;">Pull Requests</td>
        <td>
            <a href="https://github.com/jeffshurtliff/freshpy/pulls">
                <img style="margin-bottom:5px;" alt="GitHub pull open requests" src="https://img.shields.io/github/issues-pr-raw/jeffshurtliff/freshpy"><br />
            </a>
            <a href="https://github.com/jeffshurtliff/freshpy/pulls">
                <img alt="GitHub closed pull requests" src="https://img.shields.io/github/issues-pr-closed-raw/jeffshurtliff/freshpy">
            </a>
        </td>
    </tr>
</table>

## Installation
The package can be installed via pip using the syntax below.

```sh
pip install freshpy --upgrade
```

You may also clone the repository and install from source using below.

```sh
git clone git://github.com/jeffshurtliff/freshpy.git
cd freshpy/
python setup.py install
```

## Usage
This section provides basic usage instructions for the package.

### Importing the package
Rather than importing the base package, it is recommended that you import the primary `FreshPy` class using the syntax
below.

```python
from freshpy import FreshPy
```

### Initializing a FreshPy object instance
The primary `FreshPy` object serves many purposes, the most important being to establish a connection to the 
Freshservice environment with which you intend to interact. As such, when initializing an instance of the `FreshPy` 
object, you will need to pass it the Freshservice URL (e.g. `example.freshservice.com`) and the API key it will use 
to authenticate so that the connection can be established.

#### Passing the information directly into the object
The domain and API key can be passed directly into the `FreshPy` object when initializing it, as
demonstrated in the example below.

```python
fresh = FreshPy(domain='example.freshservice.com', api_key='abc123DEF456')
```

### Interacting with the Freshservice API
Once the `FreshPy` object instance has been initialized, it can be leveraged to interact with a Freshservice
environment in many ways, which is fully documented in the official
[documentation](https://api.freshservice.com/). The example below demonstrates how information for a specific incident 
ticket can be retrieved in JSON format.

```python
ticket_data = fresh.tickets.get_ticket(1299)
```

## License
[MIT License](https://github.com/jeffshurtliff/freshpy/blob/master/LICENSE)

## Changelog
Refer to the [changelog](https://freshpy.readthedocs.io/en/latest/changelog.html) for version change information.

## Reporting Issues
Issues can be reported within the [GitHub repository](https://github.com/jeffshurtliff/freshpy/issues).

## Additional Resources
Additional resources for leveraging the Freshservice API can be found in the official
[Freshservice API Reference Documentation](https://api.freshservice.com/).

## Donations
If you would like to donate to this project then you can do so using 
[this PayPal link](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=XDZ8M6UV6EFK6&item_name=FreshPy&currency_code=USD).

## Disclaimer
This package is considered unofficial and is in no way endorsed or supported by 
[Freshservice](https://www.freshservice.com).

