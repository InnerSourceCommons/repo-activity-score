import datetime
import math
import functools


def calculate_score(repo):
    # initial score is 50 to give active repos with low GitHub KPIs (forks, watchers, stars) a better starting point
    iScore = float(50)

    # weighting: forks and watches count most, then stars, add some little score for open issues, too
    iScore += repo["forks_count"] * 5
    iScore += "subscribers_count" in repo or 0
    iScore += repo["stargazers_count"] / 3
    iScore += repo["open_issues_count"] / 5

    # updated in last 3 months: adds a bonus multiplier between 0..1 to overall score (1 = updated today, 0 = updated more than 100 days ago)
    iDaysSinceLastUpdate = (
        datetime.datetime.now().timestamp()
        - datetime.datetime.strptime(
            repo["updated_at"], "%Y-%m-%dT%H:%M:%SZ"
        ).timestamp()
    ) / 86400
    iScore = iScore * ((1 + (100 - min(iDaysSinceLastUpdate, 100))) / 100)

    # evaluate participation stats for the previous  3 months
    if repo["_InnerSourceMetadata"]:
        repo["_InnerSourceMetadata"] or {}

    if "participation" in repo["_InnerSourceMetadata"]:
        # average commits: adds a bonus multiplier between 0..1 to overall score (1 = >10 commits per week, 0 = less than 3 commits per week)
        sliced = repo["_InnerSourceMetadata"]["participation"][
            len(repo["_InnerSourceMetadata"]["participation"]) - 13 :
        ]

        iAverageCommitsPerWeek = functools.reduce(lambda a, b: a + b, sliced) / 13

        iScore = iScore * ((1 + (min(max(iAverageCommitsPerWeek - 3, 0), 7))) / 7)

    # boost calculation:
    # all repositories updated in the previous year will receive a boost of maximum 1000 declining by days since last update
    iBoost = 1000 - min(iDaysSinceLastUpdate, 365) * 2.74
    # gradually scale down boost according to repository creation date to mix with "real" engagement stats
    iDaysSinceCreation = (
        datetime.datetime.now().timestamp()
        - datetime.datetime.strptime(
            repo["created_at"], "%Y-%m-%dT%H:%M:%SZ"
        ).timestamp()
    ) / 86400
    iBoost *= (365 - min(iDaysSinceCreation, 365)) / 365
    # add boost to score
    iScore += iBoost
    # give projects with a meaningful description a static boost of 50
    if (
        len(repo["description"]) > 30
        and repo["_InnerSourceMetadata"]
        or (
            "motivation" in repo["_InnerSourceMetadata"]
            and repo["_InnerSourceMetadata"]["motivation"].length > 30
        )
    ):
        iScore += 50
    # give projects with contribution guidelines (CONTRIBUTING.md) file a static boost of 100
    if repo["_InnerSourceMetadata"] and "guidelines" in repo["_InnerSourceMetadata"]:
        iScore += 100
    # build in a logarithmic scale for very active projects (open ended but stabilizing around 5000)
    if iScore > 3000:
        iScore = 3000 + math.log(iScore) * 100
    # final score is a rounded value starting from 0 (subtract the initial value)
    iScore = round(iScore - 50)

    # add score to metadata on the fly
    repo["_InnerSourceMetadata"]["score"] = iScore

    return iScore
