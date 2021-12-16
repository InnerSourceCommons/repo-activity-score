# repo-activity-score

The goal of this repository is to collect reference implementations of the [Repository Activity Score](https://patterns.innersourcecommons.org/p/repository-activity-score).

Currently we got only a single implementation (in Python), but are considering to add similar versions for JavaScript, Go and C#. Feel free to contribute other implementations! :)

## Installation

```bash
pip install repo-activity-score
```

## Usage

```python
import repo_score.score as Score

# code sample - get the repo json data
# https://github.com/zkoppert/innersource-crawler
github_repo_json = github.get_repo

score = Score.calculate(github_repo_json)
```

## Limitations

These implementations assume that the repositories for which you want to calculate the Repository Activity Score are hosted in GitHub i.e. the respective metadata is available via the GitHub Search API and GitHub stats/participation API.
The current algorithm is based on the structure available through the [zkoppert/innersource-crawler](https://github.com/zkoppert/innersource-crawler) result.

Some incompatibility could be found, however, it should be possible with relatively low effort to adapt these implementations to other version control systems.

## Educational purposes only

These implementations are provided as reference implementations and with that for educational purposes only.

## License

[MIT](LICENSE)
