import re
from datetime import datetime
from pprint import pprint as print
from re import Match
from string import Template
from time import sleep, time
from typing import List

from progress.bar import Bar
from requests import Response, get
from requests.structures import CaseInsensitiveDict

from prime_vx.issue_trackers._classes._issueTrackerHandler import ITHandler_ABC

RESPONSE_HEADERS: dict[str, int] = {
    "lastPage": 1,
    "tokenLimit": 0,
    "tokenRemaining": 0,
    "tokenReset": 0,
}


class GitHubHandler(ITHandler_ABC):
    def __init__(self, repo: str, owner: str, token: str) -> None:
        self.token: str = token

        foo: str = (
            f"https://api.github.com/repos/{owner}/{repo}/issues?state=all&per_page=100"
        )
        self.endpoint: Template = Template(template=foo + "&page=${page}")

    def parseResponseHeader(self, headers: CaseInsensitiveDict) -> None:
        link: str = headers["link"]
        splitLink: List[str] = link.split(sep=",")

        lastPageLink: str = ""
        if len(splitLink) == 2:
            lastPageLink = splitLink[1]
        else:
            lastPageLink = splitLink[2]

        lastPageMatch: Match[str] | None = re.search(r"[?&]page=(\d+)", lastPageLink)
        lastPage: int | None = int(lastPageMatch.group(1)) if lastPageMatch else None

        RESPONSE_HEADERS["lastPage"] = lastPage
        RESPONSE_HEADERS["tokenLimit"] = int(headers["x-ratelimit-limit"])
        RESPONSE_HEADERS["tokenRemaining"] = int(headers["x-ratelimit-remaining"])
        RESPONSE_HEADERS["tokenReset"] = int(headers["x-ratelimit-reset"]) + 10

    def getResponses(self) -> List[Response]:
        data: List[Response] = []

        headers: dict[str, str] = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "prime-vX",
            # "Authorization": f"Bearer {self.token}",
        }

        with Bar("Getting issues...", max=1) as bar:

            def _get(page: int) -> bool:
                print(RESPONSE_HEADERS)
                resp: Response = get(
                    url=self.endpoint.substitute(page=page),
                    headers=headers,
                )
                data.append(resp)

                if resp.status_code != 200:
                    bar.next()
                    return False
                else:
                    self.parseResponseHeader(headers=resp.headers)
                    return True

            if _get(page=1) == False:
                return data

            bar.max = RESPONSE_HEADERS["lastPage"]
            bar.update()
            bar.next()

            stableLastPage: int = RESPONSE_HEADERS["lastPage"]

            page: int
            for page in range(2, stableLastPage + 1):
                if RESPONSE_HEADERS["tokenRemaining"] > 0:
                    pass
                else:
                    currentTime: float = time()
                    diffTime: float = RESPONSE_HEADERS["tokenReset"] - currentTime
                    sleepUntil: datetime = datetime.fromtimestamp(
                        RESPONSE_HEADERS["tokenReset"]
                    )
                    message: str = f"Sleeping until {sleepUntil}..."
                    bar.message = message
                    bar.update()
                    sleep(diffTime)
                    bar.message = "Getting issues..."
                    bar.update()

                if _get(page=page) == False:
                    break
                else:
                    bar.next()

        return data

    def extractIssues(self, resp: Response) -> dict:
        pass


gh = GitHubHandler(repo="numpy", owner="numpy", token="a")

print(len(gh.getResponses()))