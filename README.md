# Github LICENSE searcher
Github search for Licence (or another file) on all branches

## Usage
Generate new `Personal Access Token` for [GitHub](https://github.com/settings/tokens)

```bash
export GITHUB_PAT=%GITHUB PERSONAL ACCESS TOKEN%

docker run --rm --env GITHUB_PAT github-search \
    --org "BenHaslamInc"\
    --name "LICENSE"
```

## CLI options

```
optional arguments:
  -h              show this help message and exit
  --org           GitHub organisation (default: clearmatics)
  --name          Search name (default: LICENSE)
```

## Build
```
docker build -t github-search:latest .
```

## Links
* [GitHub's GraphQL Explorer ](https://developer.github.com/v4/explorer/)
