# Description
ChatGrid

# Installation and run process
## 1. Download docker image

Pull the ChatGrid user interface [docker image](https://hub.docker.com/r/walternzd/chatgrid_chat_ui):

```bash
docker pull walternzd/chatgrid_chat_ui:latest-multi-platform
```

> [!NOTE]
> This is a multi-architecture image supporting both **ARM64** (Apple Silicon M1/M2/M3) and **AMD64** (Intel/AMD x86_64). Docker automatically selects the correct architecture for your system.

<details>
<summary>Optional: Manually specify architecture</summary>

If you need to run a specific architecture (e.g., for testing), use:
```bash
# For ARM64 (Apple Silicon)
docker pull --platform linux/arm64 walternzd/chatgrid_chat_ui:latest-multi-platform

# For AMD64 (Intel/AMD)
docker pull --platform linux/amd64 walternzd/chatgrid_chat_ui:latest-multi-platform
```
</details>


## 2. Run docker image

>[!TIP]
> Check that your [chatgrid_backend server](../chatgrid_backend/README.md) is running at: http://127.0.0.1:2024  

Run the docker image:
```bash
docker run -d --name chatgrid_chat_ui -p 8080:80 walternzd/chatgrid_chat_ui:latest-multi-platform
```

Then open http://localhost:8080/ and click `Continue` to start the chat.

Stop the docker image:
```bash
docker stop chatgrid_chat_ui
```