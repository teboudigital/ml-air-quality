from src.utils.analysis import correlation_adjacency_matrix, correlation_edge_list, correlation_p_values, sensor_reference_correlation
from src.utils.data_loader import load_air_quality_data


def test_correlation_p_values_match_correlation_shape():
    df = load_air_quality_data().head(500)
    corr = sensor_reference_correlation(df, method="pearson")
    p_values = correlation_p_values(df, method="pearson")

    assert p_values.shape == corr.shape
    assert list(p_values.index) == list(corr.index)
    assert list(p_values.columns) == list(corr.columns)
    assert (p_values.values >= 0).all()
    assert (p_values.values <= 1).all()


def test_correlation_adjacency_matrix_and_edge_list_are_consistent():
    df = load_air_quality_data().head(500)
    corr = sensor_reference_correlation(df, method="spearman")
    p_values = correlation_p_values(df, method="spearman")
    adjacency = correlation_adjacency_matrix(corr, p_values, correlation_threshold=0.7, alpha=0.05)
    edges = correlation_edge_list(corr, adjacency)

    assert adjacency.shape == corr.shape
    assert (adjacency.values.diagonal() == 0).all()
    assert set(adjacency.stack().unique()).issubset({0, 1})
    if not edges.empty:
        assert {"source", "target", "correlation", "abs_correlation"}.issubset(edges.columns)
        assert (edges["abs_correlation"] >= 0.7).all()
