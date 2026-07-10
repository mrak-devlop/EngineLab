from dataclasses import dataclass, field

from models.session import Session


@dataclass(slots=True)
class Project:
    name: str = "Untitled"

    sessions: list[Session] = field(
        default_factory=list,
    )

    @property
    def current_session(self) -> Session | None:

        if not self.sessions:
            return None

        return self.sessions[0]

    def add_session(
        self,
        session: Session,
    ):

        self.sessions.append(
            session,
        )
