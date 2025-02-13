from invoke import task


@task
def check(ctx):
    """Check linting with ruff."""
    ctx.run('ruff check')


@task
def format(ctx):
    """Remove unused imports, sort imports, format code."""
    ctx.run('ruff check --select I --fix')
    ctx.run('ruff format')
