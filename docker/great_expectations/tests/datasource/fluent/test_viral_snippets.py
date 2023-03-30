import difflib
import functools
import logging
import pathlib
from pprint import pformat as pf

import pytest

# apply markers to entire test module
pytestmark = [pytest.mark.integration]

from great_expectations import get_context
from great_expectations.data_context import FileDataContext
from great_expectations.datasource.fluent.config import GxConfig
from great_expectations.datasource.fluent.interfaces import Datasource

logger = logging.getLogger(__file__)


@pytest.fixture
def db_file() -> pathlib.Path:
    relative_path = pathlib.Path(
        "..",
        "..",
        "test_sets",
        "taxi_yellow_tripdata_samples",
        "sqlite",
        "yellow_tripdata.db",
    )
    db_file = pathlib.Path(__file__).parent.joinpath(relative_path).resolve(strict=True)
    assert db_file.exists()
    return db_file


@pytest.fixture
def fluent_config_dict(db_file) -> dict:
    return {
        "fluent_datasources": {
            "my_sql_ds": {
                "connection_string": f"sqlite:///{db_file}",
                "name": "my_sql_ds",
                "type": "sql",
                "assets": {
                    "my_asset": {
                        "name": "my_asset",
                        "table_name": "yellow_tripdata_sample_2019_01",
                        "type": "table",
                        "splitter": {
                            "column_name": "pickup_datetime",
                            "method_name": "split_on_year_and_month",
                        },
                        "order_by": [
                            {"key": "year"},
                            {"key": "month"},
                        ],
                    },
                },
            }
        }
    }


@pytest.fixture
def fluent_only_config(fluent_config_dict: dict) -> GxConfig:
    """Creates a fluent `GxConfig` object and ensures it contains at least one `Datasource`"""
    fluent_config = GxConfig.parse_obj(fluent_config_dict)
    assert fluent_config.datasources
    return fluent_config


@pytest.fixture
def fluent_yaml_config_file(
    file_dc_config_dir_init: pathlib.Path, fluent_only_config: GxConfig
) -> pathlib.Path:
    """
    Dump the provided GxConfig to a temporary path. File is removed during test teardown.

    Append fluent config to default config file
    """
    config_file_path = file_dc_config_dir_init / FileDataContext.GX_YML

    assert config_file_path.exists() is True

    with open(config_file_path, mode="a") as f_append:
        yaml_string = "\n# Fluent\n" + fluent_only_config.yaml()
        f_append.write(yaml_string)

    for ds_name in fluent_only_config.datasources.keys():
        assert ds_name in yaml_string

    logger.info(f"  Config File Text\n-----------\n{config_file_path.read_text()}")
    return config_file_path


@pytest.fixture
@functools.lru_cache(maxsize=1)
def fluent_file_context(fluent_yaml_config_file: pathlib.Path) -> FileDataContext:
    context = get_context(
        context_root_dir=fluent_yaml_config_file.parent, cloud_mode=False
    )
    assert isinstance(context, FileDataContext)
    return context


def test_load_an_existing_config(
    fluent_yaml_config_file: pathlib.Path, fluent_only_config: GxConfig
):
    context = get_context(
        context_root_dir=fluent_yaml_config_file.parent, cloud_mode=False
    )

    assert context.fluent_config == fluent_only_config


def test_serialize_fluent_config(fluent_file_context: FileDataContext):
    dumped_yaml: str = fluent_file_context.fluent_config.yaml()
    print(f"  Dumped Config\n\n{dumped_yaml}\n")

    assert fluent_file_context.fluent_config.datasources

    for ds_name, datasource in fluent_file_context.fluent_config.datasources.items():
        assert ds_name in dumped_yaml

        for asset_name in datasource.assets.keys():
            assert asset_name in dumped_yaml


def test_fluent_simple_validate_workflow(fluent_file_context: FileDataContext):
    datasource = fluent_file_context.get_datasource("my_sql_ds")
    assert isinstance(datasource, Datasource)
    batch_request = datasource.get_asset("my_asset").build_batch_request(
        {"year": 2019, "month": 1}
    )

    validator = fluent_file_context.get_validator(batch_request=batch_request)
    result = validator.expect_column_max_to_be_between(
        column="passenger_count", min_value=1, max_value=12
    )
    print(f"  results ->\n{pf(result)}")
    assert result["success"] is True


def test_save_project_does_not_break(fluent_file_context: FileDataContext):
    print(fluent_file_context.fluent_config)
    fluent_file_context._save_project_config()


def test_variables_save_config_does_not_break(fluent_file_context: FileDataContext):
    print(fluent_file_context.fluent_config)
    print(fluent_file_context.variables)
    fluent_file_context.variables.save_config()


def test_save_datacontext_persists_fluent_config(
    file_dc_config_dir_init: pathlib.Path, fluent_only_config: GxConfig
):
    config_file = file_dc_config_dir_init / FileDataContext.GX_YML

    initial_yaml = config_file.read_text()
    for ds_name in fluent_only_config.datasources:
        assert ds_name not in initial_yaml

    context: FileDataContext = get_context(
        context_root_dir=config_file.parent, cloud_mode=False
    )

    context.fluent_config = fluent_only_config
    context._save_project_config()

    final_yaml = config_file.read_text()
    diff = difflib.ndiff(initial_yaml.splitlines(), final_yaml.splitlines())

    print("\n".join(diff))

    for ds_name in fluent_only_config.datasources:
        assert ds_name in final_yaml


def test_add_and_save_fluent_datasource(
    file_dc_config_dir_init: pathlib.Path,
    fluent_only_config: GxConfig,
    db_file: pathlib.Path,
):
    datasource_name = "save_ds_test"
    config_file = file_dc_config_dir_init / FileDataContext.GX_YML

    initial_yaml = config_file.read_text()
    assert datasource_name not in initial_yaml

    context: FileDataContext = get_context(
        context_root_dir=config_file.parent, cloud_mode=False
    )

    ds = context.sources.add_sqlite(
        name=datasource_name, connection_string=f"sqlite:///{db_file}"
    )

    final_yaml = config_file.read_text()
    diff = difflib.ndiff(initial_yaml.splitlines(), final_yaml.splitlines())

    print("\n".join(diff))

    assert datasource_name == ds.name
    assert datasource_name in final_yaml
    # ensure comments preserved
    assert "# Welcome to Great Expectations!" in final_yaml


if __name__ == "__main__":
    pytest.main([__file__, "-vv"])
