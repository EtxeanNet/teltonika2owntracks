
FROM python:3.11-slim AS build
WORKDIR /app
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    POETRY_VERSION="1.7.1" \
    POETRY_VENV=.venv

RUN \
    if [ `dpkg --print-architecture` = "armhf" ]; then \
    printf "[global]\nextra-index-url=https://www.piwheels.org/simple\n" > /etc/pip.conf ; \
    fi
RUN python3 -m venv $POETRY_VENV \
	&& $POETRY_VENV/bin/pip install -U pip setuptools \
	&& $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

ENV PATH="${PATH}:${POETRY_VENV}/bin"
COPY pyproject.toml poetry.lock ./
RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --without dev --no-root

FROM python:3.11-slim AS final
WORKDIR /app
ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1

COPY --from=build ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY ./teltonika_owntracks teltonika_owntracks

# During debugging, this entry point will be overridden. For more information, refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "-m", "teltonika_owntracks"]