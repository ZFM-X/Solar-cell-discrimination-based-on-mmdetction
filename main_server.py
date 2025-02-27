from server_linux import load_model, app


load_model(
    model_cfg='/home/aiuser/workspace/mmlab/ai_file/20221017/htc_r50_newdata_hs_val48.py',
    checkpoint='/home/aiuser/workspace/mmlab/ai_file/20221017/latest.pth', 
    rule_engine_config='/home/aiuser/workspace/mmlab/ai_file/20221017/rule_engine_config.yaml', 
    # model_cfg='/home/aiuser/workspace/mmlab/ai_file/htc_20220926/htc_r50_newdata_hs_val39.py',
    # checkpoint='/home/aiuser/workspace/mmlab/ai_file/htc_20220926/epoch_130_20220926.pth', 
    # rule_engine_config='/home/aiuser/workspace/mmlab/ai_file/rule_engine_config.yaml', 
    device='cuda:0'
)
app.run(host='0.0.0.0', port=5000)
