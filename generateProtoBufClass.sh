# Installation:
# Download from https://github.com/protocolbuffers/protobuf/releases/download/v3.9.0/protoc-3.9.0-linux-x86_64.zip,
# sudo mkdir /opt/protobuf/
# cd /opt/protobuf/
# unzip ~/Download/protoc-3.9.0-linux-x86_64.zip
#
# sudo pip3 install protobuf
# 
/opt/protobuf/bin/protoc -I=. --python_out=webapp/ resumeDB.proto

