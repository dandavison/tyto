from dataclasses import dataclass
from datetime import datetime
from typing import NamedTuple, Optional, Protocol, runtime_checkable


@runtime_checkable
class Serializable(Protocol):
    def to_dict(self) -> dict: ...


@dataclass
class PR:
    repo: str
    number: int
    title: str
    branch: str

    @property
    def url(self) -> str:
        return f"https://github.com/{self.repo}/pull/{self.number}"

    def __rich__(self) -> str:
        return f"[link={self.url}]#{self.number} {self.title}[/link]"


@dataclass
class Run(Serializable):
    repo: str
    id: int
    time: datetime
    pr: Optional[PR]

    @property
    def url(self) -> str:
        return f"https://github.com/{self.repo}/actions/runs/{self.id}"

    def to_dict(self) -> dict:
        return {
            "repo": self.repo,
            "id": self.id,
            "time": self.time.isoformat(),
            "pr": self.pr.__dict__ if self.pr is not None else None,
        }

    def title(self) -> str:
        t = f"{self.repo} #{self.id}"
        if self.pr is not None:
            t += f" {self.pr.title}"
        return t


class TestResult(NamedTuple):
    artifact: str

    # run-level fields
    repo: str
    branch: str
    run_id: int
    sha: str
    pr: Optional[int]
    pr_title: Optional[str]

    # suite-level fields
    file: str
    suite: str
    suite_time: datetime
    suite_duration: float

    # test-level fields
    name: str  # Name of the test function
    classname: str  # Name of class or module containing the test function
    duration: float
    passed: bool
    skipped: bool
    flaky: bool
    message: Optional[str]  # Failure message
    text: Optional[str]  # Stack trace or code context of failure

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.artifact}, {self.repo}, {self.branch}, {self.run_id}, {self.file}, {self.name})"

    def __repr__(self) -> str:
        return self.__str__()

    def make_pr(self) -> Optional[PR]:
        if self.pr is None or self.pr_title is None:
            return None
        return PR(
            repo=self.repo,
            number=self.pr,
            title=self.pr_title,
            branch=self.branch,
        )


TreeSitterLanguageName = str  # TODO
