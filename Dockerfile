FROM python:3.7-slim

WORKDIR /app

COPY components/module_project_3_backend/setup.cfg .
COPY components/module_project_3_backend/setup.py .

#COPY components/module_project_3_backend /app


RUN pip install --upgrade --no-cache-dir pip && pip install -e ".[dev]"
COPY . .

CMD ["gunicorn", "-b", "0.0.0.0:1111", "private_library.composites.private_library:app", "--reload"]

