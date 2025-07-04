from mentoragents.core.config import settings
from loguru import logger
from opik.configurator.configure import OpikConfigurator
import os
import opik

def configure_opik() -> None:
    if settings.COMET_API_KEY and settings.COMET_PROJECT:
        try:
            client = OpikConfigurator(api_key = settings.COMET_API_KEY)
            default_workspace = client._get_default_workspace()
        
        except Exception:
            logger.warning("Default workspace not found. Settings workspace to None and enabling interactive mode.")

        os.environ["OPIK_PROJECT_NAME"] = settings.COMET_PROJECT
        try:
            opik.configure(
                api_key = settings.COMET_API_KEY,
                workspace = default_workspace, 
                use_local = False,
                force = True
            )
            logger.info(f"Opik configured successfully with workspace : {default_workspace} and project : {settings.COMET_PROJECT}")
        
        except Exception:
            logger.warning(
                "Couldn't configure Opik. There is probably a problem with the COMET_API_KEY or COMET_PROJECT environment variables or with the Opik server."
            )
    else:
        logger.warning(
            "COMET_API_KEY and COMET_PROJECT are not set. Set them to enable prompt monitoring with Opik (powered by Comet ML)."
        )
    
def get_opik_dataset(name : str) -> opik.Dataset | None:
    try:
        client = opik.Opik()
        dataset = client.get_dataset(name=name)
        return dataset
    except Exception:
        return None
    
def create_opik_dataset(name : str, description: str, items: list[dict]) -> opik.Dataset:
    client = opik.Opik()
    client.delete_dataset(name=name)
    dataset = client.create_dataset(name=name, description=description)
    dataset.insert(items)
    return dataset