import pytest

from kim.field import Field, FieldInvalid, FieldError
from kim.pipelines.base import (
    get_data_from_source, get_data_from_name, update_output_to_name,
    update_output_to_source)


def test_get_data_from_name_pipe():

    data = {
        'name': 'mike',
        'test': 'true',
        'nested': {'foo': 'bar'}
    }

    default = 'bar'
    field = Field(name='foo', required=True)
    field2 = Field(name='foo', default=default, required=False)
    field3 = Field(name='foo', allow_none=False, required=False)

    with pytest.raises(FieldInvalid):
        get_data_from_name(field, data)

    assert get_data_from_name(field2, data) == default

    with pytest.raises(FieldInvalid):
        get_data_from_name(field3, data)


def test_get_data_from_source_pipe():
    data = {
        'name': 'mike'
    }

    field = Field(source='foo')
    assert get_data_from_source(field, data) is None

    field = Field(source='name')
    assert get_data_from_source(field, data) == 'mike'


def test_update_output_to_name_with_object():

    data = {
        'name': 'mike',
        'test': 'true',
        'nested': {'foo': 'bar'}
    }

    class MyObject(object):
        pass

    output = MyObject()
    field = Field(name='name', required=True)
    update_output_to_name(field, data['name'], output)
    assert output.name == 'mike'


def test_update_output_to_name_with_dict():

    data = {
        'name': 'mike',
        'test': 'true',
        'nested': {'foo': 'bar'}
    }

    output = {}

    field = Field(name='name', required=True)
    update_output_to_name(field, data['name'], output)
    assert output == {'name': 'mike'}


def test_update_output_to_name_invalid_output_type():

    data = {
        'name': 'mike',
        'test': 'true',
        'nested': {'foo': 'bar'}
    }

    field = Field(name='name', required=True)
    with pytest.raises(FieldError):
        update_output_to_name(field, data['name'], 1)


def test_update_output_to_source_with_object():

    data = {
        'source': 'mike',
        'test': 'true',
        'nested': {'foo': 'bar'}
    }

    class MyObject(object):
        pass

    output = MyObject()
    field = Field(source='source', required=True)
    update_output_to_source(field, data['source'], output)
    assert output.source == 'mike'


def test_update_output_to_source_with_dict():

    data = {
        'source': 'mike',
        'test': 'true',
        'nested': {'foo': 'bar'}
    }

    output = {}

    field = Field(source='source', required=True)
    update_output_to_source(field, data['source'], output)
    assert output == {'source': 'mike'}


def test_update_output_to_source_invalid_output_type():

    data = {
        'source': 'mike',
        'test': 'true',
        'nested': {'foo': 'bar'}
    }

    field = Field(source='source', required=True)
    with pytest.raises(FieldError):
        update_output_to_source(field, data['source'], 1)