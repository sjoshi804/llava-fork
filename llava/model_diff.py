import torch
import argparse
import json
from llava.model import *
from llava.mm_utils import get_model_name_from_path
from llava.model.builder import load_pretrained_model
from llava.utils import disable_torch_init
        
def compute_model_diffs(model_id_1, model_id_2, jsonl_path):
    compute_dtype = torch.bfloat16
    # args
    class ModelArgs():
        def __init__(self):
            self.vision_tower = "openai/clip-vit-large-patch14-336"
            self.mm_projector_type = "mlp2x_gelu"
            self.mm_vision_select_layer = -2
            self.mm_vision_select_feature = "patch"
            self.pretrain_mm_mlp_adapter = None
            self.mm_patch_merge_type = "flat"
            
    model_args = ModelArgs()
    # Load the models
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    _, model1, _, _ = load_pretrained_model(model_id_1, None, get_model_name_from_path(model_id_1), device=device)
    _, model2, _, _ = load_pretrained_model(model_id_2, None, get_model_name_from_path(model_id_1), device=device)
    # Ensure the models are on the same device

    # Iterate through the parameters and compute differences
    diffs = []
    for (name1, param1), (name2, param2) in zip(model1.named_parameters(), model2.named_parameters()):
        if name1 != name2:
            raise ValueError(f"Parameter names do not match: {name1} vs {name2}")
        diff = param1 - param2

        abs_diff = torch.norm(diff).item()
        norm_diff = abs_diff / torch.norm(param1).item()
        
        diffs.append((name1, abs_diff, norm_diff))

        print(f"Difference in {name1}: {abs_diff} (normalized: {norm_diff})")
        
    # Save the differences to a JSONL file
    with open(jsonl_path, 'a') as f:
        json_record = {
            "model_id_1": model_id_1,
            "model_id_2": model_id_2,
            "diffs": diffs
        }
        f.write(json.dumps(json_record) + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compute differences between two models' weights")
    parser.add_argument("--model_id_1", type=str, default="microsoft/Phi-3-vision-128k-instruct", help="ID of the first model")
    parser.add_argument("--model_id_2", type=str, required=True, help="ID of the second model")
    parser.add_argument("--jsonl_path", type=str, default="model_diffs.jsonl", help="Path to save the differences in JSONL format")

    args = parser.parse_args()

    compute_model_diffs(args.model_id_1, args.model_id_2, args.jsonl_path)
