FROM python:3.12-slim

WORKDIR /appdir
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY dev/app /appdir/app
RUN pip install --no-cache-dir -r /appdir/app/requirements.txt

WORKDIR /appdir/app

EXPOSE 8091

CMD ["bash","run.sh" ]


