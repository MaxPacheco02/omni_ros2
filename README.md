## Dependencies:
```Shell
pip install grpcio
pip install grpcio-tools
pip install pygame
pip install protobuf==3.20.*

# Build proto:
cd ~/[your ws]/src/oav_utils/scripts
python3 -m grpc_tools.protoc -I ./interface --python_out=. --grpc_python_out=. ./interface/rpi-motor.proto
```

## SSH Interface
# Ethernet
ssh user@192.168.55.1

# Max Hotspot
ssh user@10.42.0.243

# RPI
ssh pi@192.168.1.11