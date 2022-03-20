import json
import tqdm

import transformers


def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = []
        for s in f:
            data.append(json.loads(s))
    return data


def translate(data, model_name, batch_size):
    model_name = './experiments/contest_train'
    new_data = []
    tokenizer = transformers.MarianTokenizer.from_pretrained(model_name)
    model = transformers.MarianMTModel.from_pretrained(model_name)
    for batch_start_ind in tqdm.tqdm(range(0, len(data), batch_size)):
        data_trim = data[batch_start_ind : batch_start_ind + batch_size]
        src_text = [data_trim[_]['translation']['ru'] for _ in range(len(data_trim))]
        translated = model.generate(**tokenizer(src_text, return_tensors="pt", padding=True))
        new_data.extend([tokenizer.decode(t, skip_special_tokens=True) for t in translated])
    return new_data


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


if __name__ == '__main__':
    test_data_path = './train_transformers/data/test.json'
    submit_path = './train_transformers/data/submission.jsonl'
    data = read_json(test_data_path)
    
    model_name = './experiments/contest_train'
    translated = translate(data, model_name, 20)
    new_data = format_output(data, translated)
    write_output(submit_path, new_data)
    