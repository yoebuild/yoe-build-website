#!/bin/bash

# Build and deploy script for the [yoe] build website
# Usage: source envsetup.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEPLOY_TARGET="yoedistro.org:/srv/http/yoebuild/website/"

yoebuild_deploy() {
	echo "Building site with Zola..."
	cd "$SCRIPT_DIR" || return 1
	zola build || return 1
	echo "Deploying to $DEPLOY_TARGET..."
	rsync -avz --delete public/ "$DEPLOY_TARGET"
}

yoebuild_serve() {
	echo "Starting Zola development server..."
	cd "$SCRIPT_DIR" || return 1
	zola serve
}

echo "[yoe] build website environment loaded."
echo "Available commands:"
echo "  yoebuild_deploy - Build and deploy to $DEPLOY_TARGET"
echo "  yoebuild_serve  - Start local development server"
