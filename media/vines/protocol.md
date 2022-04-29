# Vine Archive Protocol

1. Fetch profile (https://archive.vine.co/profiles/_/927060056233623552.json)
    - URL contains user ID
    - Responds with a json blob containing a list of posts

```
$ curl -s https://archive.vine.co/profiles/_/927060056233623552.json | jq

{
  "username": "IG@alexferko",
  "shareUrl": "https://vine.co/u/927060056233623552",
  "userIdStr": "927060056233623552",
  "vanityUrls": [],
  "created": "2013-03-23T01:35:55.000000",
  "posts": [
    "533p0Zx6qm0",
    "53VXJzJzPle",
    "53EOTgtWJj0",
    "53qj55jPPDj",
    "5YwHYxzXZph",
    [...]
  ]
}
```

2. Fetch post (https://archive.vine.co/posts/533p0Zx6qm0.json)
    - URL contains post ID
    - Responds with json blob containing post attributes, including media URLs

```
$ curl -s https://archive.vine.co/posts/533p0Zx6qm0.json | jq

{
  "videoUrl": ...,
  "videoLowURL": ...,
  "videoDashUrl": ...,
  "thumbnailUrl": ...,
}
```

3. Fetch normal and low-bitrate video media (`videoUrl` and `videoLowURL`)
