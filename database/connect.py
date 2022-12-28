from __future__ import annotations

import collections
import contextlib

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session

db = SQLAlchemy()


@contextlib.contextmanager
def ManagedSession() -> collections.abc.Iterator[scoped_session]:
    if db.session is None:
        raise ValueError("Call create database before using ManagedSession!")
    try:
        yield db.session
        db.session.commit()  # pylint: disable=no-member
        db.session.flush()  # pylint: disable=no-member
    except Exception:
        db.session.rollback()  # pylint: disable=no-member
        # When an exception occurs, handle session session cleaning,
        # but raise the Exception afterwards so that user can handle it.
        raise
