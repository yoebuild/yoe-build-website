# Download the binary (Linux x86_64)
curl -L https://github.com/yoebuild/yoe/releases/latest/download/yoe-Linux-x86_64 -o yoe
chmod +x yoe && mv yoe ~/bin/

# Create a project, build, run
yoe init yoe-test
cd yoe-test
yoe build base-image
yoe run base-image
