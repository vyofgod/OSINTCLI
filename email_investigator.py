"""
Email Investigation Module for OSINT-CLI
"""

import time
import re
import hashlib
from typing import Dict, List, Any, Optional, Union
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel

console = Console()

class EmailInvestigator:
    def __init__(self, verbose=False):
        self.verbose = verbose
        
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
    
    def validate_email(self, email: str) -> bool:
        """Validate email format"""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))
    
    def investigate_email(self, email: str) -> Dict[str, Any]:
        """
        Investigate an email address for breaches, social profiles, and other information
        """
        if not self.validate_email(email):
            self.log(f"Invalid email format: {email}", "error")
            return {"error": "Invalid email format"}
        
        self.log(f"Starting investigation for email: {email}")
        
        results = {
            "email": email,
            "domain": email.split('@')[1],
            "username": email.split('@')[0],
            "breaches": [],
            "pastes": [],
            "social_profiles": [],
            "domain_info": {}
        }
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            # Check for breaches
            breach_task = progress.add_task("[cyan]Checking for breaches...", total=None)
            results["breaches"] = self._check_breaches(email)
            progress.update(breach_task, completed=True)
            
            # Check for pastes
            paste_task = progress.add_task("[cyan]Checking for pastes...", total=None)
            results["pastes"] = self._check_pastes(email)
            progress.update(paste_task, completed=True)
            
            # Check for social profiles
            social_task = progress.add_task("[cyan]Finding social profiles...", total=None)
            results["social_profiles"] = self._find_social_profiles(email)
            progress.update(social_task, completed=True)
            
            # Get domain information
            domain_task = progress.add_task("[cyan]Gathering domain information...", total=None)
            results["domain_info"] = self._get_domain_info(results["domain"])
            progress.update(domain_task, completed=True)
        
        return results
    
    def _check_breaches(self, email: str) -> List[Dict[str, Any]]:
        """
        Check if email has been found in data breaches
        
        In a real implementation, this would use APIs like HaveIBeenPwned
        """
        # Simulate API call
        time.sleep(1.5)
        
        # For demonstration, we'll create some simulated breach data
        # In a real implementation, this would come from an API
        
        # Use email hash to consistently generate the same results for the same email
        email_hash = int(hashlib.md5(email.encode()).hexdigest(), 16)
        
        # Determine number of breaches (0-3) based on email hash
        num_breaches = email_hash % 4
        
        breaches = []
        breach_examples = [
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
            },
            {
                "name": "MajorServiceBreach",
                "date": "2019-11-05",
                "description": "Major service provider breach affecting 100M accounts",
                "data_classes": ["Email", "Password", "Name", "Phone", "Address"]
            }
        ]
        
        for i in range(num_breaches):
            breaches.append(breach_examples[i])
        
        return breaches
    
    def _check_pastes(self, email: str) -> List[Dict[str, Any]]:
        """
        Check if email has been found in pastes
        
        In a real implementation, this would use APIs like HaveIBeenPwned
        """
        # Simulate API call
        time.sleep(1)
        
        # Use email hash to consistently generate the same results for the same email
        email_hash = int(hashlib.md5(email.encode()).hexdigest(), 16)
        
        # Determine number of pastes (0-2) based on email hash
        num_pastes = email_hash % 3
        
        pastes = []
        paste_examples = [
            {
                "source": "Pastebin",
                "date": "2022-01-10",
                "title": "Leaked Credentials",
                "url": "https://pastebin.com/example1"
            },
            {
                "source": "GitHub Gist",
                "date": "2021-05-18",
                "title": "User Database",
                "url": "https://gist.github.com/example2"
            }
        ]
        
        for i in range(num_pastes):
            pastes.append(paste_examples[i])
        
        return pastes
    
    def _find_social_profiles(self, email: str) -> List[Dict[str, Any]]:
        """
        Find social profiles associated with the email
        
        In a real implementation, this would use various APIs and techniques
        """
        # Simulate API call
        time.sleep(1.2)
        
        # Use email hash to consistently generate the same results for the same email
        email_hash = int(hashlib.md5(email.encode()).hexdigest(), 16)
        
        # Determine which social profiles to include based on email hash
        profiles = []
        
        social_examples = [
            {
                "platform": "LinkedIn",
                "url": f"https://linkedin.com/in/{email.split('@')[0]}",
                "name": "John Doe",
                "title": "Software Engineer"
            },
            {
                "platform": "GitHub",
                "url": f"https://github.com/{email.split('@')[0]}",
                "repositories": 24,
                "followers": 45
            },
            {
                "platform": "Twitter",
                "url": f"https://twitter.com/{email.split('@')[0]}",
                "followers": 320,
                "following": 210
            },
            {
                "platform": "Facebook",
                "url": f"https://facebook.com/{email.split('@')[0]}",
                "name": "John Doe"
            }
        ]
        
        # Include 0-4 profiles based on email hash
        num_profiles = email_hash % 5
        for i in range(num_profiles):
            if i < len(social_examples):
                profiles.append(social_examples[i])
        
        return profiles
    
    def _get_domain_info(self, domain: str) -> Dict[str, Any]:
        """
        Get information about the email domain
        
        In a real implementation, this would use DNS lookups and other techniques
        """
        # Simulate API call
        time.sleep(0.8)
        
        # For demonstration, return simulated domain info
        return {
            "domain": domain,
            "mx_records": [
                f"mail1.{domain}",
                f"mail2.{domain}"
            ],
            "spf_record": f"v=spf1 include:_spf.{domain} ~all",
            "dmarc_record": f"v=DMARC1; p=none; rua=mailto:dmarc@{domain}",
            "registrar": "Example Registrar, LLC",
            "creation_date": "2010-05-17",
            "expiration_date": "2025-05-17"
        }
    
    def display_results(self, results: Dict[str, Any]) -> None:
        """Display email investigation results in a formatted output"""
        if "error" in results:
            console.print(f"[bold red]Error:[/bold red] {results['error']}")
            return
        
        console.print(Panel.fit(
            f"[bold]Email:[/bold] {results['email']}\n"
            f"[bold]Username:[/bold] {results['username']}\n"
            f"[bold]Domain:[/bold] {results['domain']}",
            title="Email Information",
            border_style="blue"
        ))
        
        # Display breaches
        if results["breaches"]:
            table = Table(title="Data Breaches")
            table.add_column("Breach", style="red")
            table.add_column("Date", style="yellow")
            table.add_column("Description", style="cyan")
            table.add_column("Exposed Data", style="green")
            
            for breach in results["breaches"]:
                table.add_row(
                    breach["name"],
                    breach["date"],
                    breach["description"],
                    ", ".join(breach["data_classes"])
                )
            
            console.print(table)
            console.print(f"[bold red]Total breaches found:[/bold red] {len(results['breaches'])}")
        else:
            console.print("[green]No breaches found for this email.[/green]")
        
        # Display pastes
        if results["pastes"]:
            table = Table(title="Pastes")
            table.add_column("Source", style="cyan")
            table.add_column("Date", style="yellow")
            table.add_column("Title", style="green")
            table.add_column("URL", style="blue")
            
            for paste in results["pastes"]:
                table.add_row(
                    paste["source"],
                    paste["date"],
                    paste["title"],
                    paste["url"]
                )
            
            console.print(table)
        else:
            console.print("[green]No pastes found for this email.[/green]")
        
        # Display social profiles
        if results["social_profiles"]:
            table = Table(title="Associated Social Profiles")
            table.add_column("Platform", style="cyan")
            table.add_column("URL", style="blue")
            table.add_column("Details", style="green")
            
            for profile in results["social_profiles"]:
                details = []
                for key, value in profile.items():
                    if key not in ["platform", "url"]:
                        details.append(f"{key}: {value}")
                
                details_text = "\n".join(details) if details else ""
                
                table.add_row(
                    profile["platform"],
                    profile["url"],
                    details_text
                )
            
            console.print(table)
        else:
            console.print("[yellow]No social profiles found for this email.[/yellow]")
        
        # Display domain information
        domain_info = results["domain_info"]
        if domain_info:
            table = Table(title=f"Domain Information: {domain_info['domain']}")
            table.add_column("Property", style="cyan")
            table.add_column("Value", style="green")
            
            for key, value in domain_info.items():
                if key != "domain":
                    if isinstance(value, list):
                        table.add_row(key, "\n".join(value))
                    else:
                        table.add_row(key, str(value))
            
            console.print(table)

def investigate_email(email: str, verbose: bool = False) -> Dict[str, Any]:
    """
    Main function to investigate an email address
    
    Returns a dictionary with all findings
    """
    investigator = EmailInvestigator(verbose=verbose)
    results = investigator.investigate_email(email)
    investigator.display_results(results)
    return results

if __name__ == "__main__":
    # Example usage when run directly
    investigate_email("test@example.com", verbose=True)