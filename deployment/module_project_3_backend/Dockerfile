FROM python:3.7-slim

WORKDIR /app

COPY ./components/module_project_3_backend/setup.cfg .
COPY ./components/module_project_3_backend/setup.py .
COPY dist ./dist/


RUN pip install --upgrade --no-cache-dir pip && pip install -e ".[dev]"
RUN pip install ./dist/*.tar.gz


COPY components/module_project_3_backend/ .
COPY . .

#CMD['cunsumer']
#CMD['cli']
CMD ["gunicorn", "-b", "0.0.0.0:1111", "components.module_project_3_backend.private_library.composites.private_library_api:app", "--reload"]

