import hw3.models as models 
import hw3.chunks as chunks 
import hw3.utils  as utils 
import torch

def generation(inp, forward):
    """
    Generate a sequence of words given a starting sequence.
    Load your model before generating words.
    :param inp: Initial sequence of words (batch size, length)
    :param forward: number of additional words to generate
    :return: generated words (batch size, forward)
    """
    model_path = 'models/lr-1e-2-base.pt'
    chunk_path = model_path + '.npy.{}'  # format for each chunk
    data = chunks.read_chunks(chunk_path)
    # Load the data
    state_dict = chunks.load_from_numpy(data)
    model = models.LSTMModelV2(33278, 400, 1150)
    print(model)
    # Load dictionary into your model
    model.load_state_dict(state_dict)
    model.eval()
    if torch.cuda.is_available():
        model = model.cuda()        
    logits  = model(utils.to_variable(utils.to_tensor(inp).long()),forward=forward, stochastic=True)
    classes = torch.max(logits, dim=2)[1]
    return classes[:,forward:].cpu().data.numpy()
