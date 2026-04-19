from django.apps import apps
import logging


# method used to fetch all models details or a specific model detail for a specific application
def fetch_models(app_name=False, model_name=False):
    if app_name and model_name:
        logging.info("Fetching model : %s" %model_name)
        return apps.get_model(app_label=app_name, model_name=model_name)
    logging.info("Fetching App: %s models" %app_name)
    return apps.get_app_config(app_name).get_models()


