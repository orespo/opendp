from opendp.mod import enable_features
from opendp.typing import L1Distance

enable_features('floating-point', 'contrib')


def test_base_laplace():
    from opendp.meas import make_base_laplace
    meas = make_base_laplace(scale=10.5)
    print("base laplace:", meas(100.))
    assert meas.check(1., 1.3)


def test_base_vector_laplace():
    from opendp.meas import make_base_laplace
    meas = make_base_laplace(scale=10.5, D="VectorDomain<AllDomain<f64>>")
    print("base laplace:", meas([80., 90., 100.]))
    assert meas.check(1., 1.3)


def test_base_gaussian():
    from opendp.meas import make_base_gaussian
    meas = make_base_gaussian(scale=10.5)
    print("base gaussian:", meas(100.))
    assert meas.check(1., (1.3, .000001))


def test_base_vector_gaussian():
    from opendp.meas import make_base_gaussian
    meas = make_base_gaussian(scale=10.5, D="VectorDomain<AllDomain<f64>>")
    print("base gaussian:", meas([80., 90., 100.]))
    assert meas.check(1., (1.3, .000001))


def test_base_geometric():
    from opendp.meas import make_base_geometric
    meas = make_base_geometric(scale=2., bounds=(1, 10))
    print("base_geometric in constant time:", meas(100))
    assert meas.check(1, 0.5)
    assert not meas.check(1, 0.49999)

    meas = make_base_geometric(scale=2.)
    print("base_geometric:", meas(100))
    assert meas.check(1, 0.5)
    assert not meas.check(1, 0.49999)


def test_base_vector_geometric():
    from opendp.meas import make_base_geometric
    meas = make_base_geometric(scale=2., D="VectorDomain<AllDomain<i32>>")
    print("vector base_geometric:", meas([100, 10, 12]))
    assert meas.check(1, 0.5)
    assert not meas.check(1, 0.49999)

    meas = make_base_geometric(scale=2., bounds=(10, 100), D="VectorDomain<AllDomain<i32>>")
    print("constant time vector base_geometric:", meas([100, 10, 12]))
    assert meas.check(1, 0.5)
    assert not meas.check(1, 0.49999)


def test_base_stability():
    from opendp.trans import make_count_by
    from opendp.meas import make_base_stability
    meas = (
        make_count_by(size=10, MO=L1Distance[float], TIA=str) >>
        make_base_stability(size=10, scale=20., threshold=1., MI=L1Distance[float], TIK=str)
    )
    print("base stability:", meas(["CAT_A"] * 4 + ["CAT_B"] * 6))
    assert meas.check(1, (2.3, .000001))
