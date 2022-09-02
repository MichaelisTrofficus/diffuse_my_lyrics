import os
import pip
from setuptools import find_packages, setup


pip_major = int(pip.__version__.split(".")[0])

if pip_major < 10:
    from pip.download import PipSession
    from pip.req import parse_requirements
elif pip_major < 20:
    from pip._internal.download import PipSession
    from pip._internal.req import parse_requirements
else:
    from pip._internal.network.session import PipSession
    from pip._internal.req.req_file import parse_requirements

here = os.path.abspath(os.path.dirname(__file__))

# Extract the requirements from the deps file.
session = PipSession()
process_requirements = parse_requirements("requirements.txt", session=session)
complete_reqs = list(process_requirements)
try:
    requirements = [str(ir.req) for ir in complete_reqs]
except:  # noqa: E722
    requirements = [str(ir.requirement) for ir in complete_reqs]

with open("README_package.md", "r") as fh:
    long_description = fh.read()

setup(
    name="diffuse_my_lyrics",
    version="0.0.1",
    author="MTrofficus",
    author_email="miguel.otero.pedrido.1993@gmail.com",
    description="A dummy project to generate images from song lyrics using Latent Stable Diffusion",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MichaelisTrofficus/diffuse_my_lyrics",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=requirements,
    python_requires='>=3.7.0',
)
