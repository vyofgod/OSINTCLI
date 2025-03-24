# OSINT-CLI

A comprehensive Open Source Intelligence (OSINT) gathering tool with a command-line interface by VyOfGod.

## Features

- **Domain Reconnaissance**: Gather information about domains, including subdomains, IP addresses, and registration details.
- **IP Analysis**: Analyze IP addresses for geolocation, ISP information, and open ports.
- **Email Breach Scanning**: Check if email addresses have been exposed in data breaches.
- **Social Media Investigation**: Discover and analyze social media profiles across multiple platforms.
- **Company Information**: Gather details about companies, including key personnel and associated domains.
- **DNS Enumeration**: Enumerate and analyze DNS records.
- **WHOIS Lookup**: Retrieve domain registration details.

## Installation

```bash
# Clone the repository
git clone https://github.com/vyofgod/OSINTCLI.git
cd OSINTCLI

# Install dependencies
pip install -r requirements.txt
```

## Example Usage

OSINT-CLI utilizes modules for various intelligence-gathering tasks. Below are some basic usage examples:

### General Usage

```bash
python3 osint-cli.py --module <module_name> --target <target> [additional_arguments]
```

### Examples

#### Gathering information about a domain (IP addresses, subdomains, etc.)
```bash
python3 osint-cli.py --module domain --target example.com
```

#### Analyzing geolocation and ISP information of an IP address
```bash
python3 osint-cli.py --module ip --target 192.0.2.1
```

#### Checking if an email address has been involved in data breaches
```bash
python3 osint-cli.py --module email --target user@example.com
```

#### Searching for a username across multiple social media platforms
```bash
python3 osint-cli.py --module social --target username
```

#### Gathering information about a company (e.g., key personnel, domains)
```bash
python3 osint-cli.py --module company --target "Example Company"
```

#### Listing the DNS records for a given domain
```bash
python3 osint-cli.py --module dns --target example.com
```

#### Retrieving WHOIS information for a domain
```bash
python3 osint-cli.py --module whois --target example.com
```

### Getting Help for Modules

Each module has its own specific options and arguments. You can get more information using the `--help` argument:

```bash
python3 osint-cli.py --module domain --help
```

This command will display the usage instructions and available options for the `domain` module.

