#! /bin/sh

mkdir -p /home
cd /home

git clone https://github.com/k-seta/trpg-bot2.git
cd trpg-bot2

export DISCORD_BOT_TOKEN=$(curl -H "Metadata-Flavor: Google" 'http://metadata.google.internal/computeMetadata/v1/instance/attributes/discord-bot-token')

cp .env.tmp .env
sed -i -e "s/DISCORD_BOT_TOKEN=/DISCORD_BOT_TOKEN=${DISCORD_BOT_TOKEN}/g" .env

docker compose up -d
