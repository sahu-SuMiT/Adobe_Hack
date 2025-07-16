FROM --platform=linux/amd64 python:3.9-slim

# Set working directory
WORKDIR /app

# Set environment variables for better performance
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    OMP_NUM_THREADS=8 \
    OPENBLAS_NUM_THREADS=8 \
    MKL_NUM_THREADS=8 \
    VECLIB_MAXIMUM_THREADS=8 \
    NUMEXPR_NUM_THREADS=8

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the package
COPY pdf_outline_extractor/ /app/pdf_outline_extractor/
COPY main.py setup.py /app/

# Install the package
RUN pip install -e .

# Create directories
RUN mkdir -p /app/input /app/output

# Set the entrypoint
ENTRYPOINT ["python", "main.py"]