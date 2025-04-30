# Use a lightweight stable Ubuntu base
FROM ubuntu:20.04

# Disable interactive prompts during build
ENV DEBIAN_FRONTEND=noninteractive

# Update, fix release info if needed, install socat
RUN apt update --allow-releaseinfo-change && \
    apt install -y socat && \
    apt clean

# Expose UDP port 80
EXPOSE 80/udp

# When container starts, launch a UDP listener
CMD ["socat", "-v", "UDP4-RECVFROM:80,fork", "STDOUT"]
