from dataclasses import dataclass, field

from models.session import Session


@dataclass(slots=True)
class Project:
    name: str = "Untitled"

    sessions: list[Session] = field(
        default_factory=list,
    )

    current_index: int = 0

    @property
    def current_session(self) -> Session | None:

        if not self.sessions:
            return None

        if self.current_index >= len(self.sessions):
            return None

        return self.sessions[self.current_index]

    def set_current_session(
        self,
        index: int,
    ):

        if 0 <= index < len(self.sessions):
            self.current_index = index

    @property
    def session_count(self) -> int:

        return len(self.sessions)

    def add_session(
        self,
        session: Session,
    ):

        self.sessions.append(
            session,
        )
