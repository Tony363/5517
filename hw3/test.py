import requests

def main()->None:
    """
    curl -X POST http://your-ec2-instance-public-ip/is_leap_year/ -H "Content-Type: application/json" -d '{"year": 2020}'
    curl -X POST http://0.0.0.0:80/is_leap_year/ -H "Content-Type: application/json" -d '{"year": 2020}'
    """
    return

if __name__ == "__main__":
    main()