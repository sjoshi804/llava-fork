#!/bin/bash

TRAIN_DATA_PATH=$INPUT_DIR/generated_data/spatial_map_gen_task_desc_50k_20240918_merged.json
RUN_ID=spatial_map_mminstruct_3x_10_22_2024

python scripts/process_data.py $TRAIN_DATA_PATH $INPUT_DIR

CUDA_VISIBLE_DEVICES=0,1,2,3 deepspeed llava/train/train_mem.py \
    --deepspeed ./scripts/zero3.json \
    --model_name_or_path liuhaotian/llava-v1.5-7b \
    --version $RUN_ID \
    --data_path $TRAIN_DATA_PATH \
    --image_folder ./data_images \
    --vision_tower openai/clip-vit-large-patch14-336 \
    --mm_projector_type mlp2x_gelu \
    --mm_vision_select_layer -2 \
    --mm_use_im_start_end False \
    --mm_use_im_patch_token False \
    --image_aspect_ratio pad \
    --group_by_modality_length True \
    --bf16 True \
    --output_dir $OUTPUT_DIR/checkpoints/llava_$RUN_ID \
    --num_train_epochs 3 \
    --per_device_train_batch_size 16 \
    --per_device_eval_batch_size 4 \
    --gradient_accumulation_steps 1 \
    --evaluation_strategy "no" \
    --save_strategy "steps" \
    --save_steps 50000 \
    --save_total_limit 1 \
    --learning_rate 2e-5 \
    --weight_decay 0. \
    --warmup_ratio 0.03 \
    --lr_scheduler_type "cosine" \
    --logging_steps 1 \
    --tf32 True \
    --model_max_length 2048 \
    --gradient_checkpointing True \
    --dataloader_num_workers 4 \
    --lazy_preprocess True \
    --report_to wandb

