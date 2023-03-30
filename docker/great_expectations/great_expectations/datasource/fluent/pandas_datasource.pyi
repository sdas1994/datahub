import os
import sqlite3
import typing
from logging import Logger
from typing import (
    TYPE_CHECKING,
    AbstractSet,
    Any,
    Callable,
    ClassVar,
    Dict,
    Hashable,
    Iterable,
    Mapping,
    MutableMapping,
    Optional,
    Sequence,
    Set,
    Type,
    TypeVar,
    Union,
)

import pandas as pd
import pydantic
import sqlalchemy
from typing_extensions import Literal

from great_expectations.datasource.fluent.interfaces import (
    Batch,
    BatchRequest,
    BatchRequestOptions,
    DataAsset,
    Datasource,
    _DataAssetT,
)

if TYPE_CHECKING:
    from great_expectations.datasource.fluent import Sorter
    from great_expectations.datasource.fluent.dynamic_pandas import (
        CompressionOptions,
        CSVEngine,
        FilePath,
        IndexLabel,
        StorageOptions,
    )
    from great_expectations.execution_engine import (
        PandasExecutionEngine,
    )
    from great_expectations.validator.validator import Validator

_EXCLUDE_TYPES_FROM_JSON: list[Type]

MappingIntStrAny = Mapping[Union[int, str], Any]
AbstractSetIntStr = AbstractSet[Union[int, str]]
logger: Logger
_PandasDataFrameT = TypeVar("_PandasDataFrameT")

class PandasDatasourceError(Exception): ...

class _PandasDataAsset(DataAsset):
    _EXCLUDE_FROM_READER_OPTIONS: ClassVar[Set[str]]

    def _get_reader_method(self) -> str: ...
    def test_connection(self) -> None: ...
    def batch_request_options_template(self) -> BatchRequestOptions: ...
    def get_batch_list_from_batch_request(
        self, batch_request: BatchRequest
    ) -> list[Batch]: ...
    def build_batch_request(
        self, options: Optional[BatchRequestOptions] = ...
    ) -> BatchRequest: ...
    def _validate_batch_request(self, batch_request: BatchRequest) -> None: ...
    def json(
        self,
        *,
        include: Union[AbstractSetIntStr, MappingIntStrAny, None] = ...,
        exclude: Union[AbstractSetIntStr, MappingIntStrAny, None] = ...,
        by_alias: bool = ...,
        skip_defaults: Union[bool, None] = ...,
        exclude_unset: bool = ...,
        exclude_defaults: bool = ...,
        exclude_none: bool = ...,
        encoder: Union[Callable[[Any], Any], None] = ...,
        models_as_dict: bool = ...,
        **dumps_kwargs: Any
    ) -> str: ...

class ClipboardAsset(_PandasDataAsset): ...
class CSVAsset(_PandasDataAsset): ...
class ExcelAsset(_PandasDataAsset): ...
class FeatherAsset(_PandasDataAsset): ...
class GBQAsset(_PandasDataAsset): ...
class HDFAsset(_PandasDataAsset): ...
class HTMLAsset(_PandasDataAsset): ...
class JSONAsset(_PandasDataAsset): ...
class ORCAsset(_PandasDataAsset): ...
class ParquetAsset(_PandasDataAsset): ...
class PickleAsset(_PandasDataAsset): ...
class SQLAsset(_PandasDataAsset): ...
class SQLQueryAsset(_PandasDataAsset): ...
class SQLTableAsset(_PandasDataAsset): ...
class SASAsset(_PandasDataAsset): ...
class SPSSAsset(_PandasDataAsset): ...
class STATAAsset(_PandasDataAsset): ...
class TableAsset(_PandasDataAsset): ...
class XMLAsset(_PandasDataAsset): ...

class DataFrameAsset(_PandasDataAsset):
    type: Literal["dataframe"]
    dataframe: _PandasDataFrameT  # type: ignore[valid-type]

    def get_batch_list_from_batch_request(
        self, batch_request: BatchRequest
    ) -> list[Batch]: ...

class _PandasDatasource(Datasource):
    asset_types: ClassVar[Sequence[Type[DataAsset]]]
    assets: MutableMapping[str, _DataAssetT]  # type: ignore[valid-type]
    @property
    def execution_engine_type(self) -> Type[PandasExecutionEngine]: ...
    def test_connection(self, test_assets: bool = ...) -> None: ...
    def json(
        self,
        *,
        include: Union[AbstractSetIntStr, MappingIntStrAny, None] = ...,
        exclude: Union[AbstractSetIntStr, MappingIntStrAny, None] = ...,
        by_alias: bool = ...,
        skip_defaults: Union[bool, None] = ...,
        exclude_unset: bool = ...,
        exclude_defaults: bool = ...,
        exclude_none: bool = ...,
        encoder: Union[Callable[[Any], Any], None] = ...,
        models_as_dict: bool = ...,
        **dumps_kwargs: Any
    ) -> str: ...

