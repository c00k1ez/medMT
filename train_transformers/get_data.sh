mkdir data
cp ../train_test_data/train.jsonl ./data
cp ../train_test_data/test.jsonl ./data
cp ../additional_data/clean_data/merged_data.jsonl ./data
cat ./data/merged_data.jsonl >> ./data/train.jsonl
# shuffle data
sort -o ./data/train.jsonl -R ./data/train.jsonl
FILE_SIZE="$(wc -l < "./data/train.jsonl")"

TRAIN_SIZE=0.8
TRAIN_LEN=$( echo "$TRAIN_SIZE * $FILE_SIZE" | bc)
TRAIN_LEN=$(printf "%.0f\n" $TRAIN_LEN)
VALID_LEN=$(echo "$FILE_SIZE - $TRAIN_LEN" | bc)
echo "Train size: $TRAIN_LEN"
echo "Valid size: $VALID_LEN"
tail -n $VALID_LEN ./data/train.jsonl > ./data/val.jsonl
mv ./data/train.jsonl ./data/train_.jsonl
head -n $TRAIN_LEN ./data/train_.jsonl > ./data/train.jsonl
rm ./data/train_.jsonl