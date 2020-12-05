from etl.extractor import Extractor
from etl.transformer import Transformer
from etl.loader import Loader


class Runner:
    EXTRACTION_BATCH_SIZE = 10

    @classmethod
    def run(cls):
        extractor = Extractor()
        transformer = Transformer()
        loader = Loader()

        all_users = extractor.extract_all_users()

        for users in cls.chunks(all_users, cls.EXTRACTION_BATCH_SIZE):
            raw_data = extractor.extract_user_shifts(users)
            transformed_shifts = transformer.transform(raw_data)
            loader.load_into_db(transformed_shifts)

    @staticmethod
    def chunks(iterable, size):
        for i in range(0, len(iterable), size):
            yield iterable[i:i + size]


if __name__ == '__main__':
    Runner.run()
