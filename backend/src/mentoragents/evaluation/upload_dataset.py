
from pathlib import Path 
import opik 
from mentoragents.infra.opik_utils import create_opik_dataset
import json

def upload_dataset(name : str, data_path : Path) -> opik.Dataset:
    """
    Uploads a evaluation dataset to opik.

    Args:
        data_path : Path to the evaluation dataset. 

    Returns:
        opik.Dataset : The uploaded dataset. 
    """
    assert data_path.exists(), f"File {data_path} does not exist."

    with open(data_path, "r") as f:
        evaluation_data = json.load(f)

    dataset_items = []
    for sample in evaluation_data["samples"]:
        dataset_items.append(
            {
                "mentor_id" : sample['mentor_id'],
                "messages" : sample['messages']
            }
        )

    dataset = create_opik_dataset(
        name = name,
        description = "Dataset containing question-answer pairs for multiple mentors.",
        items = dataset_items,
    )

    return dataset