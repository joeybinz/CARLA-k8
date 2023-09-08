# Carla test

A quick test to see if Carla runs on k8s. This assumes deploying to a
"carla-test" namespace.

1. Auth

```
make auth
```

2. Build

```
make
```

3. Deploy

```
make deploy
```

4.  Stream video from camera on ego car.

    In one tab, start port forwarding:

    ```
    kubectl -n carla-test port-forward $(kubectl -n carla-test get pods -o jsonpath="{.items[*].metadata.name}") 1935:1935
    ```

    In another tab, start ffplay:

    ```
    ffplay  rtmp://localhost:1935/live/test
    ```

    Note, it may take up to a minute for the stream to start (I think it is
    buffering??)
