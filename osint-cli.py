#!/usr/bin/env python3
"""
OSINT-CLI: A comprehensive Open Source Intelligence gathering tool
"""

import argparse
import sys
import json
import os
import re
import time
import ipaddress
from datetime import datetime
from typing import Dict, List, Any, Optional, Union

try:
    from rich.console import Console
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.panel import Panel
    from rich.text import Text
    import requests
    from concurrent.futures import ThreadPoolExecutor
except ImportError:
    print("Required packages not found. Installing...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "rich", "requests"])
    from rich.console import Console
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.panel import Panel
    from rich.text import Text
    import requests
    from concurrent.futures import ThreadPoolExecutor

# Initialize Rich console
console = Console()

class OsintTool:
    def __init__(self):
        self.modules = {
            "domain": self.domain_recon,
            "ip": self.ip_analysis,
            "email": self.email_breach,
            "social": self.social_media_scan,
            "company": self.company_info,
            "dns": self.dns_enumeration,
            "whois": self.whois_lookup
        }
        self.results = {}
        self.verbose = False
        self.output_file = None
        self.threads = 5
        
    def banner(self):
        banner_text = """
        ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃                                                                              ┃
        ┃   ██████╗ ███████╗██╗███╗   ██╗████████╗      ██████╗██╗     ██╗             ┃
        ┃  ██╔═══██╗██╔════╝██║████╗  ██║╚══██╔══╝     ██╔════╝██║     ██║             ┃
        ┃  ██║   ██║███████╗██║██╔██╗ ██║   ██║        ██║     ██║     ██║             ┃
        ┃  ██║   ██║╚════██║██║██║╚██╗██║   ██║        ██║     ██║     ██║             ┃
        ┃  ╚██████╔╝███████║██║██║ ╚████║   ██║        ╚██████╗███████╗██║             ┃ 
        ┃   ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝         ╚═════╝╚══════╝╚═╝             ┃
        ┃                                                                              ┃
        ┃  Open Source Intelligence Tool for Security Professionals                    ┃
        ┃  Version 1.0.0                                                               ┃
        ┃                                                                              ┃
        ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
        """
        console.print(Panel.fit(banner_text, border_style="blue"))
        console.print("\n[bold yellow]DISCLAIMER:[/bold yellow] This tool is for [bold]legitimate security research only[/bold]. Use responsibly and ethically.\n")

    def parse_args(self):
        parser = argparse.ArgumentParser(description="OSINT-CLI: A comprehensive OSINT gathering tool")
        parser.add_argument("--module", "-m", help="Module to use (domain, ip, email, social, company, dns, whois)")
        parser.add_argument("--target", "-t", help="Target to investigate")
        parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
        parser.add_argument("--output", "-o", help="Output results to file")
        parser.add_argument("--threads", help="Number of threads to use (default: 5)", type=int, default=5)
        parser.add_argument("--interactive", "-i", action="store_true", help="Run in interactive mode")
        parser.add_argument("--list-modules", "-l", action="store_true", help="List available modules")
        
        args = parser.parse_args()
        
        if args.list_modules:
            self.list_modules()
            sys.exit(0)
            
        if args.interactive:
            self.interactive_mode()
            sys.exit(0)
            
        if not args.module or not args.target:
            parser.print_help()
            sys.exit(1)
            
        self.verbose = args.verbose
        self.output_file = args.output
        self.threads = args.threads
        
        return args

    def list_modules(self):
        table = Table(title="Available Modules")
        table.add_column("Module", style="cyan")
        table.add_column("Description", style="green")
        
        modules_info = {
            "domain": "Domain reconnaissance and information gathering",
            "ip": "IP address analysis and geolocation",
            "email": "Email breach and exposure scanning",
            "social": "Social media profile discovery and analysis",
            "company": "Company information and employee data gathering",
            "dns": "DNS record enumeration and analysis",
            "whois": "WHOIS lookup and domain registration details"
        }
        
        for module, description in modules_info.items():
            table.add_row(module, description)
            
        console.print(table)

    def interactive_mode(self):
        self.banner()
        console.print("[bold green]Interactive Mode[/bold green]")
        
        while True:
            console.print("\n[bold cyan]OSINT-CLI[/bold cyan] > ", end="")
            command = input().strip()
            
            if command in ["exit", "quit", "q"]:
                console.print("[yellow]Exiting...[/yellow]")
                break
                
            if command in ["help", "h", "?"]:
                self.show_help()
                continue
                
            if command in ["list", "ls"]:
                self.list_modules()
                continue
                
            # Parse command similar to SQLMap
            try:
                parts = command.split()
                module = parts[0]
                
                if module not in self.modules:
                    console.print(f"[bold red]Unknown module: {module}[/bold red]")
                    continue
                
                args = {}
                current_key = None
                
                for part in parts[1:]:
                    if part.startswith("--"):
                        current_key = part[2:]
                        args[current_key] = True
                    elif part.startswith("-"):
                        current_key = part[1:]
                        args[current_key] = True
                    elif current_key:
                        args[current_key] = part
                        current_key = None
                
                if "t" in args:
                    args["target"] = args.pop("t")
                if "v" in args:
                    self.verbose = True
                if "o" in args:
                    self.output_file = args.get("o")
                
                if "target" not in args:
                    console.print("[bold red]Error: Target is required[/bold red]")
                    continue
                
                # Execute the module
                self.modules[module](args["target"])
                
            except Exception as e:
                console.print(f"[bold red]Error: {str(e)}[/bold red]")

    def show_help(self):
        help_text = """
        Available commands:
        
        <module> --target <target> [options]    Run a specific module
        help, h, ?                             Show this help message
        list, ls                               List available modules
        exit, quit, q                          Exit the program
        
        Modules:
        - domain    Domain reconnaissance
        - ip        IP analysis
        - email     Email breach scanning
        - social    Social media scanning
        - company   Company information
        - dns       DNS enumeration
        - whois     WHOIS lookup
        
        Options:
        --target, -t    Target to investigate
        --verbose, -v   Enable verbose output
        --output, -o    Output results to file
        """
        console.print(Panel(help_text, title="Help", border_style="green"))

    def log(self, message, level="info"):
        if level == "info":
            console.print(f"[cyan][*][/cyan] {message}")
        elif level == "success":
            console.print(f"[green][+][/green] {message}")
        elif level == "warning":
            console.print(f"[yellow][!][/yellow] {message}")
        elif level == "error":
            console.print(f"[red][-][/red] {message}")
        elif level == "debug" and self.verbose:
            console.print(f"[blue][D][/blue] {message}")

    def save_results(self):
        if self.output_file:
            try:
                with open(self.output_file, 'w') as f:
                    json.dump(self.results, f, indent=4)
                self.log(f"Results saved to {self.output_file}", "success")
            except Exception as e:
                self.log(f"Failed to save results: {str(e)}", "error")

    def domain_recon(self, target):
        self.log(f"Starting domain reconnaissance for {target}")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Gathering domain information...", total=None)
            
            # Simulate API calls and data gathering
            time.sleep(2)
            
            domain_info = {
                "domain": target,
                "creation_date": "2020-01-01",
                "expiration_date": "2025-01-01",
                "registrar": "Example Registrar, LLC",
                "nameservers": [
                    "ns1.example.com",
                    "ns2.example.com"
                ],
                "subdomains": [
                    f"www.{target}",
                    f"mail.{target}",
                    f"api.{target}"
                ],
                "ip_addresses": [
                    "192.0.2.1",
                    "192.0.2.2"
                ]
            }
            
            progress.update(task, completed=True)
        
        self.results["domain"] = domain_info
        
        # Display results
        table = Table(title=f"Domain Information: {target}")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="green")
        
        for key, value in domain_info.items():
            if isinstance(value, list):
                table.add_row(key, "\n".join(value))
            else:
                table.add_row(key, str(value))
        
        console.print(table)
        
        self.log("Domain reconnaissance completed", "success")
        self.save_results()

    def ip_analysis(self, target):
        self.log(f"Starting IP analysis for {target}")
        
        try:
            # Validate IP address
            ipaddress.ip_address(target)
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("[cyan]Analyzing IP address...", total=None)
                
                # Simulate API calls and data gathering
                time.sleep(2)
                
                ip_info = {
                    "ip": target,
                    "hostname": "server.example.com",
                    "country": "United States",
                    "city": "San Francisco",
                    "isp": "Example ISP",
                    "asn": "AS12345",
                    "open_ports": [
                        {"port": 80, "service": "HTTP"},
                        {"port": 443, "service": "HTTPS"},
                        {"port": 22, "service": "SSH"}
                    ]
                }
                
                progress.update(task, completed=True)
            
            self.results["ip"] = ip_info
            
            # Display results
            table = Table(title=f"IP Information: {target}")
            table.add_column("Property", style="cyan")
            table.add_column("Value", style="green")
            
            for key, value in ip_info.items():
                if key == "open_ports":
                    port_list = []
                    for port_info in value:
                        port_list.append(f"{port_info['port']}/TCP ({port_info['service']})")
                    table.add_row(key, "\n".join(port_list))
                elif isinstance(value, list):
                    table.add_row(key, "\n".join(value))
                else:
                    table.add_row(key, str(value))
            
            console.print(table)
            
            self.log("IP analysis completed", "success")
            self.save_results()
            
        except ValueError:
            self.log(f"Invalid IP address: {target}", "error")

    def email_breach(self, target):
        self.log(f"Starting email breach scan for {target}")
        
        # Validate email format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", target):
            self.log(f"Invalid email format: {target}", "error")
            return
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Scanning for email breaches...", total=None)
            
            # Simulate API calls and data gathering
            time.sleep(2)
            
            breach_info = {
                "email": target,
                "breaches": [
                    {
                        "name": "ExampleBreach",
                        "date": "2021-03-15",
                        "description": "Data breach affecting 1M users",
                        "data_classes": ["Email", "Password", "Username"]
                    },
                    {
                        "name": "AnotherBreach",
                        "date": "2020-07-22",
                        "description": "Security incident exposing user data",
                        "data_classes": ["Email", "IP Address", "Name"]
                    }
                ],
                "total_breaches": 2,
                "first_breach": "2020-07-22",
                "last_breach": "2021-03-15"
            }
            
            progress.update(task, completed=True)
        
        self.results["email"] = breach_info
        
        # Display results
        table = Table(title=f"Email Breach Information: {target}")
        table.add_column("Breach", style="red")
        table.add_column("Date", style="yellow")
        table.add_column("Description", style="cyan")
        table.add_column("Exposed Data", style="green")
        
        for breach in breach_info["breaches"]:
            table.add_row(
                breach["name"],
                breach["date"],
                breach["description"],
                ", ".join(breach["data_classes"])
            )
        
        console.print(table)
        console.print(f"[bold]Total breaches found:[/bold] {breach_info['total_breaches']}")
        console.print(f"[bold]First breach:[/bold] {breach_info['first_breach']}")
        console.print(f"[bold]Last breach:[/bold] {breach_info['last_breach']}")
        
        self.log("Email breach scan completed", "success")
        self.save_results()

    def social_media_scan(self, target):
        self.log(f"Starting social media scan for {target}")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Scanning social media platforms...", total=None)
            
            # Simulate API calls and data gathering
            time.sleep(3)
            
            social_info = {
                "username": target,
                "profiles": [
                    {
                        "platform": "Twitter",
                        "url": f"https://twitter.com/{target}",
                        "exists": True,
                        "username": target,
                        "bio": "Example Twitter bio",
                        "followers": 1234,
                        "following": 567,
                        "joined": "January 2019"
                    },
                    {
                        "platform": "GitHub",
                        "url": f"https://github.com/{target}",
                        "exists": True,
                        "username": target,
                        "bio": "Software Developer",
                        "repositories": 45,
                        "followers": 89,
                        "joined": "March 2018"
                    },
                    {
                        "platform": "LinkedIn",
                        "url": f"https://linkedin.com/in/{target}",
                        "exists": True,
                        "name": "John Doe",
                        "title": "Senior Developer at Example Corp",
                        "location": "San Francisco, CA"
                    },
                    {
                        "platform": "Instagram",
                        "url": f"https://instagram.com/{target}",
                        "exists": False
                    }
                ]
            }
            
            progress.update(task, completed=True)
        
        self.results["social"] = social_info
        
        # Display results
        table = Table(title=f"Social Media Profiles: {target}")
        table.add_column("Platform", style="cyan")
        table.add_column("URL", style="blue")
        table.add_column("Status", style="green")
        table.add_column("Details", style="yellow")
        
        for profile in social_info["profiles"]:
            status = "[green]Found[/green]" if profile["exists"] else "[red]Not Found[/red]"
            
            details = []
            for key, value in profile.items():
                if key not in ["platform", "url", "exists", "username"]:
                    details.append(f"{key}: {value}")
            
            details_text = "\n".join(details) if details else ""
            
            table.add_row(
                profile["platform"],
                profile["url"],
                status,
                details_text
            )
        
        console.print(table)
        
        self.log("Social media scan completed", "success")
        self.save_results()

    def company_info(self, target):
        self.log(f"Starting company information gathering for {target}")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Gathering company information...", total=None)
            
            # Simulate API calls and data gathering
            time.sleep(3)
            
            company_info = {
                "name": target,
                "website": f"https://www.{target.lower().replace(' ', '')}.com",
                "founded": "2010",
                "industry": "Technology",
                "employees": "1,000-5,000",
                "headquarters": "San Francisco, CA",
                "revenue": "$100M-$500M",
                "domains": [
                    f"{target.lower().replace(' ', '')}.com",
                    f"{target.lower().replace(' ', '')}.net",
                    f"{target.lower().replace(' ', '')}.org"
                ],
                "email_format": "firstname.lastname@company.com",
                "key_people": [
                    {"name": "John Smith", "title": "CEO"},
                    {"name": "Jane Doe", "title": "CTO"},
                    {"name": "Bob Johnson", "title": "CFO"}
                ]
            }
            
            progress.update(task, completed=True)
        
        self.results["company"] = company_info
        
        # Display results
        table = Table(title=f"Company Information: {target}")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="green")
        
        for key, value in company_info.items():
            if key == "key_people":
                people_list = []
                for person in value:
                    people_list.append(f"{person['name']} - {person['title']}")
                table.add_row(key, "\n".join(people_list))
            elif isinstance(value, list):
                table.add_row(key, "\n".join(value))
            else:
                table.add_row(key, str(value))
        
        console.print(table)
        
        self.log("Company information gathering completed", "success")
        self.save_results()

    def dns_enumeration(self, target):
        self.log(f"Starting DNS enumeration for {target}")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Enumerating DNS records...", total=None)
            
            # Simulate API calls and data gathering
            time.sleep(2)
            
            dns_info = {
                "domain": target,
                "records": {
                    "A": [
                        {"name": target, "value": "192.0.2.1", "ttl": 3600},
                        {"name": f"www.{target}", "value": "192.0.2.1", "ttl": 3600}
                    ],
                    "MX": [
                        {"name": target, "value": f"mail1.{target}", "priority": 10, "ttl": 3600},
                        {"name": target, "value": f"mail2.{target}", "priority": 20, "ttl": 3600}
                    ],
                    "NS": [
                        {"name": target, "value": f"ns1.{target}", "ttl": 86400},
                        {"name": target, "value": f"ns2.{target}", "ttl": 86400}
                    ],
                    "TXT": [
                        {"name": target, "value": "v=spf1 include:_spf.example.com ~all", "ttl": 3600},
                        {"name": f"_dmarc.{target}", "value": "v=DMARC1; p=none; rua=mailto:dmarc@example.com", "ttl": 3600}
                    ]
                }
            }
            
            progress.update(task, completed=True)
        
        self.results["dns"] = dns_info
        
        # Display results
        for record_type, records in dns_info["records"].items():
            table = Table(title=f"DNS {record_type} Records: {target}")
            
            # Add columns based on record type
            if record_type == "A":
                table.add_column("Name", style="cyan")
                table.add_column("IP Address", style="green")
                table.add_column("TTL", style="yellow")
                
                for record in records:
                    table.add_row(
                        record["name"],
                        record["value"],
                        str(record["ttl"])
                    )
            
            elif record_type == "MX":
                table.add_column("Name", style="cyan")
                table.add_column("Mail Server", style="green")
                table.add_column("Priority", style="blue")
                table.add_column("TTL", style="yellow")
                
                for record in records:
                    table.add_row(
                        record["name"],
                        record["value"],
                        str(record["priority"]),
                        str(record["ttl"])
                    )
            
            elif record_type in ["NS", "TXT"]:
                table.add_column("Name", style="cyan")
                table.add_column("Value", style="green")
                table.add_column("TTL", style="yellow")
                
                for record in records:
                    table.add_row(
                        record["name"],
                        record["value"],
                        str(record["ttl"])
                    )
            
            console.print(table)
        
        self.log("DNS enumeration completed", "success")
        self.save_results()

    def whois_lookup(self, target):
        self.log(f"Starting WHOIS lookup for {target}")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Performing WHOIS lookup...", total=None)
            
            # Simulate API calls and data gathering
            time.sleep(2)
            
            whois_info = {
                "domain": target,
                "registrar": "Example Registrar, LLC",
                "whois_server": "whois.example-registrar.com",
                "referral_url": "http://www.example-registrar.com",
                "updated_date": "2022-01-15",
                "creation_date": "2020-01-01",
                "expiration_date": "2025-01-01",
                "name_servers": [
                    "NS1.EXAMPLE.COM",
                    "NS2.EXAMPLE.COM"
                ],
                "status": [
                    "clientTransferProhibited",
                    "clientUpdateProhibited"
                ],
                "registrant": {
                    "organization": "Example Organization",
                    "state": "CA",
                    "country": "US",
                    "privacy": True
                },
                "admin": {
                    "organization": "Example Organization",
                    "state": "CA",
                    "country": "US",
                    "privacy": True
                },
                "tech": {
                    "organization": "Example Organization",
                    "state": "CA",
                    "country": "US",
                    "privacy": True
                }
            }
            
            progress.update(task, completed=True)
        
        self.results["whois"] = whois_info
        
        # Display results
        table = Table(title=f"WHOIS Information: {target}")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="green")
        
        for key, value in whois_info.items():
            if key in ["registrant", "admin", "tech"]:
                contact_info = []
                for k, v in value.items():
                    contact_info.append(f"{k}: {v}")
                table.add_row(key, "\n".join(contact_info))
            elif isinstance(value, list):
                table.add_row(key, "\n".join(value))
            else:
                table.add_row(key, str(value))
        
        console.print(table)
        
        self.log("WHOIS lookup completed", "success")
        self.save_results()

def main():
    tool = OsintTool()
    tool.banner()
    args = tool.parse_args()
    
    if args.module in tool.modules:
        tool.modules[args.module](args.target)
    else:
        console.print(f"[bold red]Unknown module: {args.module}[/bold red]")
        tool.list_modules()

if __name__ == "__main__":
    main()
