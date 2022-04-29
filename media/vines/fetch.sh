#!/bin/sh

userId="927060056233623552"

mkdir -p output
mkdir -p output/json
mkdir -p output/video/high
mkdir -p output/video/low


# JSON

echo "Fetching JSON..."

curl -s "https://archive.vine.co/profiles/_/${userId}.json" > "output/json/user-${userId}.json"

for postId in $(cat "output/json/user-${userId}.json" | jq -r '.posts[]'); do
    curl -s "https://archive.vine.co/posts/${postId}.json" > "output/json/post-${postId}.json"
    sleep 1
done

echo "Fetching videos..."

# Video

for postId in $(cat "output/json/user-${userId}.json" | jq -r '.posts[]'); do
    postJsonFile="output/json/post-${postId}.json"

    createdAt=$(cat "${postJsonFile}" | jq -r .created)
    videoUrl=$(cat "${postJsonFile}" | jq -r .videoUrl)
    videoLowUrl=$(cat "${postJsonFile}" | jq -r .videoLowURL)

    creationDate=$(gdate --date="${createdAt}" +%Y-%m-%d)
    videoFileName="output/video/high/${creationDate}.${postId}.mp4"
    videoLowFileName="output/video/low/${creationDate}.${postId}-low.mp4"

    echo "Downloading ${creationDate}.${postId}...\n"

    curl "${videoUrl}" --output ${videoFileName}
    sleep 1
    curl "${videoLowUrl}" --output ${videoLowFileName}
    sleep 1

    echo ""
done
