# tap-bls

`tap-bls` is a Singer tap for bls.

Built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.

## Installation

An example GitLab installation command:

```bash
pipx install git+https://gitlab.com/ORG_NAME/tap-bls.git
```

## Configuration

### Accepted Config Options

| Setting             | Required | Default | Description |
|:--------------------|:--------:|:-------:|:------------|
| registration_key    | True     | None    | Your registration key. Should look like `a7f5b9e2c0d48ba1e6d8c90763e45f7d`. |
| start_year          | True     | Seven years ago | Only records with a year equal to or greater `start_year` will be synced. |
| end_year            | True     | Current year | Only records with a year equal to or less than `end_year` will be synced. |
| series_ids          | True     | None    | An array of series IDs to sync. If more than 50 are provided, they will be split into groups of 50 before querying. |
| stream_maps         | False    | None    | Config object for stream maps capability. For more information check out [Stream Maps](https://sdk.meltano.com/en/latest/stream_maps.html). |
| stream_map_config   | False    | None    | User-defined config values to be used within map expressions. |
| flattening_enabled  | False    | None    | 'True' to enable schema flattening and automatically expand nested properties. |
| flattening_max_depth| False    | None    | The max depth to flatten schemas. |
| batch_config        | False    | None    |             |

A full list of supported settings and capabilities is available by running: `tap-bls --about`

### Configure using environment variables

This Singer tap will automatically import any environment variables within the working directory's
`.env` if the `--config=ENV` is provided, such that config values will be considered if a matching
environment variable is set either in the terminal context or in the `.env` file.

### Source Authentication and Authorization

You can obtain a registration key by registering on the [bls.gov website](https://data.bls.gov/registrationEngine/).

## Usage

You can easily run `tap-bls` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Tap Directly

```bash
tap-bls --version
tap-bls --help
tap-bls --config CONFIG --discover > ./catalog.json
```

## Developer Resources

Follow these instructions to contribute to this project.

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Create and Run Tests

Create tests within the `tests` subfolder and
  then run:

```bash
poetry run pytest
```

You can also test the `tap-bls` CLI interface directly using `poetry run`:

```bash
poetry run tap-bls --help
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._


Next, install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
pipx install meltano
# Initialize meltano within this directory
cd tap-bls
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke tap-bls --version
# OR run a test `elt` pipeline:
meltano elt tap-bls target-jsonl
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to
develop your own taps and targets.
