"""
Social Media Investigation Module for OSINT-CLI
"""

import time
import re
from typing import Dict, List, Any, Optional, Union
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

class SocialMediaInvestigator:
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.platforms = [
            "twitter", "facebook", "instagram", "linkedin", "github", 
            "reddit", "youtube", "tiktok", "pinterest", "snapchat",
            "medium", "quora", "stackoverflow", "hackernews", "dev.to"
        ]
        
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
    
    def search_username(self, username: str) -> Dict[str, Any]:
        """
        Search for a username across multiple social media platforms
        """
        self.log(f"Searching for username '{username}' across {len(self.platforms)} platforms")
        
        results = {
            "username": username,
            "profiles": []
        }
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Scanning social media platforms...", total=len(self.platforms))
            
            for platform in self.platforms:
                # In a real implementation, this would make API calls or web requests
                # Here we're simulating the process
                time.sleep(0.3)  # Simulate API call
                
                profile = self._check_platform(platform, username)
                if profile:
                    results["profiles"].append(profile)
                
                progress.update(task, advance=1, description=f"[cyan]Scanning {platform}...")
        
        # Sort profiles by existence (found first)
        results["profiles"].sort(key=lambda x: not x["exists"])
        
        return results
    
    def _check_platform(self, platform: str, username: str) -> Dict[str, Any]:
        """
        Check if a username exists on a specific platform
        
        Returns a dictionary with platform information and profile details if found
        """
        # This is a simulation - in a real implementation, this would make API calls
        # or use web scraping techniques to check if the profile exists
        
        profile = {
            "platform": platform.capitalize(),
            "url": self._get_profile_url(platform, username),
            "exists": self._simulate_profile_exists(platform, username),
            "username": username
        }
        
        # If the profile exists, add additional information
        if profile["exists"]:
            if platform == "twitter":
                profile.update({
                    "bio": "Example Twitter bio for demonstration",
                    "followers": 1234,
                    "following": 567,
                    "joined": "January 2019",
                    "verified": False
                })
            elif platform == "github":
                profile.update({
                    "bio": "Software Developer",
                    "repositories": 45,
                    "followers": 89,
                    "joined": "March 2018",
                    "contributions": 1256
                })
            elif platform == "linkedin":
                profile.update({
                    "name": "John Doe",
                    "title": "Senior Developer at Example Corp",
                    "location": "San Francisco, CA",
                    "connections": "500+"
                })
            elif platform == "instagram":
                profile.update({
                    "posts": 123,
                    "followers": 5678,
                    "following": 432,
                    "verified": False
                })
            elif platform == "reddit":
                profile.update({
                    "karma": 12345,
                    "cake_day": "April 2017",
                    "active_communities": ["programming", "python", "cybersecurity"]
                })
        
        return profile
    
    def _get_profile_url(self, platform: str, username: str) -> str:
        """Generate a profile URL based on platform and username"""
        url_formats = {
            "twitter": f"https://twitter.com/{username}",
            "facebook": f"https://facebook.com/{username}",
            "instagram": f"https://instagram.com/{username}",
            "linkedin": f"https://linkedin.com/in/{username}",
            "github": f"https://github.com/{username}",
            "reddit": f"https://reddit.com/user/{username}",
            "youtube": f"https://youtube.com/@{username}",
            "tiktok": f"https://tiktok.com/@{username}",
            "pinterest": f"https://pinterest.com/{username}",
            "medium": f"https://medium.com/@{username}",
            "quora": f"https://quora.com/profile/{username}",
            "stackoverflow": f"https://stackoverflow.com/users/{username}",
            "dev.to": f"https://dev.to/{username}"
        }
        
        return url_formats.get(platform, f"https://{platform}.com/{username}")
    
    def _simulate_profile_exists(self, platform: str, username: str) -> bool:
        """
        Simulate checking if a profile exists
        
        In a real implementation, this would make actual checks
        """
        # For demonstration purposes, we'll say profiles exist on major platforms
        # and randomly on others
        major_platforms = ["twitter", "github", "linkedin", "instagram", "reddit"]
        
        if platform in major_platforms:
            return True
        else:
            # Randomly determine if profile exists on other platforms
            # In a real implementation, this would be an actual check
            import random
            return random.choice([True, False])
    
    def display_results(self, results: Dict[str, Any]) -> None:
        """Display social media investigation results in a formatted table"""
        found_count = sum(1 for profile in results["profiles"] if profile["exists"])
        
        console.print(f"\n[bold green]Results for username:[/bold green] [bold cyan]{results['username']}[/bold cyan]")
        console.print(f"[bold]Profiles found:[/bold] {found_count} out of {len(results['profiles'])}")
        
        # Display found profiles
        if found_count > 0:
            table = Table(title="Found Profiles")
            table.add_column("Platform", style="cyan")
            table.add_column("URL", style="blue")
            table.add_column("Details", style="green")
            
            for profile in results["profiles"]:
                if profile["exists"]:
                    details = []
                    for key, value in profile.items():
                        if key not in ["platform", "url", "exists", "username"]:
                            details.append(f"{key}: {value}")
                    
                    details_text = "\n".join(details) if details else ""
                    
                    table.add_row(
                        profile["platform"],
                        profile["url"],
                        details_text
                    )
            
            console.print(table)
        
        # Display platforms where profile was not found
        not_found = [p["platform"] for p in results["profiles"] if not p["exists"]]
        if not_found:
            console.print("\n[bold yellow]Not found on:[/bold yellow] " + ", ".join(not_found))

def analyze_social_presence(username: str, verbose: bool = False) -> Dict[str, Any]:
    """
    Main function to analyze social media presence for a username
    
    Returns a dictionary with all findings
    """
    investigator = SocialMediaInvestigator(verbose=verbose)
    results = investigator.search_username(username)
    investigator.display_results(results)
    return results

if __name__ == "__main__":
    # Example usage when run directly
    analyze_social_presence("testuser", verbose=True)