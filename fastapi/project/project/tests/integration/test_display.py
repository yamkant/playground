from project.apps.database import orm
import pytest

@pytest.mark.skip(reason="Test is skipped for a specific reason")
def test_투두리스트_추가(test_session):
    # given
    new_todo = orm.Todo(content="New", is_completed="N")

    # when
    test_session.add(new_todo)
    test_session.commit()

    # then
    assert new_todo == test_session.query(orm.Todo).filter(orm.Todo.id == 1).first()
