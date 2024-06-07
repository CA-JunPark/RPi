import subprocess

command = "source /home/airobot/yolov8/env/bin/activate"
# Run the command
result = subprocess.run(command, shell=True, capture_output=True, text=True)
# Print the output
print(result.stdout)
