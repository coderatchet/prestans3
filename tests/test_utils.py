from prestans3.utils import is_str, inject_class


def test_is_str():
    assert is_str("yes")
    assert not is_str(1)


class InjectableClass(object):
    pass


def test_inject_class():
    class MyClass(object):
        pass

    new_type = inject_class(MyClass, InjectableClass)
    assert new_type.__bases__ == (InjectableClass, object)


def test_can_inject_class_with_more_than_one_subclass():
    class __A(object):
        pass

    class __B(object):
        pass

    class __C(__A, __B):
        pass

    new_type = inject_class(__C, InjectableClass)
    assert new_type.__name__ == 'Injected{}'.format(__C.__name__)
    first_base = new_type.__bases__[0]
    assert first_base.__name__ == 'Injected{}'.format(__A.__name__)
    assert first_base.__bases__ == (InjectableClass, object)
    second_base = new_type.__bases__[1]
    assert second_base.__name__ == 'Injected{}'.format(__B.__name__)
    assert second_base.__bases__ == (InjectableClass, object)


def test_can_inject_before_custom_class():
    class __A(object):
        pass

    class __B(object):
        pass

    class __C(__A, __B):
        pass

    new_type = inject_class(__C, InjectableClass, __B)
    assert new_type.__name__ == 'Injected{}'.format(__C.__name__)
    assert len(new_type.__bases__) == 3
    assert new_type.__bases__[0] is __A
    new_base = new_type.__bases__[1]
    assert new_base is InjectableClass
    assert new_type.__bases__[2] is __B
    assert new_type.mro() == [new_type, __A, InjectableClass, __B, object]


def test_can_inject_class_in_complex_hierarchy():
    class __A(object):
        pass

    class __B(object):
        pass

    class __X(__A, __B):
        pass

    class __Y(__A):
        pass

    class __Z(__X, __Y, __B):
        pass

    new_type = inject_class(__Z, InjectableClass, __B)
    assert len(new_type.__bases__) == 4
    __new_X = new_type.__bases__[0]
    assert __new_X.__name__ == 'Injected{}'.format(__X.__name__)
    assert len(__new_X.__bases__) == 3


def test_inject_class_returns_original_class_if_target_base_class_is_not_in_mro():
    class __A(object):
        pass

    class __B(object):
        pass

    class __C(__B):
        pass

    assert __A not in __C.mro()
    assert __C is inject_class(__C, InjectableClass, __A)
