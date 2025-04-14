import pandas as pd
from pandera.errors import SchemaError
from config import schema, source_columns_to_rename


class DataValidatorAndProcessor:
    def __new__(cls, source_data: dict):
        instance = super().__new__(cls)
        instance.schema = schema
        instance.data = instance.parse_input_data(source_data).drop_duplicates() # source contains duplicates
        return instance.validate_and_clean()

    @staticmethod
    def parse_input_data(source_data) -> pd.DataFrame:
        parsed = pd.DataFrame.from_records(source_data)
        parsed.rename(columns=source_columns_to_rename, inplace=True)
        return parsed

    def validate_and_clean(self) -> pd.DataFrame:
        try:
            validated_data = self.schema.validate(self.data)
        except SchemaError as e:
            raise ValueError(f'Failing data validation error: {e}')

        for col in validated_data.columns:
            if pd.api.types.is_integer_dtype(validated_data[col]):
                validated_data[col] = validated_data[col].apply(lambda x: int(x) if pd.notna(x) else None)
            elif pd.api.types.is_datetime64_any_dtype(validated_data[col]):
                validated_data[col] = validated_data[col].apply(lambda x: x.to_pydatetime() if pd.notna(x) else None)

        return validated_data.to_dict(orient='records')
