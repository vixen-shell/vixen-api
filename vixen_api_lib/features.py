import subprocess, json

def start_feature(feature: str):
    cmd = f'vx-client -f {feature} &'
    subprocess.run(cmd, shell=True)

def start_active_features():
    with open('/home/noha/.config/vixen/active_features.json', 'r') as file:
        active_features = json.load(file)
        file.close()

    for feature in active_features:
        start_feature(feature)