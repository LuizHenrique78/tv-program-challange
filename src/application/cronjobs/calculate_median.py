import logging

from src.domain.services.tv_data_service import TvDataService

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def run_cron_task():
    logging.info("🔄 Iniciando processamento diário de TV Data...")

    service = TvDataService()
    audience_csv_key = "tvaberta_program_audience.csv"
    inventory_csv_key = "tvaberta_inventory_availability.csv"
    service.process_and_store_data(audience_csv_key, inventory_csv_key)

    logging.info("✅ Processamento concluído e salvo no Redis.")


if __name__ == "__main__":
    run_cron_task()
