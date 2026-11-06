# Miniature Floodstorm Video Generator

This repository contains the saved prompt and a GitHub Actions workflow that generates an MP4 using Kling 2.5 Turbo Pro through fal.ai.

## One-time setup

1. Create an API key at https://fal.ai/dashboard/keys
2. In this GitHub repository, open **Settings → Secrets and variables → Actions → New repository secret**.
3. Name the secret exactly `FAL_KEY` and paste your fal.ai key as its value. Never put the key in a file or in a chat.

## Generate a video

1. Open the repository's **Actions** tab.
2. Select **Generate Floodstorm Video**.
3. Press **Run workflow**.
4. Leave the prompt empty to use `floodstorm-video-prompt.md`; choose 5 or 10 seconds and vertical 9:16.
5. When the run finishes, open it and download the **floodstorm-video** artifact. It contains `floodstorm-video.mp4`.

The provider may charge for generation. GitHub Actions only orchestrates the job; fal.ai/Kling performs the video generation.
