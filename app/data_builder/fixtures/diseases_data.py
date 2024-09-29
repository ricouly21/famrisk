import os
import json
import sys
import psycopg2
import time


DB_INFO = {
    "host": os.getenv("DB_HOST"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "port": 5432,
}

FIXTURES_DIR = os.getenv("FIXTURES_DIR")

TABLE_DISEASETYPE = "diseases_core_diseasetype"
TABLE_DISEASE = "diseases_core_disease"

DISEASETYPE_COLNAMES = ("code", "short_name", "full_name")
DISEASE_JSON_COLNAMES = (
    "disease_code",
    "disease_name",
    "short_name",
    "disease_type",
    "gender_specific",
    "show",
    "main_question",
    "umls_id",
)
DISEASE_TBL_COLNAMES = (
    "disease_type",
    "code",
    "full_name",
    "short_name",
    "specific_gender",
    "umls_id",
    "is_hidden",
)

DISEASETYPES_JSON = f"{FIXTURES_DIR}/DiseaseTypes.json"
DISEASES_JSON = f"{FIXTURES_DIR}/Diseases.json"

diseasetype_list = []
disease_list = []


def timer(func):
    def run_timer(*args, **kwargs):
        st_time = time.perf_counter()
        result = func(*args, **kwargs)
        print("Done!")
        print(f"Query took {time.perf_counter() - st_time} seconds.")
        return result

    return run_timer


@timer
def execute_query(raw_query, many=False):
    with psycopg2.connect(**DB_INFO) as conn:
        with conn.cursor() as cursor:
            cursor = conn.cursor()
            # cursor.execute("SELECT version();")
            # version = cursor.fetchone()
            # print(f"version: {version}")
            try:
                cursor.execute(raw_query)
            except Exception as e:
                print(f"Postgres Error: {str(e)}")


@timer
def execute_query_with_results(raw_query, many=False):
    result = []
    with psycopg2.connect(**DB_INFO) as conn:
        with conn.cursor() as cursor:
            try:
                cursor.execute(raw_query)
                if many:
                    result = [item for item in cursor.fetchall()]
                else:
                    result = cursor.fetchone()
            except Exception as e:
                print(f"Postgres Error: {str(e)}")
    return result


def generate_raw_query(table_name, colnames, values):
    raw_query = f"""
    INSERT INTO {table_name} ({colnames}) 
    VALUES {",".join(values)}
    RETURNING (id,{colnames});
    """
    print(raw_query)
    return raw_query


def get_diseasetype(id):
    result = execute_query_with_results(
        f"""
        SELECT id,{",".join(DISEASETYPE_COLNAMES)} from {TABLE_DISEASETYPE}
        WHERE id={id}
        """,
        False,
    )
    return result


def get_diseasetype_by_name(name):
    result = execute_query_with_results(
        f"""
        SELECT id,{",".join(DISEASETYPE_COLNAMES)} from {TABLE_DISEASETYPE}
        WHERE short_name LIKE '%{name}%' OR full_name LIKE '%{name}%';
        """,
        False,
    )
    return result


def create_diseasetypes():
    with open(DISEASETYPES_JSON, "r") as json_file:
        diseasetype_list: list[dict] = json.load(json_file)
        colnames = ",".join(DISEASETYPE_COLNAMES)
        values = []

        print("\nGenerating disease types ...")
        for diseasetype in diseasetype_list:
            code, short_name, full_name = diseasetype.values()
            values.append(f"('{code}','{short_name}','{full_name}')")
        execute_query(generate_raw_query(TABLE_DISEASETYPE, colnames, values), False)


def delete_diseasetypes_all():
    # Delete table data
    print("\nDeleting disease types ...")
    execute_query(f"DELETE FROM {TABLE_DISEASETYPE};", False)
    # Reset sequence IDs
    print(f"\nResetting sequence IDs ...")
    execute_query(
        f"ALTER SEQUENCE public.{TABLE_DISEASETYPE}_id_seq RESTART WITH 1;", False
    )


def create_diseases():
    # def generate_raw_query(colnames, values):
    #     raw_query = f"""
    #     INSERT INTO {TABLE_DISEASETYPE} ({colnames})
    #     VALUES {",".join(values)}
    #     RETURNING (id,{colnames});
    #     """
    #     return raw_query

    # def generate_raw_query(*args, **kwargs):
    #     disease = {**kwargs}
    #     colnames = ",".join(DISEASE_COLNAMES)
    #     values = [f"'{disease[col]}'" for col in DISEASE_COLNAMES]
    #     raw_query = f"""
    #     INSERT INTO {TABLE_DISEASE} ({colnames})
    #     VALUES ({",".join(values)})
    #     RETURNING (id,{colnames})
    #     ;
    #     """
    #     return raw_query

    with open(DISEASES_JSON, "r") as json_file:
        disease_list: list[dict] = json.load(json_file)
        colnames = ",".join(DISEASE_TBL_COLNAMES)
        values = []

        print("\nGenerating diseases list ...")
        for disease in disease_list:
            (
                disease_code,
                disease_name,
                short_name,
                disease_type,
                gender_specific,
                show,
                main_question,
                umls_id,
            ) = disease.values()

            # Change key names to matching table columns.
            code = disease_code
            full_name = disease_name
            specific_gender = gender_specific
            is_hidden = show == "" or show is None

            disease_type = get_diseasetype_by_name(disease_type)
            disease_type_id = disease_type[0] if disease_type else None

            values.append(
                f"('{disease_type_id}','{code}','{full_name}','{short_name}','{specific_gender}','{umls_id}','{is_hidden}')"
            )

            print(f"Disease: {disease}", f"DiseaseTypeID: {disease_type_id}")
            # execute_query(generate_raw_query(
            #     disease_type_id=disease_type_id,
            #     **disease))
        generate_raw_query(TABLE_DISEASETYPE, colnames, values)
        # execute_query(generate_raw_query(TABLE_DISEASETYPE, colnames, values), False)


def delete_diseases_all():
    # Delete table data
    print("\nDeleting diseases ...")
    execute_query(f"DELETE FROM {TABLE_DISEASE};", False)
    # Reset sequence IDs
    print(f"\nResetting sequence IDs ...")
    execute_query(
        f"ALTER SEQUENCE public.{TABLE_DISEASE}_id_seq RESTART WITH 1;", False
    )


def run():
    # delete_diseasetypes_all()
    # create_diseasetypes()

    delete_diseases_all()
    create_diseases()


if __name__ == "__main__":
    run()
