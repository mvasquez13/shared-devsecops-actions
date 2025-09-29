import time
import os
import argparse
from prometheus_remote_writer import RemoteWriter


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Send DevSecOps metrics to Grafana Cloud',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage with required parameters
  python send_data.py --app-name "mibanco-demo" --app-version "1.0.0" \\
    --build-status 1 --code-coverage 85.5 --execution-time 120

  # Full example with all vulnerabilities
  python send_data.py --app-name "mibanco-demo" --app-version "1.0.0-20250929" \\
    --environment "production" --build-status 1 \\
    --vulnerabilities-critical 0 --vulnerabilities-high 0 \\
    --vulnerabilities-medium 2 --vulnerabilities-low 0 \\
    --code-coverage 88.5 --execution-time 117

  # Using custom Grafana settings
  python send_data.py --app-name "my-app" --app-version "2.0.0" \\
    --build-status 1 --code-coverage 90 --execution-time 150 \\
    --grafana-api-key "your-api-key" \\
    --pushgateway-url "https://your-grafana.com/api/prom/push"
        """)
    
    # Required arguments
    parser.add_argument('--app-name', required=True, 
                       help='Application name (e.g., mibanco-demo)')
    parser.add_argument('--app-version', required=True,
                       help='Application version (e.g., 1.0.0-20250929)')
    parser.add_argument('--build-status', type=int, choices=[0, 1], required=True,
                       help='Build status: 1=success, 0=failure')
    parser.add_argument('--code-coverage', type=float, required=True,
                       help='Code coverage percentage (e.g., 85.5)')
    parser.add_argument('--execution-time', type=int, required=True,
                       help='Pipeline execution time in seconds')
    
    # Optional arguments with defaults
    parser.add_argument('--environment', default='production',
                       help='Environment (default: production)')
    parser.add_argument('--vulnerabilities-critical', type=int, default=0,
                       help='Number of critical vulnerabilities (default: 0)')
    parser.add_argument('--vulnerabilities-high', type=int, default=0,
                       help='Number of high vulnerabilities (default: 0)')
    parser.add_argument('--vulnerabilities-medium', type=int, default=0,
                       help='Number of medium vulnerabilities (default: 0)')
    parser.add_argument('--vulnerabilities-low', type=int, default=0,
                       help='Number of low vulnerabilities (default: 0)')
    
    parser.add_argument('--grafana-api-key', help='Grafana API key (has default)')
    parser.add_argument('--pushgateway-url', help='Pushgateway URL (has default)')
    
    return parser.parse_args()


def print_usage():
    """Print usage information for the script."""
    print("""
Usage: python send_data.py

This script sends DevSecOps metrics to Grafana Cloud using environment variables.

Required environment variables:
  APP_NAME                 - Application name (default: mibanco-demo)
  APP_VERSION             - Application version (default: 1.0.0)
  ENVIRONMENT             - Environment (default: production)
  BUILD_STATUS            - Build status: 1=success, 0=failure (default: 1)
  VULNERABILITIES_CRITICAL - Number of critical vulnerabilities (default: 0)
  VULNERABILITIES_HIGH    - Number of high vulnerabilities (default: 0)
  VULNERABILITIES_MEDIUM  - Number of medium vulnerabilities (default: 0)
  VULNERABILITIES_LOW     - Number of low vulnerabilities (default: 0)
  CODE_COVERAGE_PERCENT   - Code coverage percentage (default: 0)
  EXECUTION_TIME_SECONDS  - Pipeline execution time in seconds (default: 0)

Optional environment variables:
  GRAFANA_API_KEY         - Grafana API key (has default)
  PUSHGATEWAY_URL         - Pushgateway URL (has default)

Example:
  export APP_NAME="my-app"
  export APP_VERSION="1.2.3"
  export BUILD_STATUS=1
  export VULNERABILITIES_CRITICAL=0
  export VULNERABILITIES_HIGH=1
  export VULNERABILITIES_MEDIUM=2
  export VULNERABILITIES_LOW=5
  export CODE_COVERAGE_PERCENT=85.5
  export EXECUTION_TIME_SECONDS=120
  python send_data.py
