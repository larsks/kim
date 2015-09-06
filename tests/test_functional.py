from kim.mapper import Mapper
from kim.field import Integer, Collection
from .helpers import TestType


def test_field_serialize_from_source():
    """On TestType, our score field is called 'normalised_score' but in the
    json output we just want it to be called 'score'"""

    class MapperBase(Mapper):

        __type__ = TestType

        score = Integer(source='normalised_score')

    obj = TestType(normalised_score=5)

    mapper = MapperBase(obj=obj)
    result = mapper.serialize()

    assert result == {'score': 5}


def test_field_marshal_to_source():
    """On TestType, our score field is called 'normalised_score' but in the
    json input we just want it to be called 'score'"""

    class MapperBase(Mapper):

        __type__ = TestType

        score = Integer(source='normalised_score')

    data = {'score': 5}

    mapper = MapperBase(data=data)
    result = mapper.marshal()

    assert result.normalised_score == 5


def test_field_serialize_from_source_collection():

    class MapperBase(Mapper):

        __type__ = TestType

        scores = Collection(Integer(), source='normalised_scores')

    obj = TestType(normalised_scores=[1, 2, 3])

    mapper = MapperBase(obj=obj)
    result = mapper.serialize()

    assert result == {'scores': [1, 2, 3]}


def test_field_marshal_to_source_collection():

    class MapperBase(Mapper):

        __type__ = TestType

        scores = Collection(Integer(), source='normalised_scores')

    data = {'scores': [1, 2, 3]}

    mapper = MapperBase(data=data)
    result = mapper.marshal()

    assert result.normalised_scores == [1, 2, 3]


def test_field_serialize_from_name():
    """On TestType, we have not defined a custom source so 'name' should be
    used in the json output"""

    class MapperBase(Mapper):

        __type__ = TestType

        my_score = Integer(name='score')

    obj = TestType(score=5)

    mapper = MapperBase(obj=obj)
    result = mapper.serialize()

    assert result == {'score': 5}


def test_field_marshal_to_name():
    """On TestType, we have not defined a custom source so 'name' should be
    used when updating the object"""

    class MapperBase(Mapper):

        __type__ = TestType

        my_score = Integer(name='score')

    data = {'score': 5}

    mapper = MapperBase(data=data)
    result = mapper.marshal()

    assert result.score == 5