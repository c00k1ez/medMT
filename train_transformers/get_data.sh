mkdir data
cp ../train_test_data/train.jsonl ./data/train.json
cp ../train_test_data/test.jsonl ./data/test.json
cp ../additional_data/clean_data/merged_data.jsonl ./data/merged_data.json
cat ./data/merged_data.json >> ./data/train.json
# shuffle data
sort -o ./data/train.json -R ./data/train.json
FILE_SIZE="$(wc -l < "./data/train.json")"

TRAIN_SIZE=0.8
TRAIN_LEN=$( echo "$TRAIN_SIZE * $FILE_SIZE" | bc)
TRAIN_LEN=$(printf "%.0f\n" $TRAIN_LEN)
VALID_LEN=$(echo "$FILE_SIZE - $TRAIN_LEN" | bc)
echo "Train size: $TRAIN_LEN"
echo "Valid size: $VALID_LEN"
tail -n $VALID_LEN ./data/train.json > ./data/val.json
mv ./data/train.json ./data/train_.json
head -n $TRAIN_LEN ./data/train_.json > ./data/train.json
rm ./data/train_.json