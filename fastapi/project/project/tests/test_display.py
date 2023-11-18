from apps.display.entity import Todo

def test_투두리스트_추가(test_session):
    # given
    new_todo = Todo(content="New", is_completed="N")

    # when
    test_session.add(new_todo)
    test_session.commit()

    # then
    assert new_todo == test_session.query(Todo).filter(Todo.id == 1).first()
