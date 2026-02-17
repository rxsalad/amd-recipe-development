# https://hub.docker.com/r/rocm/vllm/tags
FROM docker.io/rocm/vllm:rocm7.0.0_vllm_0.11.1_20251103

# Install essential utilities
RUN apt-get update && apt-get install -y curl net-tools iputils-ping nano tree

# Optional: Install VS Code Server
RUN curl -Lk 'https://code.visualstudio.com/sha/download?build=stable&os=cli-alpine-x64' -o vscode_cli.tar.gz && \
    tar -xf vscode_cli.tar.gz && \
    mv code /usr/local/bin/code && \
    rm vscode_cli.tar.gz

# To connect using VS Code:
# Log in the instance using the terminal, and then run the following commands:
# code tunnel user login --provider github
# nohup code tunnel --accept-server-license-terms --name 001 &> output.log &

# Install rclone and prepare config directory
# https://rclone.org/downloads/
RUN curl -Lk 'https://downloads.rclone.org/v1.71.2/rclone-v1.71.2-linux-amd64.deb' -o rclone-v1.71.2-linux-amd64.deb && \
    dpkg -i rclone-v1.71.2-linux-amd64.deb && \
    rm rclone-v1.71.2-linux-amd64.deb && \
    mkdir -p /root/.config/rclone

RUN pip install --upgrade pip
RUN pip install python-dotenv pymongo 

    
WORKDIR /app

COPY test_cases_default.csv helper.py benchmarker.py /app/

#CMD ["python3", "benchmarker.py"]

CMD ["sleep", "infinity"]

# Image: docker.io/richardxgf/amd:vllm_benchmarker_1.0
# https://hub.docker.com/repository/docker/richardxgf/amd/tags