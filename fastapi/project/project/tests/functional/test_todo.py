from fastapi.testclient import TestClient
from project.apps.database import orm


def test_투두리스트_조회(client, test_session):
    # given
    new_todo = orm.Todo(content="New1", is_completed="N")

    test_session.add(new_todo)
    test_session.commit()


    # when
    response = client.get("/todos/")


    # then
    assert response.json()[0]['content'] == new_todo.content
    assert response.json()[0]['is_completed'] == new_todo.is_completed