""")


# Parse command line arguments
args = parse_arguments()

# Configuration from arguments
APP_NAME = args.app_name
APP_VERSION = args.app_version
ENVIRONMENT = args.environment
BUILD_STATUS = args.build_status
VULNERABILITIES_CRITICAL = args.vulnerabilities_critical
VULNERABILITIES_HIGH = args.vulnerabilities_high
VULNERABILITIES_MEDIUM = args.vulnerabilities_medium
VULNERABILITIES_LOW = args.vulnerabilities_low
CODE_COVERAGE_PERCENT = args.code_coverage
EXECUTION_TIME_SECONDS = args.execution_time
API_KEY = args.grafana_api_key
PUSHGATEWAY_URL = args.pushgateway_url

# Create a RemoteWriter instance
writer = RemoteWriter(
    url=PUSHGATEWAY_URL,
    headers={'Authorization': 'Bearer ' + API_KEY},
)

# Prepare the data to send
current_time = int(time.time() * 1000)  # Current time in milliseconds

# DevSecOps metrics data
data = [
    # Build status metric (1=success, 0=failure)
    {
        'metric': {
            '__name__': 'devsecops_build_status',
            'app': APP_NAME,
            'version': APP_VERSION,
            'environment': ENVIRONMENT
        },
        'values': [BUILD_STATUS],
        'timestamps': [current_time]
    },
    # Vulnerabilities by severity
    {
        'metric': {
            '__name__': 'devsecops_vulnerabilities_total',
            'app': APP_NAME,
            'severity': 'critical',
            'environment': ENVIRONMENT
        },
        'values': [VULNERABILITIES_CRITICAL],
        'timestamps': [current_time]
    },
    {
        'metric': {
            '__name__': 'devsecops_vulnerabilities_total',
            'app': APP_NAME,
            'severity': 'high',
            'environment': ENVIRONMENT
        },
        'values': [VULNERABILITIES_HIGH],
        'timestamps': [current_time]
    },
    {
        'metric': {
            '__name__': 'devsecops_vulnerabilities_total',
            'app': APP_NAME,
            'severity': 'medium',
            'environment': ENVIRONMENT
        },
        'values': [VULNERABILITIES_MEDIUM],
        'timestamps': [current_time]
    },
    {
        'metric': {
            '__name__': 'devsecops_vulnerabilities_total',
            'app': APP_NAME,
            'severity': 'low',
            'environment': ENVIRONMENT
        },
        'values': [VULNERABILITIES_LOW],
        'timestamps': [current_time]
    },
    # Code coverage percentage
    {
        'metric': {
            '__name__': 'devsecops_code_coverage_percent',
            'app': APP_NAME,
            'environment': ENVIRONMENT
        },
        'values': [CODE_COVERAGE_PERCENT],
        'timestamps': [current_time]
    },
    # Pipeline execution time
    {
        'metric': {
            '__name__': 'devsecops_execution_time_seconds',
            'app': APP_NAME,
            'environment': ENVIRONMENT
        },
        'values': [EXECUTION_TIME_SECONDS],
        'timestamps': [current_time]
    }
]

# Send the data
try:
    print(f"Sending DevSecOps metrics to Grafana Cloud...")
    print(f"  App: {APP_NAME} v{APP_VERSION}")
    print(f"  Environment: {ENVIRONMENT}")
    print(f"  Build Status: {'SUCCESS' if BUILD_STATUS == 1 else 'FAILURE'}")
    print(f"  Vulnerabilities: Critical={VULNERABILITIES_CRITICAL}, High={VULNERABILITIES_HIGH}, Medium={VULNERABILITIES_MEDIUM}, Low={VULNERABILITIES_LOW}")
    print(f"  Code Coverage: {CODE_COVERAGE_PERCENT}%")
    print(f"  Execution Time: {EXECUTION_TIME_SECONDS}s")
    print()
    
    writer.send(data)
    print("✓ DevSecOps metrics sent successfully to Grafana Cloud!")
    
except Exception as e:
    print(f"✗ Error sending metrics to Grafana Cloud: {e}")
    exit(1) 
