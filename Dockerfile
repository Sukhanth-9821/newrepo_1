#BaseBuilder
FROM python:3.13 as baseimage
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
#Dependencies Instalation
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --prefix=/install -r requirements.txt
COPY . .

#RuntimeImage
FROM python:3.13-slim
RUN useradd -m appuser
WORKDIR /app
#copy from builder image
COPY --from=baseimage /install /usr/local
COPY --from=baseimage /app /app
RUN chown -R appuser:appuser /app
USER appuser
EXPOSE 8000
#Running FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]