_DYNAMIC_ASSET_TYPES: list[Type[_PandasDataAsset]]

class PandasDatasource(_PandasDatasource):
    asset_types: ClassVar[Sequence[Type[DataAsset]]]
    type: Literal["pandas"]
    assets: Dict[str, _PandasDataAsset]
    def test_connection(self, test_assets: bool = ...) -> None: ...
    def _get_validator(self, asset: _PandasDataAsset) -> Validator: ...
    def add_dataframe_asset(
        self, name: str, dataframe: pd.DataFrame
    ) -> DataFrameAsset: ...
    def read_dataframe(
        self, dataframe: pd.DataFrame, asset_name: Optional[str] = ...
    ) -> Validator: ...
    def add_clipboard_asset(
        self,
        name: str,
        order_by: typing.List[Sorter] = ...,
        sep: str = "\\s+",
        kwargs: typing.Union[dict, None] = ...,
    ) -> ClipboardAsset: ...
    def add_csv_asset(
        self,
        name: str,
        filepath_or_buffer: pydantic.FilePath | pydantic.AnyUrl,
        order_by: typing.List[Sorter] = ...,
        sep: typing.Union[str, None] = ...,
        delimiter: typing.Union[str, None] = ...,
        header: Union[int, Sequence[int], None, Literal["infer"]] = "infer",
        names: Union[Sequence[Hashable], None] = ...,
        index_col: Union[IndexLabel, Literal[False], None] = ...,
        usecols: typing.Union[int, str, typing.Sequence[int], None] = ...,
        squeeze: typing.Union[bool, None] = ...,
        prefix: str = ...,
        mangle_dupe_cols: bool = ...,
        dtype: typing.Union[dict, None] = ...,
        engine: Union[CSVEngine, None] = ...,
        converters: typing.Any = ...,
        true_values: typing.Any = ...,
        false_values: typing.Any = ...,
        skipinitialspace: bool = ...,
        skiprows: typing.Union[typing.Sequence[int], int, None] = ...,
        skipfooter: int = 0,
        nrows: typing.Union[int, None] = ...,
        na_values: typing.Any = ...,
        keep_default_na: bool = ...,
        na_filter: bool = ...,
        verbose: bool = ...,
        skip_blank_lines: bool = ...,
        parse_dates: typing.Any = ...,
        infer_datetime_format: bool = ...,
        keep_date_col: bool = ...,
        date_parser: typing.Any = ...,
        dayfirst: bool = ...,
        cache_dates: bool = ...,
        iterator: bool = ...,
        chunksize: typing.Union[int, None] = ...,
        compression: CompressionOptions = "infer",
        thousands: typing.Union[str, None] = ...,
        decimal: str = ".",
        lineterminator: typing.Union[str, None] = ...,
        quotechar: str = '"',
        quoting: int = 0,
        doublequote: bool = ...,
        escapechar: typing.Union[str, None] = ...,
        comment: typing.Union[str, None] = ...,
        encoding: typing.Union[str, None] = ...,
        encoding_errors: typing.Union[str, None] = "strict",
        dialect: typing.Union[str, None] = ...,
        error_bad_lines: typing.Union[bool, None] = ...,
        warn_bad_lines: typing.Union[bool, None] = ...,
        on_bad_lines: typing.Any = ...,
        delim_whitespace: bool = ...,
        low_memory: typing.Any = ...,
        memory_map: bool = ...,
        storage_options: StorageOptions = ...,
    ) -> CSVAsset: ...
    def add_excel_asset(
        self,
        name: str,
        io: os.PathLike | str | bytes,
        order_by: typing.List[Sorter] = ...,
        sheet_name: typing.Union[str, int, None] = 0,
        header: Union[int, Sequence[int], None] = 0,
        names: typing.Union[typing.List[str], None] = ...,
        index_col: Union[int, Sequence[int], None] = ...,
        usecols: typing.Union[int, str, typing.Sequence[int], None] = ...,
        squeeze: typing.Union[bool, None] = ...,
        dtype: typing.Union[dict, None] = ...,
        true_values: Union[Iterable[Hashable], None] = ...,
        false_values: Union[Iterable[Hashable], None] = ...,
        skiprows: typing.Union[typing.Sequence[int], int, None] = ...,
        nrows: typing.Union[int, None] = ...,
        na_values: typing.Any = ...,
        keep_default_na: bool = ...,
        na_filter: bool = ...,
        verbose: bool = ...,
        parse_dates: typing.Union[typing.List, typing.Dict, bool] = ...,
        thousands: typing.Union[str, None] = ...,
        decimal: str = ".",
        comment: typing.Union[str, None] = ...,
        skipfooter: int = 0,
        convert_float: typing.Union[bool, None] = ...,
        mangle_dupe_cols: bool = ...,
        storage_options: StorageOptions = ...,
    ) -> ExcelAsset: ...
    def add_feather_asset(
        self,
        name: str,
        path: pydantic.FilePath | pydantic.AnyUrl,
        order_by: typing.List[Sorter] = ...,
        columns: Union[Sequence[Hashable], None] = ...,
        use_threads: bool = ...,
        storage_options: StorageOptions = ...,
    ) -> FeatherAsset: ...
    def add_gbq_asset(
        self,
        name: str,
        query: str,
        order_by: typing.List[Sorter] = ...,
        project_id: typing.Union[str, None] = ...,
        index_col: typing.Union[str, None] = ...,
        col_order: typing.Union[typing.List[str], None] = ...,
        reauth: bool = ...,
        auth_local_webserver: bool = ...,
        dialect: typing.Union[str, None] = ...,
        location: typing.Union[str, None] = ...,
        configuration: typing.Union[typing.Dict[str, typing.Any], None] = ...,
        credentials: typing.Any = ...,
        use_bqstorage_api: typing.Union[bool, None] = ...,
        max_results: typing.Union[int, None] = ...,
        progress_bar_type: typing.Union[str, None] = ...,
    ) -> GBQAsset: ...
    def add_hdf_asset(
        self,
        name: str,
        path_or_buf: str | os.PathLike | pd.HDFStore,
        order_by: typing.List[Sorter] = ...,
        key: typing.Any = ...,
        mode: str = "r",
        errors: str = "strict",
        where: typing.Union[str, typing.List, None] = ...,
        start: typing.Union[int, None] = ...,
        stop: typing.Union[int, None] = ...,
        columns: typing.Union[typing.List[str], None] = ...,
        iterator: bool = ...,
        chunksize: typing.Union[int, None] = ...,
        kwargs: typing.Union[dict, None] = ...,
    ) -> HDFAsset: ...
    def add_html_asset(
        self,
        name: str,
        io: os.PathLike | str,
        order_by: typing.List[Sorter] = ...,
        match: Union[str, typing.Pattern] = ".+",
        flavor: typing.Union[str, None] = ...,
        header: Union[int, Sequence[int], None] = ...,
        index_col: Union[int, Sequence[int], None] = ...,
        skiprows: typing.Union[typing.Sequence[int], int, None] = ...,
        attrs: typing.Union[typing.Dict[str, str], None] = ...,
        parse_dates: bool = ...,
        thousands: typing.Union[str, None] = ",",
        encoding: typing.Union[str, None] = ...,
        decimal: str = ".",
        converters: typing.Union[typing.Dict, None] = ...,
        na_values: Union[Iterable[object], None] = ...,
        keep_default_na: bool = ...,
        displayed_only: bool = ...,
    ) -> HTMLAsset: ...
    def add_json_asset(
        self,
        name: str,
        path_or_buf: pydantic.Json | pydantic.FilePath | pydantic.AnyUrl,
        order_by: typing.List[Sorter] = ...,
        orient: typing.Union[str, None] = ...,
        dtype: typing.Union[dict, None] = ...,
        convert_axes: typing.Any = ...,
        convert_dates: typing.Union[bool, typing.List[str]] = ...,
        keep_default_dates: bool = ...,
        numpy: bool = ...,
        precise_float: bool = ...,
        date_unit: typing.Union[str, None] = ...,
        encoding: typing.Union[str, None] = ...,
        encoding_errors: typing.Union[str, None] = "strict",
        lines: bool = ...,
        chunksize: typing.Union[int, None] = ...,
        compression: CompressionOptions = "infer",
        nrows: typing.Union[int, None] = ...,
        storage_options: StorageOptions = ...,
    ) -> JSONAsset: ...
    def add_orc_asset(
        self,
        name: str,
        path: pydantic.FilePath | pydantic.AnyUrl,
        order_by: typing.List[Sorter] = ...,
        columns: typing.Union[typing.List[str], None] = ...,
        kwargs: typing.Union[dict, None] = ...,
    ) -> ORCAsset: ...
    def add_parquet_asset(
        self,
        name: str,
        path: pydantic.FilePath | pydantic.AnyUrl,
        order_by: typing.List[Sorter] = ...,
        engine: str = "auto",
        columns: typing.Union[typing.List[str], None] = ...,
        storage_options: StorageOptions = ...,
        use_nullable_dtypes: bool = ...,
        kwargs: typing.Union[dict, None] = ...,
    ) -> ParquetAsset: ...
    def add_pickle_asset(
        self,
        name: str,
        filepath_or_buffer: pydantic.FilePath | pydantic.AnyUrl,
        order_by: typing.List[Sorter] = ...,
        compression: CompressionOptions = "infer",
        storage_options: StorageOptions = ...,
    ) -> PickleAsset: ...
    def add_sas_asset(
        self,
        name: str,
        filepath_or_buffer: pydantic.FilePath | pydantic.AnyUrl,
        order_by: typing.List[Sorter] = ...,
        format: typing.Union[str, None] = ...,
        index: Union[Hashable, None] = ...,
        encoding: typing.Union[str, None] = ...,
        chunksize: typing.Union[int, None] = ...,
        iterator: bool = ...,
        compression: CompressionOptions = "infer",
    ) -> SASAsset: ...
    def add_spss_asset(
        self,
        name: str,
        path: pydantic.FilePath,
        order_by: typing.List[Sorter] = ...,
        usecols: typing.Union[int, str, typing.Sequence[int], None] = ...,
        convert_categoricals: bool = ...,
    ) -> SPSSAsset: ...
    def add_sql_asset(
        self,
        name: str,
        sql: sqlalchemy.select | sqlalchemy.text | str,
        con: sqlalchemy.engine.Engine | sqlite3.Connection | str,
        order_by: typing.List[Sorter] = ...,
        index_col: typing.Union[str, typing.List[str], None] = ...,
        coerce_float: bool = ...,
        params: typing.Any = ...,
        parse_dates: typing.Any = ...,
        columns: typing.Union[typing.List[str], None] = ...,
        chunksize: typing.Union[int, None] = ...,
    ) -> SQLAsset: ...
    def add_sql_query_asset(
        self,
        name: str,
        sql: sqlalchemy.select | sqlalchemy.text | str,
        con: sqlalchemy.engine.Engine | sqlite3.Connection | str,
        order_by: typing.List[Sorter] = ...,
        index_col: typing.Union[str, typing.List[str], None] = ...,
        coerce_float: bool = ...,
        params: typing.Union[typing.List[str], typing.Dict[str, str], None] = ...,
        parse_dates: typing.Union[typing.List[str], typing.Dict[str, str], None] = ...,
        chunksize: typing.Union[int, None] = ...,
        dtype: typing.Union[dict, None] = ...,
    ) -> SQLQueryAsset: ...
    def add_sql_table_asset(
        self,
        name: str,
        table_name: str,
        con: sqlalchemy.engine.Engine | str,
        order_by: typing.List[Sorter] = ...,
        schema: typing.Union[str, None] = ...,
        index_col: typing.Union[str, typing.List[str], None] = ...,
        coerce_float: bool = ...,
        parse_dates: typing.Union[typing.List[str], typing.Dict[str, str], None] = ...,
        columns: typing.Union[typing.List[str], None] = ...,
        chunksize: typing.Union[int, None] = ...,
    ) -> SQLTableAsset: ...
    def add_stata_asset(
        self,
        name: str,
        filepath_or_buffer: pydantic.FilePath | pydantic.AnyUrl,
        order_by: typing.List[Sorter] = ...,
        convert_dates: bool = ...,
        convert_categoricals: bool = ...,
        index_col: typing.Union[str, None] = ...,
        convert_missing: bool = ...,
        preserve_dtypes: bool = ...,
        columns: Union[Sequence[str], None] = ...,
        order_categoricals: bool = ...,
        chunksize: typing.Union[int, None] = ...,
        iterator: bool = ...,
        compression: CompressionOptions = "infer",
        storage_options: StorageOptions = ...,
    ) -> STATAAsset: ...
    def add_table_asset(
        self,
        name: str,
        filepath_or_buffer: pydantic.FilePath | pydantic.AnyUrl,
        order_by: typing.List[Sorter] = ...,
        sep: typing.Union[str, None] = ...,
        delimiter: typing.Union[str, None] = ...,
        header: Union[int, Sequence[int], None, Literal["infer"]] = "infer",
        names: Union[Sequence[Hashable], None] = ...,
        index_col: Union[IndexLabel, Literal[False], None] = ...,
        usecols: typing.Union[int, str, typing.Sequence[int], None] = ...,
        squeeze: typing.Union[bool, None] = ...,
        prefix: str = ...,
        mangle_dupe_cols: bool = ...,
        dtype: typing.Union[dict, None] = ...,
        engine: Union[CSVEngine, None] = ...,
        converters: typing.Any = ...,
        true_values: typing.Any = ...,
        false_values: typing.Any = ...,
        skipinitialspace: bool = ...,
        skiprows: typing.Union[typing.Sequence[int], int, None] = ...,
        skipfooter: int = 0,
        nrows: typing.Union[int, None] = ...,
        na_values: typing.Any = ...,
        keep_default_na: bool = ...,
        na_filter: bool = ...,
        verbose: bool = ...,
        skip_blank_lines: bool = ...,
        parse_dates: typing.Any = ...,
        infer_datetime_format: bool = ...,
        keep_date_col: bool = ...,
        date_parser: typing.Any = ...,
        dayfirst: bool = ...,
        cache_dates: bool = ...,
        iterator: bool = ...,
        chunksize: typing.Union[int, None] = ...,
        compression: CompressionOptions = "infer",
        thousands: typing.Union[str, None] = ...,
        decimal: str = ".",
        lineterminator: typing.Union[str, None] = ...,
        quotechar: str = '"',
        quoting: int = 0,
        doublequote: bool = ...,
        escapechar: typing.Union[str, None] = ...,
        comment: typing.Union[str, None] = ...,
        encoding: typing.Union[str, None] = ...,
        encoding_errors: typing.Union[str, None] = "strict",
        dialect: typing.Union[str, None] = ...,
        error_bad_lines: typing.Union[bool, None] = ...,
        warn_bad_lines: typing.Union[bool, None] = ...,
        on_bad_lines: typing.Any = ...,
        delim_whitespace: typing.Any = ...,
        low_memory: typing.Any = ...,
        memory_map: bool = ...,
        float_precision: typing.Union[str, None] = ...,
        storage_options: StorageOptions = ...,
    ) -> TableAsset: ...
    def add_xml_asset(
        self,
        name: str,
        path_or_buffer: pydantic.FilePath | pydantic.AnyUrl,
        order_by: typing.List[Sorter] = ...,
        xpath: str = "./*",
        namespaces: typing.Union[typing.Dict[str, str], None] = ...,
        elems_only: bool = ...,
        attrs_only: bool = ...,
        names: Union[Sequence[str], None] = ...,
        dtype: typing.Union[dict, None] = ...,
        encoding: typing.Union[str, None] = "utf-8",
        stylesheet: Union[FilePath, None] = ...,
        iterparse: typing.Union[typing.Dict[str, typing.List[str]], None] = ...,
        compression: CompressionOptions = "infer",
        storage_options: StorageOptions = ...,
    ) -> XMLAsset: ...
    def read_clipboard(
        self,
        asset_name: Optional[str] = ...,
        order_by: typing.List[Sorter] = ...,
        sep: str = r"\s+",
        kwargs: typing.Union[dict, None] = ...,
    ) -> Validator: ...
    def read_csv(
        self,
        filepath_or_buffer: pydantic.FilePath | pydantic.AnyUrl,
        asset_name: Optional[str] = ...,
        order_by: typing.List[Sorter] = ...,
        sep: typing.Union[str, None] = ...,
        delimiter: typing.Union[str, None] = ...,
        header: Union[int, Sequence[int], None, Literal["infer"]] = "infer",
        names: Union[Sequence[Hashable], None] = ...,
        index_col: Union[IndexLabel, Literal[False], None] = ...,
        usecols: typing.Union[int, str, typing.Sequence[int], None] = ...,
        squeeze: typing.Union[bool, None] = ...,
        prefix: str = ...,
        mangle_dupe_cols: bool = ...,
        dtype: typing.Union[dict, None] = ...,
        engine: Union[CSVEngine, None] = ...,
        converters: typing.Any = ...,
        true_values: typing.Any = ...,
        false_values: typing.Any = ...,
        skipinitialspace: bool = ...,
        skiprows: typing.Union[typing.Sequence[int], int, None] = ...,
        skipfooter: int = 0,
        nrows: typing.Union[int, None] = ...,
        na_values: typing.Any = ...,
        keep_default_na: bool = ...,
        na_filter: bool = ...,
        verbose: bool = ...,
        skip_blank_lines: bool = ...,
        parse_dates: typing.Any = ...,
        infer_datetime_format: bool = ...,
        keep_date_col: bool = ...,
        date_parser: typing.Any = ...,
        dayfirst: bool = ...,
        cache_dates: bool = ...,
        iterator: bool = ...,
        chunksize: typing.Union[int, None] = ...,
        compression: CompressionOptions = "infer",
        thousands: typing.Union[str, None] = ...,
        decimal: str = ".",
        lineterminator: typing.Union[str, None] = ...,
        quotechar: str = '"',
        quoting: int = 0,
        doublequote: bool = ...,
        escapechar: typing.Union[str, None] = ...,
        comment: typing.Union[str, None] = ...,
        encoding: typing.Union[str, None] = ...,
        encoding_errors: typing.Union[str, None] = "strict",
        dialect: typing.Union[str, None] = ...,
        error_bad_lines: typing.Union[bool, None] = ...,
        warn_bad_lines: typing.Union[bool, None] = ...,
        on_bad_lines: typing.Any = ...,
        delim_whitespace: bool = ...,
        low_memory: typing.Any = ...,
        memory_map: bool = ...,
        storage_options: StorageOptions = ...,
    ) -> Validator: ...
    def read_excel(
        self,
        io: os.PathLike | str | bytes,
        asset_name: Optional[str] = ...,
        order_by: typing.List[Sorter] = ...,
        sheet_name: typing.Union[str, int, None] = 0,
        header: Union[int, Sequence[int], None] = 0,
        names: typing.Union[typing.List[str], None] = ...,
        index_col: Union[int, Sequence[int], None] = ...,
        usecols: typing.Union[int, str, typing.Sequence[int], None] = ...,
        squeeze: typing.Union[bool, None] = ...,
        dtype: typing.Union[dict, None] = ...,
        true_values: Union[Iterable[Hashable], None] = ...,
        false_values: Union[Iterable[Hashable], None] = ...,
        skiprows: typing.Union[typing.Sequence[int], int, None] = ...,
        nrows: typing.Union[int, None] = ...,
        na_values: typing.Any = ...,
        keep_default_na: bool = ...,
        na_filter: bool = ...,
        verbose: bool = ...,
        parse_dates: typing.Union[typing.List, typing.Dict, bool] = ...,
        thousands: typing.Union[str, None] = ...,
        decimal: str = ".",
        comment: typing.Union[str, None] = ...,
        skipfooter: int = 0,
        convert_float: typing.Union[bool, None] = ...,
        mangle_dupe_cols: bool = ...,
        storage_options: StorageOptions = ...,
    ) -> Validator: ...
    def read_feather(
        self,
        path: pydantic.FilePath | pydantic.AnyUrl,
        asset_name: Optional[str] = ...,
        order_by: typing.List[Sorter] = ...,
        columns: Union[Sequence[Hashable], None] = ...,
        use_threads: bool = ...,
        storage_options: StorageOptions = ...,
    ) -> Validator: ...
    def read_gbq(
        self,
        query: str,
        asset_name: Optional[str] = ...,
        order_by: typing.List[Sorter] = ...,
        project_id: typing.Union[str, None] = ...,
        index_col: typing.Union[str, None] = ...,
        col_order: typing.Union[typing.List[str], None] = ...,
        reauth: bool = ...,
        auth_local_webserver: bool = ...,
        dialect: typing.Union[str, None] = ...,
        location: typing.Union[str, None] = ...,
        configuration: typing.Union[typing.Dict[str, typing.Any], None] = ...,
        credentials: typing.Any = ...,
        use_bqstorage_api: typing.Union[bool, None] = ...,
        max_results: typing.Union[int, None] = ...,
        progress_bar_type: typing.Union[str, None] = ...,
    ) -> Validator: ...
    def read_hdf(
        self,
        path_or_buf: pd.HDFStore | os.PathLike | str,
        asset_name: Optional[str] = ...,
        order_by: typing.List[Sorter] = ...,
        key: typing.Any = ...,
        mode: str = "r",
        errors: str = "strict",
        where: typing.Union[str, typing.List, None] = ...,
        start: typing.Union[int, None] = ...,
        stop: typing.Union[int, None] = ...,
        columns: typing.Union[typing.List[str], None] = ...,
        iterator: bool = ...,
        chunksize: typing.Union[int, None] = ...,
        kwargs: typing.Union[dict, None] = ...,
    ) -> Validator: ...
    def read_html(
        self,
        io: os.PathLike | str,
        asset_name: Optional[str],
        order_by: typing.List[Sorter] = ...,
        match: Union[str, typing.Pattern] = ".+",
        flavor: typing.Union[str, None] = ...,
        header: Union[int, Sequence[int], None] = ...,
        index_col: Union[int, Sequence[int], None] = ...,
        skiprows: typing.Union[typing.Sequence[int], int, None] = ...,
        attrs: typing.Union[typing.Dict[str, str], None] = ...,
        parse_dates: bool = ...,
        thousands: typing.Union[str, None] = ",",
        encoding: typing.Union[str, None] = ...,
        decimal: str = ".",
        converters: typing.Union[typing.Dict, None] = ...,
        na_values: Union[Iterable[object], None] = ...,
        keep_default_na: bool = ...,
        displayed_only: bool = ...,
    ) -> Validator: ...
    def read_json(
        self,
        path_or_buf: pydantic.Json | pydantic.FilePath | pydantic.AnyUrl,
        asset_name: Optional[str] = ...,
        order_by: typing.List[Sorter] = ...,
        orient: typing.Union[str, None] = ...,
        dtype: typing.Union[dict, None] = ...,
        convert_axes: typing.Any = ...,
        convert_dates: typing.Union[bool, typing.List[str]] = ...,
        keep_default_dates: bool = ...,
        numpy: bool = ...,
        precise_float: bool = ...,
        date_unit: typing.Union[str, None] = ...,
        encoding: typing.Union[str, None] = ...,
        encoding_errors: typing.Union[str, None] = "strict",
        lines: bool = ...,
        chunksize: typing.Union[int, None] = ...,
        compression: CompressionOptions = "infer",
        nrows: typing.Union[int, None] = ...,
        storage_options: StorageOptions = ...,
    ) -> Validator: ...
    def read_orc(
        self,
        path: pydantic.FilePath | pydantic.AnyUrl,
        asset_name: Optional[str] = ...,
        order_by: typing.List[Sorter] = ...,
        columns: typing.Union[typing.List[str], None] = ...,
        kwargs: typing.Union[dict, None] = ...,
    ) -> Validator: ...
    def read_parquet(
        self,
        path: pydantic.FilePath | pydantic.AnyUrl,
        asset_name: Optional[str] = ...,
        order_by: typing.List[Sorter] = ...,
        engine: str = "auto",
        columns: typing.Union[typing.List[str], None] = ...,
        storage_options: StorageOptions = ...,
        use_nullable_dtypes: bool = ...,
        kwargs: typing.Union[dict, None] = ...,
    ) -> Validator: ...
    def read_pickle(
        self,
        filepath_or_buffer: pydantic.FilePath | pydantic.AnyUrl,
        asset_name: Optional[str] = ...,
        order_by: typing.List[Sorter] = ...,
        compression: CompressionOptions = "infer",
        storage_options: StorageOptions = ...,
    ) -> Validator: ...
    def read_sas(
        self,
        filepath_or_buffer: pydantic.FilePath | pydantic.AnyUrl,
        asset_name: Optional[str] = ...,
        order_by: typing.List[Sorter] = ...,
        format: typing.Union[str, None] = ...,
        index: Union[Hashable, None] = ...,
        encoding: typing.Union[str, None] = ...,
        chunksize: typing.Union[int, None] = ...,
        iterator: bool = ...,
        compression: CompressionOptions = "infer",
    ) -> Validator: ...
    def read_spss(
        self,
        path: pydantic.FilePath,
        asset_name: Optional[str],
        order_by: typing.List[Sorter] = ...,
        usecols: typing.Union[int, str, typing.Sequence[int], None] = ...,
        convert_categoricals: bool = ...,
    ) -> Validator: ...
    def read_sql(
        self,
        sql: sqlalchemy.select | sqlalchemy.text | str,
        con: sqlalchemy.engine.Engine | sqlite3.Connection | str,
        asset_name: Optional[str] = ...,
        order_by: typing.List[Sorter] = ...,
        index_col: typing.Union[str, typing.List[str], None] = ...,
        coerce_float: bool = ...,
        params: typing.Any = ...,
        parse_dates: typing.Any = ...,
        columns: typing.Union[typing.List[str], None] = ...,
        chunksize: typing.Union[int, None] = ...,
    ) -> Validator: ...
    def read_sql_query(
        self,
        sql: sqlalchemy.select | sqlalchemy.text | str,
        con: sqlalchemy.engine.Engine | sqlite3.Connection | str,
        asset_name: Optional[str] = ...,
        order_by: typing.List[Sorter] = ...,
        index_col: typing.Union[str, typing.List[str], None] = ...,
        coerce_float: bool = ...,
        params: typing.Union[typing.List[str], typing.Dict[str, str], None] = ...,
        parse_dates: typing.Union[typing.List[str], typing.Dict[str, str], None] = ...,
        chunksize: typing.Union[int, None] = ...,
        dtype: typing.Union[dict, None] = ...,
    ) -> Validator: ...
    def read_sql_table(
        self,
        table_name: str,
        con: sqlalchemy.engine.Engine | str,
        asset_name: Optional[str] = ...,
        order_by: typing.List[Sorter] = ...,
        schema: typing.Union[str, None] = ...,
        index_col: typing.Union[str, typing.List[str], None] = ...,
        coerce_float: bool = ...,
        parse_dates: typing.Union[typing.List[str], typing.Dict[str, str], None] = ...,
        columns: typing.Union[typing.List[str], None] = ...,
        chunksize: typing.Union[int, None] = ...,
    ) -> Validator: ...
    def read_stata(
        self,
        filepath_or_buffer: pydantic.FilePath | pydantic.AnyUrl,
        asset_name: Optional[str] = ...,
        order_by: typing.List[Sorter] = ...,
        convert_dates: bool = ...,
        convert_categoricals: bool = ...,
        index_col: typing.Union[str, None] = ...,
        convert_missing: bool = ...,
        preserve_dtypes: bool = ...,
        columns: Union[Sequence[str], None] = ...,
        order_categoricals: bool = ...,
        chunksize: typing.Union[int, None] = ...,
        iterator: bool = ...,
        compression: CompressionOptions = "infer",
        storage_options: StorageOptions = ...,
    ) -> Validator: ...
    def read_table(
        self,
        filepath_or_buffer: pydantic.FilePath | pydantic.AnyUrl,
        asset_name: Optional[str] = ...,
        order_by: typing.List[Sorter] = ...,
        sep: typing.Union[str, None] = ...,
        delimiter: typing.Union[str, None] = ...,
        header: Union[int, Sequence[int], None, Literal["infer"]] = "infer",
        names: Union[Sequence[Hashable], None] = ...,
        index_col: Union[IndexLabel, Literal[False], None] = ...,
        usecols: typing.Union[int, str, typing.Sequence[int], None] = ...,
        squeeze: typing.Union[bool, None] = ...,
        prefix: str = ...,
        mangle_dupe_cols: bool = ...,
        dtype: typing.Union[dict, None] = ...,
        engine: Union[CSVEngine, None] = ...,
        converters: typing.Any = ...,
        true_values: typing.Any = ...,
        false_values: typing.Any = ...,
        skipinitialspace: bool = ...,
        skiprows: typing.Union[typing.Sequence[int], int, None] = ...,
        skipfooter: int = 0,
        nrows: typing.Union[int, None] = ...,
        na_values: typing.Any = ...,
        keep_default_na: bool = ...,
        na_filter: bool = ...,
        verbose: bool = ...,
        skip_blank_lines: bool = ...,
        parse_dates: typing.Any = ...,
        infer_datetime_format: bool = ...,
        keep_date_col: bool = ...,
        date_parser: typing.Any = ...,
        dayfirst: bool = ...,
        cache_dates: bool = ...,
        iterator: bool = ...,
        chunksize: typing.Union[int, None] = ...,
        compression: CompressionOptions = "infer",
        thousands: typing.Union[str, None] = ...,
        decimal: str = ".",
        lineterminator: typing.Union[str, None] = ...,
        quotechar: str = '"',
        quoting: int = 0,
        doublequote: bool = ...,
        escapechar: typing.Union[str, None] = ...,
        comment: typing.Union[str, None] = ...,
        encoding: typing.Union[str, None] = ...,
        encoding_errors: typing.Union[str, None] = "strict",
        dialect: typing.Union[str, None] = ...,
        error_bad_lines: typing.Union[bool, None] = ...,
        warn_bad_lines: typing.Union[bool, None] = ...,
        on_bad_lines: typing.Any = ...,
        delim_whitespace: typing.Any = ...,
        low_memory: typing.Any = ...,
        memory_map: bool = ...,
        float_precision: typing.Union[str, None] = ...,
        storage_options: StorageOptions = ...,
    ) -> Validator: ...
    def read_xml(
        self,
        path_or_buffer: pydantic.FilePath | pydantic.AnyUrl,
        asset_name: Optional[str] = ...,
        order_by: typing.List[Sorter] = ...,
        xpath: str = "./*",
        namespaces: typing.Union[typing.Dict[str, str], None] = ...,
        elems_only: bool = ...,
        attrs_only: bool = ...,
        names: Union[Sequence[str], None] = ...,
        dtype: typing.Union[dict, None] = ...,
        encoding: typing.Union[str, None] = "utf-8",
        stylesheet: Union[FilePath, None] = ...,
        iterparse: typing.Union[typing.Dict[str, typing.List[str]], None] = ...,
        compression: CompressionOptions = "infer",
        storage_options: StorageOptions = ...,
    ) -> Validator: ...
