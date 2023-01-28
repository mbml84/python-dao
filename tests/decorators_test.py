from __future__ import annotations

from python_dao.exceptions import MultipleResultFound
from python_dao.exceptions import NoResultFound
from tests import utils_test as utils


class TestFunctionDecorator:

    def test_simple_decorator(self):

        objs = utils.simple_decorator(utils.Dummy)(utils.create_many)(0)
        assert len(objs) == 2
        assert all([isinstance(obj, utils.Dummy) for obj in objs])

    def test_formatter(self):
        objs = utils.decorator_with_formatter(utils.Dummy)(utils.create_many_non_formatted)(0)
        assert len(objs) == 2
        assert all([isinstance(obj, utils.Dummy) for obj in objs])

    def test_adapter(self):
        objs = utils.decorator_with_adapter(
            utils.Dummy,
            cache_time=10,
        )(utils.create_many)(0)

        assert len(objs) == 2
        assert all([isinstance(obj, utils.Dummy) for obj in objs])

    def test_formatter_and_adapter(self):
        objs = utils.full_param_decorator(
            utils.Dummy,
            cache_time=10,
        )(utils.create_many_non_formatted)(0)

        assert len(objs) == 2
        assert all([isinstance(obj, utils.Dummy) for obj in objs])

    def test_simple_decorator_raise_exception(self):

        objs = utils.simple_decorator(
            utils.Dummy,
            raise_exception=True,
        )(utils.create_many)(0)

        assert len(objs) == 2
        assert all([isinstance(obj, utils.Dummy) for obj in objs])

    def test_formatter_raise_exception(self):
        objs = utils.decorator_with_formatter(
            utils.Dummy,
            raise_exception=True,
        )(utils.create_many_non_formatted)(0)

        assert len(objs) == 2
        assert all([isinstance(obj, utils.Dummy) for obj in objs])

    def test_adapter_raise_exception(self):
        objs = utils.decorator_with_adapter(
            utils.Dummy,
            cache_time=10,
            raise_exception=True,
        )(utils.create_many)(0)

        assert len(objs) == 2
        assert all([isinstance(obj, utils.Dummy) for obj in objs])

    def test_formatter_and_adapter_raise_exception(self):
        objs = utils.full_param_decorator(
            utils.Dummy,
            cache_time=10,
            raise_exception=True,
        )(utils.create_many_non_formatted)(0)

        assert len(objs) == 2
        assert all([isinstance(obj, utils.Dummy) for obj in objs])

    def test_simple_decorator_many_false(self):

        obj = utils.simple_decorator(utils.Dummy, many=False)(utils.create_one)(0)
        assert isinstance(obj, utils.Dummy)

    def test_formatter_many_false(self):
        obj = utils.decorator_with_formatter(utils.Dummy, many=False)(utils.create_one_non_formatted)(0)
        assert isinstance(obj, utils.Dummy)

    def test_adapter_many_false(self):
        obj = utils.decorator_with_adapter(
            utils.Dummy,
            cache_time=10,
            many=False,
        )(utils.create_one)(0)

        assert isinstance(obj, utils.Dummy)

    def test_formatter_and_adapter_many_false(self):
        obj = utils.full_param_decorator(
            utils.Dummy,
            cache_time=10,
            many=False,
        )(utils.create_one_non_formatted)(0)

        assert isinstance(obj, utils.Dummy)

    def test_simple_decorator_raise_exception_many_false(self):

        obj = utils.simple_decorator(
            utils.Dummy,
            raise_exception=True,
            many=False,
        )(utils.create_one)(0)

        assert isinstance(obj, utils.Dummy)

    def test_formatter_raise_exception_many_false(self):
        obj = utils.decorator_with_formatter(
            utils.Dummy,
            raise_exception=True,
            many=False,
        )(utils.create_one_non_formatted)(0)

        assert isinstance(obj, utils.Dummy)

    def test_adapter_raise_exception_many_false(self):
        obj = utils.decorator_with_adapter(
            utils.Dummy,
            cache_time=10,
            raise_exception=True,
            many=False,
        )(utils.create_one)(0)

        assert isinstance(obj, utils.Dummy)

    def test_formatter_and_adapter_raise_exception_many_false(self):
        obj = utils.full_param_decorator(
            utils.Dummy,
            cache_time=10,
            raise_exception=True,
            many=False,
        )(utils.create_one_non_formatted)(0)

        assert isinstance(obj, utils.Dummy)

    def test_many_false_with_multiple_results(self):
        exception_raised = False
        try:
            _ = utils.simple_decorator(
                utils.Dummy,
                many=False,
            )(utils.create_many)(0)
        except MultipleResultFound:
            exception_raised = True

        assert exception_raised

    def test_no_result_with_raise_exception(self):
        exception_raised = False
        try:
            _ = utils.simple_decorator(
                utils.Dummy,
                raise_exception=True,
            )(utils.create_nothing)(0)
        except NoResultFound:
            exception_raised = True

        assert exception_raised

    def test_many_false_with_no_result(self):

        obj = utils.simple_decorator(
            utils.Dummy,
            many=False,
        )(utils.create_nothing)(0)

        assert obj is None


__all__ = [
    'TestFunctionDecorator',
]
