import sys
sys.path.append('..')

import torch

model_name = ['result/scc_content_300']
save_name = ['scc_content_300.pt']

for i in range(len(model_name)):
    model = torch.load(model_name[i]).to(device='cpu')
    model.eval()

    example1 = torch.randn((1, 1, 128, 128))
    traced_script_module = torch.jit.trace(model, (example1,))  # 不能转换并行GPU训练的模型
    traced_script_module.save(save_name[i])
