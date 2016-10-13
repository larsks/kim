import pytest
import decimal

from kim.field import FieldInvalid, Integer, Decimal
from kim.pipelines.base import Session
from kim.pipelines.numeric import is_valid_integer, is_valid_decimal

from ..conftest import get_mapper_session


def test_is_valid_integer_pipe():
    """test piping data through is_valid_integer.
    """

    field = Integer(name='test')
    session = Session(field, 'test', {})

    with pytest.raises(FieldInvalid):
        is_valid_integer(session)

    session.data = '2'
    assert is_valid_integer(session) == 2
    session.data = 2
    assert is_valid_integer(session) == 2
    session.data = 2.3
    assert is_valid_integer(session) == 2


def test_integer_input():

    field = Integer(name='name', required=True)

    mapper_session = get_mapper_session(
        data={'email': 'mike@mike.com'}, output={})
    with pytest.raises(FieldInvalid):
        field.marshal(mapper_session)

    mapper_session = get_mapper_session(
        data={'name': 'foo', 'email': 'mike@mike.com'}, output={})
    with pytest.raises(FieldInvalid):
        field.marshal(mapper_session)

    output = {}
    mapper_session = get_mapper_session(
        data={'name': 2, 'email': 'mike@mike.com'}, output=output)
    field.marshal(mapper_session)
    assert output == {'name': 2}

    output = {}
    mapper_session = get_mapper_session(
        data={'name': '2', 'email': 'mike@mike.com'}, output=output)
    field.marshal(mapper_session)
    assert output == {'name': 2}


def test_numeric_memoize_no_existing_value():
    """ensure field sets only the new_value when the field has no
    exsiting value.
    """

    field = Integer(name='num', required=True)

    output = {}
    mapper_session = get_mapper_session(
        data={'num': 2, 'email': 'mike@mike.com'}, output=output)

    field.marshal(mapper_session)
    assert field._old_value is None
    assert field._new_value is 2


def test_numeric_memoize_no_change():
    """ensure field sets no changes when the field value remains the same
    """

    field = Integer(name='num', required=True)

    output = {'num': 2}
    mapper_session = get_mapper_session(
        data={'num': 2, 'email': 'mike@mike.com'}, output=output)

    field.marshal(mapper_session)
    assert field._old_value is None
    assert field._new_value is None


def test_numeric_memoize_new_value():
    """ensure field sets both old value and new value when the field has an
    existing value and a new value is provided.
    """

    field = Integer(name='num', required=True)

    output = {'num': 2}
    mapper_session = get_mapper_session(
        data={'num': 3, 'email': 'mike@mike.com'}, output=output)

    field.marshal(mapper_session)
    assert field._old_value == 2
    assert field._new_value == 3


def test_integer_field_invalid_type():

    field = Integer(name='name')
    mapper_session = get_mapper_session(
        data={'name': None, 'email': 'mike@mike.com'}, output={})
    with pytest.raises(FieldInvalid):
        field.marshal(mapper_session)


def test_integer_output():

    class Foo(object):
        name = 2

    field = Integer(name='name', required=True)

    output = {}
    mapper_session = get_mapper_session(obj=Foo(), output=output)
    field.serialize(mapper_session)
    assert output == {'name': 2}


def test_marshal_read_only_integer():

    field = Integer(name='name', read_only=True, required=True)

    output = {}
    mapper_session = get_mapper_session(
        data={'id': 2, 'email': 'mike@mike.com'}, output=output)

    field.marshal(mapper_session)
    assert output == {}


def test_marshal_default():

    field = Integer(name='name', default=5)

    output = {}
    mapper_session = get_mapper_session(data={}, output=output)

    field.marshal(mapper_session)
    assert output == {'name': 5}


def test_is_valid_choice():

    field = Integer(name='type', choices=[1, 2])
    output = {}
    mapper_session = get_mapper_session(data={'type': 3}, output=output)
    with pytest.raises(FieldInvalid):
        field.marshal(mapper_session)

    mapper_session = get_mapper_session(data={'type': 1}, output=output)
    field.marshal(mapper_session)
    assert output == {'type': 1}


def test_min_max():

    field = Integer(name='age', min=20, max=35)
    output = {}

    mapper_session = get_mapper_session(data={'age': 15}, output=output)
    with pytest.raises(FieldInvalid):
        field.marshal(mapper_session)

    mapper_session = get_mapper_session(data={'age': 40}, output=output)
    with pytest.raises(FieldInvalid):
        field.marshal(mapper_session)

    mapper_session = get_mapper_session(data={'age': 25}, output=output)
    field.marshal(mapper_session)
    assert output == {'age': 25}

    mapper_session = get_mapper_session(data={'age': '25'}, output=output)
    field.marshal(mapper_session)
    assert output == {'age': 25}


def test_is_valid_decimal_pipe():
    """test piping data through is_valid_decimal.
    """

    field = Decimal(name='test')
    session = Session(field, 'test', {})

    with pytest.raises(FieldInvalid):
        is_valid_decimal(session)

    session.data = '2.5'
    assert is_valid_decimal(session) == decimal.Decimal('2.5')
    session.data = 2
    assert is_valid_decimal(session) == decimal.Decimal(2)
    session.data = 2.3
    assert is_valid_decimal(session) == decimal.Decimal(2.3)


def test_decimal_input():

    field = Decimal(name='name', required=True)

    mapper_session = get_mapper_session(
        data={'email': 'mike@mike.com'}, output={})
    with pytest.raises(FieldInvalid):
        field.marshal(mapper_session)

    mapper_session = get_mapper_session(
        data={'name': 'foo', 'email': 'mike@mike.com'}, output={})
    with pytest.raises(FieldInvalid):
        field.marshal(mapper_session)

    output = {}
    mapper_session = get_mapper_session(
        data={'name': 2, 'email': 'mike@mike.com'}, output=output)
    field.marshal(mapper_session)
    assert output == {'name': decimal.Decimal(2)}


def test_decimal_input_precision():

    field = Decimal(name='name', required=True, precision=4)

    output = {}
    mapper_session = get_mapper_session(
        data={'name': '3.147261', 'email': 'mike@mike.com'}, output=output)
    field.marshal(mapper_session)
    assert output == {'name': decimal.Decimal('3.1473')}


def test_decimal_field_invalid_type():

    field = Decimal(name='name')
    mapper_session = get_mapper_session(
        data={'name': None, 'email': 'mike@mike.com'}, output={})
    with pytest.raises(FieldInvalid):
        field.marshal(mapper_session)


def test_decimal_output():

    class Foo(object):
        name = decimal.Decimal('2.52')

    field = Decimal(name='name', required=True)

    output = {}
    mapper_session = get_mapper_session(obj=Foo(), output=output)
    field.serialize(mapper_session)
    assert output == {'name': '2.52000'}
