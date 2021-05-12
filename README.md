# Yet another one github search
Github search by all branches

## Usage
Generate new `Personal Access Token` for [GitHub](https://github.com/settings/tokens)

```bash
export GITHUB_PAT=%GITHUB PERSONAL ACCESS TOKEN%

docker run --rm --env GITHUB_PAT github-search \
    --org "BenHaslamInc"\
    --dir ".github/workflows/" \
    --name "LICENCE"
```

## CLI options

```
optional arguments:
  -h, --help         show this help message and exit
  --org ORG          GitHub organisation (default: clearmatics)
  --name              Search name (default: LICENCE)
```

## Build
```
docker build -t github-search:latest .
```

## Links
* [GitHub's GraphQL Explorer ](https://developer.github.com/v4/explorer/)
