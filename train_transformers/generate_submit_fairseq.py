import torch
import json
import tqdm


def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = []
        for s in f:
            data.append(json.loads(s))
    return data


def format_output(old_data, translated):
    data = []
    assert len(old_data) == len(translated)
    for i, sample in enumerate(old_data):
        sample['translation']['en'] = translated[i]
        data.append(sample)
    return data


def write_output(submit_path, data):
    with open(submit_path, 'w', encoding='utf-8') as f:
        for sample in data:
            f.write(json.dumps(sample, ensure_ascii=False) + '\n')


def translate(data, model_name, batch_size, is_cuda):
    new_data = []
    model = torch.hub.load('pytorch/fairseq', model_name, tokenizer='moses', bpe='fastbpe')
    model.eval()
    if is_cuda:
        model.cuda()
    for batch_start_ind in tqdm.tqdm(range(0, len(data), batch_size)):
        data_trim = data[batch_start_ind : batch_start_ind + batch_size]
        src_text = [data_trim[_]['translation']['ru'] for _ in range(len(data_trim))]
        translated = model.translate(src_text)
        new_data.extend(translated)
    return new_data


if __name__ == '__main__':
    test_data_path = './data/test.json'
    submit_path = './data/submission.jsonl'
    data = read_json(test_data_path)
    
    model_name = 'transformer.wmt19.ru-en'
    translated = translate(data, model_name, 20)
    new_data = format_output(data, translated)
    write_output(submit_path, new_data)
