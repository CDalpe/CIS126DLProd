import paramiko
import hashlib
import datetime
import importlib
from grading.salt import SALT

def connect(host):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(
        hostname=host,
        username='vagrant',
        key_filename='/home/vagrant/.ssh/grading_key'
        )
        return client
    except Exception as e:
        return None

def run_command(client, command):
    stdin, stdout, stderr = client.exec_command(command)
    output = stdout.read().decode().strip()
    return output


def generate_hash(points):
    combined = str(datetime.datetime.now().isocalendar()[1]) + str(datetime.datetime.now().year) + str(points) + SALT
    return hashlib.sha256(combined.encode()).hexdigest()

def grade_lab(lab_number):
    try:
        module = importlib.import_module(f'grading.labs.lab{lab_number:02d}')
        points, objectives = module.run_checks(connect, run_command)
        hash_value = generate_hash(points)
        return {'points': points, 'hash': hash_value, 'objectives': objectives}
    except Exception as e:
        print(f"Grading error: {e}")
        return None