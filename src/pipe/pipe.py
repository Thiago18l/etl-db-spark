from pyspark.sql import SparkSession
from src.database.session import get_session
from pyspark.sql.functions import col
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import exc as orm_exc
from src.logs.log import Logger
from src.utils.utils import get_states
from src.models.empresas import *
import asyncio

async_session = get_session()
logging = Logger()
ufs: dict = get_states()

# Configuração do Spark
spark = SparkSession.builder \
    .master("local[*]") \
    .appName("ETLcrm") \
    .getOrCreate()

# Função para realizar a gravação assíncrona dos dados no PostgreSQL


async def process_chunk_async(session, class_obj, records):
    try:
        async with session.begin_nested():
            session.bulk_insert_mappings(class_obj, records, render_nulls=True)
            await session.commit()
            logging.info("Chunk processada com sucesso")
    except IntegrityError as e:
        logging.debug(e)
        logging.error("A chunk foi pulada por já existir no banco")
        await session.rollback()
    except orm_exc.FlushError as e:
        logging.debug(e)
        logging.error("Erro ao fazer o flush da chunk")
        await session.rollback()
    except Exception as e:
        logging.error(f"Erro durante o processamento da chunk: {str(e)}")
        await session.rollback()

# Configuração dos parâmetros
batch_size = 50000

# Função para realizar a gravação assíncrona dos dados no PostgreSQL


async def process_chunk_async(session, class_obj, records):
    try:
        async with session.begin_nested():
            session.bulk_insert_mappings(class_obj, records, render_nulls=True)
            await session.commit()
            logging.info("Chunk processada com sucesso")
    except IntegrityError as e:
        logging.debug(e)
        logging.error("A chunk foi pulada por já existir no banco")
        await session.rollback()
    except orm_exc.FlushError as e:
        logging.debug(e)
        logging.error("Erro ao fazer o flush da chunk")
        await session.rollback()
    except Exception as e:
        logging.error(f"Erro durante o processamento da chunk: {str(e)}")
        await session.rollback()

# Função para processar os dados das tabelas de empresas por estado
def process_empresa_table_by_state(state, df):
    class_obj = None
    class_name = f"Empresas{state}"
    class_obj = globals().get(class_name)

    if class_obj is not None:
        records = df.select(
            col("taxpayerRegistry").alias("taxpayerRegistry"),
            col("cnpjOrder").alias("cnpjOrder"),
            col("cnpjDv").alias("cnpjDv"),
            col("branchIdentifier").alias("branchIdentifier"),
            col("fantasyName").alias("fantasyName"),
            col("cadastralSituation").alias("cadastralSituation"),
            col("dateCadastralSituation").alias("dateCadastralSituation"),
            col("reasonCadastralSituation").alias("reasonCadastralSituation"),
            col("outsideCityName").alias("outsideCityName"),
            col("country").alias("country"),
            col("startDateActivity").alias("startDateActivity"),
            col("principalCNAEFiscal").alias("principalCNAEFiscal"),
            col("secondaryCNAEFiscal").alias("secondaryCNAEFiscal"),
            col("typeOfStreet").alias("typeOfStreet"),
            col("street").alias("street"),
            col("number").alias("number"),
            col("complement").alias("complement"),
            col("neighborhood").alias("neighborhood"),
            col("cep").alias("cep"),
            col("UF").alias("UF"),
            col("city").alias("city"),
            col("ddd1").alias("ddd1"),
            col("phone1").alias("phone1"),
            col("ddd2").alias("ddd2"),
            col("phone2").alias("phone2"),
            col("faxDDD").alias("faxDDD"),
            col("fax").alias("fax"),
            col("email").alias("email"),
            col("specialSituation").alias("specialSituation"),
            col("dateSpecialSituation").alias("dateSpecialSituation")
        ).collect()

        async_session = get_session()
        asyncio.run(process_chunk_async(async_session, class_obj, records))

def read_table_in_chunks(df_chunk_size):
    total_rows = spark.table("establishment").count()
    num_iterations = total_rows // df_chunk_size + 1

    for i in range(num_iterations):
        start_index = i * df_chunk_size
        end_index = start_index + df_chunk_size

        df_chunk = spark.sql("""
            SELECT
                est.*,
                c.description AS city_description,
                pc.description AS principal_cnae_description,
                sc.description AS secondary_cnae_description,
                comp.*
            FROM
                establishment est
            LEFT JOIN
                city c ON est.city = c.code
            LEFT JOIN
                cnae pc ON est.principal_cnae_fiscal = pc.code
            LEFT JOIN
                cnae sc ON est.secondary_cnae_fiscal = sc.code
            LEFT JOIN
                company comp ON est.taxpayer_registry = comp.taxpayer_registry
            WHERE
                est.tax_regime = 'Simples Nacional'
            LIMIT {0}, {1}
        """.format(start_index, df_chunk_size))

        # Iterar sobre as tabelas e fazer os respectivos joins
        table_names = ["city", "cnae", "company"]

        for table_name in table_names:
            join_condition = None

            if table_name == "city":
                join_condition = "est.city = c.code"
            elif table_name == "cnae":
                join_condition = "est.principal_cnae_fiscal = pc.code OR est.secondary_cnae_fiscal = sc.code"
            elif table_name == "company":
                join_condition = "est.taxpayer_registry = comp.taxpayer_registry"

            if join_condition:
                df_chunk = df_chunk.join(
                    spark.table(table_name).alias(table_name[0]), 
                    col(join_condition), 
                    "left_outer"
                )

        state = ufs[0]  # Substitua 0 pelo índice correto do estado no seu dicionário 'ufs'
        process_empresa_table_by_state(state, df_chunk)
