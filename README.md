# Github LICENSE searcher
Github search for license (or another file) on all branches
Returns list of repos that dont have a license and a list of repos that have one in an unusual branch

## Usage

Generate new `Personal Access Token` for [GitHub](https://github.com/settings/tokens)

```bash
export GITHUB_PAT=%GITHUB PERSONAL ACCESS TOKEN%
```

Build the image

```
docker build -t github-search:latest .
```

Run the image

``` bash
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

## Links
* [GitHub's GraphQL Explorer ](https://developer.github.com/v4/explorer/)
